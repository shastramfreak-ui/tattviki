import unittest
from retrieval_lab import DOCS, EDGES, readable, bm25, tfidf, rrf, traverse, search, QUERIES
class RetrievalTrainingTests(unittest.TestCase):
 def test_corpus(self):
  self.assertEqual(len(DOCS),28);self.assertGreaterEqual(len(EDGES),18);self.assertEqual(len(QUERIES),6)
 def test_permission_boundaries(self):
  for role in ('viewer','engineer','steward'):
   for mode in ('keyword','vector','hybrid','graph'):
    for q in ('Pump-3 approval','Northforge risk','Customer 360 access'):
     ids={id for id,_ in search(q,mode,role,12)['results']}
     self.assertTrue(all(readable(next(d for d in DOCS if d['id']==id),role) for id in ids))
 def test_graph_edge_roles(self):
  for role in ('viewer','engineer'):
   self.assertFalse(any(e.get('access')=='steward' for e in search('Pump-3 approval','graph',role,12)['links']))
  self.assertTrue(any(e.get('access')=='steward' for e in search('Pump-3 approval','graph','steward',12)['links']))
 def test_role_fail_closed(self):
  with self.assertRaises(ValueError):search('supplier',role='unknown')
 def test_steward_access(self):
  self.assertNotIn('D04',[id for id,_ in search('Pump-3 service approval','graph','viewer',12)['results']])
  self.assertIn('D04',[id for id,_ in search('Pump-3 service approval','graph','steward',12)['results']])
 def test_bm25_exact_code(self):
  self.assertIn('D12',[id for id,_ in search('code INA inactive','keyword',top_k=8)['results']])
 def test_tfidf_scores(self):
  scores=tfidf(DOCS,'industrial supplier valve');self.assertTrue(all(-1<=score<=1 for _,score in scores))
 def test_rrf(self):
  self.assertEqual(rrf([('a',1),('b',.5)],[('b',1),('c',.5)])[0][0],'b')
 def test_graph_traverse(self):
  nodes,links=traverse({'Northforge'},2,role='engineer');self.assertIn('Pump-3',nodes);self.assertGreater(len(links),0)
 def test_metrics(self):
  r=search(QUERIES[0]['q']);self.assertIsNotNone(r['recall_at_k']);self.assertTrue(0<=r['recall_at_k']<=1)
 def test_unlabelled_metrics(self):
  self.assertIsNone(search('unique nonstandard query')['recall_at_k'])
if __name__=='__main__':unittest.main()
