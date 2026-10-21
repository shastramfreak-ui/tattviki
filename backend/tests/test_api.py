"""Offline tests: FastAPI + RDFLib are available; optional owlrl/pyshacl are checked if installed."""
import os
import tempfile
import unittest
from pathlib import Path

TEMP = tempfile.TemporaryDirectory(prefix='tattviki-test-')
os.environ['TATTVIKI_DB'] = str(Path(TEMP.name) / 'test.sqlite')
from fastapi.testclient import TestClient
from backend.main import app, OWLRL_AVAILABLE, SHACL_AVAILABLE

TTL = '''@prefix ex: <https://example.org/tattviki/enterprise#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
ex:CuratedDataset rdfs:subClassOf ex:Dataset .
ex:owner rdfs:domain ex:Dataset ; rdfs:range ex:Organization .
ex:source1 a ex:CuratedDataset ; ex:owner ex:team1 .
ex:source2 a ex:CuratedDataset .
'''
SHAPES = '''@prefix ex: <https://example.org/tattviki/enterprise#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
ex:OwnerShape a sh:NodeShape ; sh:targetClass ex:CuratedDataset ;
 sh:property [ sh:path ex:owner; sh:minCount 1 ].'''

class ApiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=TestClient(app)
 def test_health(self):
  data=self.c.get('/api/health').json()
  self.assertEqual(data['status'],'ok')
  self.assertTrue(data['collaboration'])
 def test_query(self):
  r=self.c.post('/api/sparql',json={'turtle':TTL,'query':'PREFIX ex: <https://example.org/tattviki/enterprise#> SELECT ?s WHERE { ?s a ex:CuratedDataset } ORDER BY ?s'})
  self.assertEqual(r.status_code,200,r.text)
  self.assertEqual(len(r.json()['rows']),2)
 def test_update_rejected(self):
  r=self.c.post('/api/sparql',json={'turtle':TTL,'query':'DELETE WHERE {?s ?p ?o}'})
  self.assertEqual(r.status_code,422)
 def test_service_rejected(self):
  r=self.c.post('/api/sparql',json={'turtle':TTL,'query':'SELECT * WHERE {SERVICE <http://attacker.test/> {?s ?p ?o}}'})
  self.assertEqual(r.status_code,422)
 def test_rdfs_closure(self):
  r=self.c.post('/api/reason',json={'turtle':TTL,'mode':'rdfs'})
  self.assertEqual(r.status_code,200,r.text)
  self.assertGreater(r.json()['inferred_count'],0)
  self.assertIn('Organization',r.json()['inferred_turtle'])
 def test_owlrl_optional(self):
  r=self.c.post('/api/reason',json={'turtle':TTL,'mode':'owlrl'})
  self.assertEqual(r.status_code,200 if OWLRL_AVAILABLE else 503,r.text)
 def test_hermit_optional(self):
  r=self.c.post('/api/reason',json={'turtle':TTL,'mode':'hermit'})
  self.assertIn(r.status_code,(200,503,422))  # Java/ontology compatibility may vary on installed systems
 def test_shacl_optional(self):
  r=self.c.post('/api/shacl',json={'turtle':TTL,'shapes':SHAPES})
  self.assertEqual(r.status_code,200 if SHACL_AVAILABLE else 503,r.text)
  if SHACL_AVAILABLE:self.assertFalse(r.json()['conforms'])
 def test_named_class_search(self):
  r=self.c.post('/api/dlquery',json={'turtle':TTL,'expression':'Dataset and CuratedDataset'})
  self.assertEqual(r.status_code,200,r.text)
  self.assertEqual(r.json()['count'],2)
 def test_invalid_turtle(self):
  self.assertEqual(self.c.post('/api/reason',json={'turtle':'xyz .','mode':'rdfs'}).status_code,422)
 def test_version_and_permissions(self):
  import uuid
  suffix=uuid.uuid4().hex[:8]
  def account(name):
   r=self.c.post('/api/auth/register',json={'username':name,'password':'StrongPassword123!'});self.assertEqual(r.status_code,201,r.text);return {'Authorization':'Bearer '+r.json()['token']}
  owner=account('owner'+suffix);viewer=account('viewer'+suffix);editor=account('editor'+suffix)
  doc={'version':1,'base':'https://example.org/example#','classes':[]}
  r=self.c.post('/api/projects',json={'name':'Master Data Training','document':doc},headers=owner)
  self.assertEqual(r.status_code,201,r.text);pid=r.json()['id']
  self.assertEqual(self.c.get(f'/api/projects/{pid}',headers=viewer).status_code,404)
  self.assertEqual(self.c.post(f'/api/projects/{pid}/members',json={'username':'viewer'+suffix,'role':'viewer'},headers=owner).status_code,200)
  self.assertEqual(self.c.post(f'/api/projects/{pid}/members',json={'username':'editor'+suffix,'role':'editor'},headers=owner).status_code,200)
  self.assertEqual(self.c.get(f'/api/projects/{pid}',headers=viewer).json()['role'],'viewer')
  self.assertEqual(self.c.put(f'/api/projects/{pid}',json={'document':doc,'expected_version':1},headers=viewer).status_code,403)
  doc['classes']=[{'id':'Dataset'}]
  r=self.c.put(f'/api/projects/{pid}',json={'document':doc,'expected_version':1,'message':'Added Dataset'},headers=editor)
  self.assertEqual(r.status_code,200,r.text);self.assertEqual(r.json()['version'],2)
  self.assertEqual(self.c.put(f'/api/projects/{pid}',json={'document':doc,'expected_version':1},headers=owner).status_code,409)
  history=self.c.get(f'/api/projects/{pid}/history',headers=viewer).json()['revisions']
  self.assertEqual([h['version'] for h in history],[2,1])
  self.assertEqual(self.c.post(f'/api/projects/{pid}/restore/1',json={'expected_version':2},headers=viewer).status_code,403)
  r=self.c.post(f'/api/projects/{pid}/restore/1',json={'expected_version':2},headers=owner)
  self.assertEqual(r.status_code,200,r.text);self.assertEqual(r.json()['version'],3)
  self.assertEqual(self.c.get(f'/api/projects/{pid}',headers=owner).json()['document']['classes'],[])
  self.assertEqual(self.c.post(f'/api/projects/{pid}/members',json={'username':'editor'+suffix,'role':'viewer'},headers=editor).status_code,403)
  self.assertEqual(self.c.delete(f'/api/projects/{pid}/members/viewer{suffix}',headers=owner).status_code,200)
  self.assertEqual(self.c.get(f'/api/projects/{pid}',headers=viewer).status_code,404)

if __name__=='__main__':unittest.main(verbosity=2)
