"""Tāttvikī Studio Advanced: local/self-hosted semantic + collaboration API.

Do not publicly expose without HTTPS, authentication hardening, deployment isolation,
and request/time quotas. Only first-party local or configured origins may call this API.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import importlib.util
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode

try:
    from owlrl import DeductiveClosure, OWLRL_Semantics
    OWLRL_AVAILABLE = True
except ImportError:
    OWLRL_AVAILABLE = False
try:
    from pyshacl import validate as shacl_validate
    SHACL_AVAILABLE = True
except ImportError:
    SHACL_AVAILABLE = False

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get('TATTVIKI_DB', str(ROOT / '.data' / 'projects.sqlite3')))
ORIGINS = [x.strip() for x in os.environ.get('TATTVIKI_CORS_ORIGINS', 'http://127.0.0.1:8000,http://localhost:8000,http://127.0.0.1:8081,http://localhost:8081').split(',') if x.strip()]
app = FastAPI(title='Tāttvikī Advanced Studio API', version='6.0.0', docs_url='/docs')
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_methods=['GET','POST','PUT'], allow_headers=['authorization','content-type'])
MAX_TTL = 600_000
MAX_SHAPES = 200_000
MAX_RESULT_ROWS = 150
MAX_PROJECT = 1_250_000

class GraphInput(BaseModel):
    turtle: str = Field(max_length=MAX_TTL)
class SparqlInput(GraphInput):
    query: str = Field(max_length=15_000)
class ShaclInput(GraphInput):
    shapes: str = Field(max_length=MAX_SHAPES)
class ReasonInput(GraphInput):
    mode: Literal['rdfs', 'owlrl', 'hermit'] = 'rdfs'
class DlInput(GraphInput):
    expression: str = Field(max_length=500)
class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=36, pattern=r'^[a-zA-Z][a-zA-Z0-9_-]{2,35}$')
    password: str = Field(min_length=12, max_length=256)
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    document: dict[str, Any]
class ProjectSave(BaseModel):
    document: dict[str, Any]
    expected_version: int = Field(ge=1)
    message: str = Field(default='Updated ontology', max_length=300)
class MemberAdd(BaseModel):
    username: str
    role: Literal['viewer','editor']
class RestoreInput(BaseModel):
    expected_version: int = Field(ge=1)


def parse_turtle(turtle: str) -> Graph:
    try:
        g = Graph()
        g.parse(data=turtle, format='turtle')
    except Exception as exc:
        raise HTTPException(422, f'Invalid Turtle: {str(exc)[:350]}') from None
    if len(g) > 12000:
        raise HTTPException(413, 'Dataset too large for the teaching backend (12,000 triples maximum)')
    return g

def display_term(term):
    return term.n3()[:800]

@app.get('/api/health')
def health():
    return {'status':'ok','version':'6.0','engines':{'sparql':'RDFLib 7-compatible read-only SPARQL', 'rdfs':'built-in subclass, subproperty, domain, range closure', 'owlrl':OWLRL_AVAILABLE, 'hermit':bool(importlib.util.find_spec('owlready2') and shutil.which('java')), 'shacl':SHACL_AVAILABLE,'dl':'DL-style named-class intersection/union instance search'},'collaboration':True, 'limits':{'triples':12000,'results':MAX_RESULT_ROWS},'message':'OWL RL/SHACL require Python dependencies; experimental HermiT OWL DL classification requires owlready2 and Java. Manchester DL parser supports only named classes and and/or.'}

# No federated SPARQL SERVICE, network imports, updates or dataset fetching.
BLOCKED_SPARQL = re.compile(r'\b(SERVICE|LOAD|CLEAR|DROP|CREATE|INSERT|DELETE|COPY|MOVE|ADD|FROM|USING|WITH)\b', re.I)
READ_QUERY = re.compile(r'^(?:(?:PREFIX\s+[\w-]*:\s*<[^>]+>|BASE\s*<[^>]+>)\s*)*(SELECT|ASK|CONSTRUCT|DESCRIBE)\b', re.I | re.S)

@app.post('/api/sparql')
def sparql(payload: SparqlInput):
    g = parse_turtle(payload.turtle)
    # Strip comments and string constants for keyword safety checks, preserving IRI refs.
    query = payload.query
    stripped = re.sub(r'#[^\n]*', '', query)
    # Safer (conservative) keyword block; users can run queries containing these words in IRI with other tools.
    if BLOCKED_SPARQL.search(stripped) or not READ_QUERY.match(query.lstrip()):
        raise HTTPException(422, 'Only local read-only SELECT / ASK / CONSTRUCT / DESCRIBE without SERVICE, FROM or updates is supported.')
    try:
        res = g.query(query)
        if res.type == 'ASK':
            return {'type':'ASK','boolean':bool(res.askAnswer),'triples':len(g)}
        if res.type == 'SELECT':
            vars_ = [str(v) for v in res.vars]
            rows = [{str(v):display_term(row[v]) if row[v] is not None else '' for v in res.vars} for _,row in zip(range(MAX_RESULT_ROWS),res)]
            return {'type':'SELECT','columns':vars_,'rows':rows,'shown':len(rows),'capped_at':MAX_RESULT_ROWS,'triples':len(g)}
        result_graph = Graph()
        for _, triple in zip(range(1000),res.graph): result_graph.add(triple)
        return {'type':res.type,'turtle':result_graph.serialize(format='turtle'),'triples':len(result_graph),'capped_at':1000}
    except Exception as exc:
        raise HTTPException(422, f'SPARQL execution failed: {str(exc)[:350]}') from None


def rdfs_closure(graph: Graph) -> Graph:
    """Documented subset: subclass/subproperty transitivity, typing and domain/range."""
    g=Graph()
    for triple in graph: g.add(triple)
    if len(g)>4000: raise HTTPException(413,'RDFS teaching closure limited to 4,000 asserted triples')
    for i in range(15):
        additions=set()
        for c,_,p in g.triples((None,RDFS.subClassOf,None)):
            for _,_,q in g.triples((p,RDFS.subClassOf,None)): additions.add((c,RDFS.subClassOf,q))
        for p,_,q in g.triples((None,RDFS.subPropertyOf,None)):
            for _,_,r in g.triples((q,RDFS.subPropertyOf,None)): additions.add((p,RDFS.subPropertyOf,r))
        for s,p,o in tuple(g):
            for _,_,sup in g.triples((p,RDFS.subPropertyOf,None)): additions.add((s,sup,o))
            for _,_,d in g.triples((p,RDFS.domain,None)): additions.add((s,RDF.type,d))
            for _,_,r in g.triples((p,RDFS.range,None)):
                if isinstance(o,(URIRef,BNode)): additions.add((o,RDF.type,r))
            if p==RDF.type:
                for _,_,sup in g.triples((o,RDFS.subClassOf,None)): additions.add((s,RDF.type,sup))
        new=additions-set(g)
        if not new:break
        for tr in new: g.add(tr)
        if len(g)>25_000: raise HTTPException(413,'RDFS expansion exceeds 25,000 triples')
    return g

@app.post('/api/reason')
def reason(payload: ReasonInput):
    g=parse_turtle(payload.turtle)
    original=set(g)
    if payload.mode=='hermit':
        if not (importlib.util.find_spec('owlready2') and shutil.which('java')):
            raise HTTPException(503,'HermiT needs optional owlready2 and Java 17+. See backend/requirements-dl.txt. Not tested in this environment.')
        if len(g)>1000: raise HTTPException(413,'HermiT example limited to 1,000 asserted triples')
        try:
            proc=subprocess.run([sys.executable,str(ROOT/'dl_worker.py')],input=payload.turtle,capture_output=True,text=True,timeout=45,check=False)
        except subprocess.TimeoutExpired:
            raise HTTPException(504,'HermiT exceeded 45 seconds; reduce the ontology size') from None
        if proc.returncode:
            raise HTTPException(422,'OWL DL reasoning failed: '+proc.stderr[-500:])
        try:return json.loads(proc.stdout)
        except ValueError:raise HTTPException(500,'HermiT worker returned an invalid report') from None
    if payload.mode=='owlrl':
        if not OWLRL_AVAILABLE: raise HTTPException(503,'OWL RL reasoning requires: pip install -r backend/requirements.txt')
        if len(g)>2000: raise HTTPException(413,'OWL RL expansion is limited to 2,000 asserted triples')
        try: DeductiveClosure(OWLRL_Semantics).expand(g)
        except Exception as exc: raise HTTPException(422, f'OWL RL error: {str(exc)[:350]}') from None
        if len(g)>50000: raise HTTPException(413,'Expanded graph too large')
    else: g=rdfs_closure(g)
    delta=sorted((tr for tr in g if tr not in original), key=lambda tr:tuple(map(str,tr)))
    result=Graph()
    for tr in delta: result.add(tr)
    return {'mode':payload.mode,'asserted':len(original),'inferred_count':len(delta),'shown':min(len(delta),300),'new_triples':[[display_term(x) for x in tr] for tr in delta[:300]],'inferred_turtle':result.serialize(format='turtle')[:200000]}

@app.post('/api/shacl')
def shacl(payload: ShaclInput):
    if not SHACL_AVAILABLE:
        raise HTTPException(503,'Full SHACL requires: pip install -r backend/requirements.txt')
    data=parse_turtle(payload.turtle)
    shapes=parse_turtle(payload.shapes)
    try:
        conforms, report, summary=shacl_validate(data_graph=data,shacl_graph=shapes,inference='none',advanced=False,js=False,do_owl_imports=False)
        return {'conforms':bool(conforms),'summary':str(summary)[:15000],'report_turtle':report.serialize(format='turtle')[:80000]}
    except Exception as exc: raise HTTPException(422, f'SHACL validation failed: {str(exc)[:350]}') from None

@app.post('/api/dlquery')
def dlquery(payload: DlInput):
    """Named-class instance retrieval supporting A, A and B, A or B; not a Manchester DL reasoner."""
    graph=rdfs_closure(parse_turtle(payload.turtle))
    tokens=re.split(r'\s+(and|or)\s+',payload.expression.strip(),flags=re.I)
    if not tokens or len(tokens)>11: raise HTTPException(422,'Use one to six named classes joined by and / or.')
    if any(t.lower() not in ('and','or') and not re.fullmatch(r'[A-Za-z_][\w-]*|<https?://[^<>\s]+>',t) for t in tokens):
        raise HTTPException(422,'Supported: named classes joined by and / or. Full Manchester DL is not implemented.')
    if any(x.lower() not in ('and','or') for x in tokens[1::2]): raise HTTPException(422,'Only and / or operators supported')
    namespace=next((str(s).rsplit('#',1)[0]+'#' for s,_,_ in graph.triples((None,RDF.type,OWL.Class)) if '#' in str(s)),None)
    if not namespace: namespace=next((str(s).rsplit('#',1)[0]+'#' for s,_,_ in graph.triples((None,RDF.type,RDFS.Class)) if '#' in str(s)),None)
    if not namespace: namespace='https://example.org/tattviki/enterprise#'
    def cls(token):
        return URIRef(token[1:-1] if token.startswith('<') else namespace+token)
    typed=set(graph.subjects(RDF.type,None))
    def members(token): return set(graph.subjects(RDF.type,cls(token)))
    found=members(tokens[0]);expression_parts=[tokens[0]]
    for op,token in zip(tokens[1::2],tokens[2::2]):
        found=(found & members(token)) if op.lower()=='and' else (found | members(token))
        expression_parts.extend([op,token])
    return {'query':' '.join(expression_parts),'matching_instances':sorted(str(x) for x in found)[:MAX_RESULT_ROWS], 'count':len(found),'semantics':'Named-class membership lookup after limited RDFS closure. Not full Manchester DL or OWL2 DL reasoning.'}

# ---- Self-hosted collaboration and immutable revisions, SQLite ----
def db():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    conn=sqlite3.connect(DB_PATH,timeout=10)
    conn.row_factory=sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    conn.executescript('''
CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, username TEXT UNIQUE COLLATE NOCASE NOT NULL, password_hash TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tokens(token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, name TEXT NOT NULL, owner_id TEXT NOT NULL REFERENCES users(id), version INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS members(project_id TEXT NOT NULL REFERENCES projects(id), user_id TEXT NOT NULL REFERENCES users(id), role TEXT NOT NULL CHECK(role IN ('viewer','editor')),PRIMARY KEY(project_id,user_id));
CREATE TABLE IF NOT EXISTS revisions(project_id TEXT NOT NULL REFERENCES projects(id), version INTEGER NOT NULL, editor_id TEXT NOT NULL REFERENCES users(id), document TEXT NOT NULL, message TEXT NOT NULL, created TEXT NOT NULL, PRIMARY KEY(project_id,version));
''')
    try: yield conn
    finally:conn.close()

def timestamp(): return datetime.now(timezone.utc).isoformat()
def password_hash(password):
    salt=secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,300_000)
    return salt.hex()+':'+digest.hex()
def verify(password,encoded):
    try:
        salt,encoded_digest=encoded.split(':')
        calc=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),300_000)
        return hmac.compare_digest(calc,bytes.fromhex(encoded_digest))
    except (ValueError,TypeError):return False

def user_auth(authorization: str | None = Header(default=None),conn:sqlite3.Connection=Depends(db)):
    if not authorization or not authorization.startswith('Bearer '): raise HTTPException(401,'Sign in first')
    token=authorization.removeprefix('Bearer ')
    row=conn.execute('SELECT users.id,users.username FROM tokens JOIN users ON users.id=tokens.user_id WHERE token_hash=?',(hashlib.sha256(token.encode()).hexdigest(),)).fetchone()
    if row is None: raise HTTPException(401,'Invalid session')
    return dict(row)

def make_session(conn,user):
    token=secrets.token_urlsafe(40)
    conn.execute('INSERT INTO tokens VALUES (?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),user['id'],timestamp()))
    conn.commit()
    return {'token':token,'username':user['username']}

@app.post('/api/auth/register',status_code=201)
def register(payload:Credentials,conn:sqlite3.Connection=Depends(db)):
    try:
        user={'id':uuid4().hex,'username':payload.username}
        conn.execute('INSERT INTO users VALUES (?,?,?)',(user['id'],payload.username,password_hash(payload.password)))
        return make_session(conn,user)
    except sqlite3.IntegrityError: raise HTTPException(409,'Username already exists')

@app.post('/api/auth/login')
def login(payload:Credentials,conn:sqlite3.Connection=Depends(db)):
    row=conn.execute('SELECT * FROM users WHERE username=?',(payload.username,)).fetchone()
    if row is None or not verify(payload.password,row['password_hash']): raise HTTPException(401,'Wrong username or password')
    return make_session(conn,row)

@app.post('/api/auth/logout')
def logout(authorization:str|None=Header(default=None),user=Depends(user_auth),conn=Depends(db)):
    conn.execute('DELETE FROM tokens WHERE token_hash=?',(hashlib.sha256(authorization.removeprefix('Bearer ').encode()).hexdigest(),))
    conn.commit()
    return {'logged_out':True}

def role_for(conn,project,user):
    row=conn.execute('SELECT * FROM projects WHERE id=?',(project,)).fetchone()
    if not row: raise HTTPException(404,'Project not found')
    if row['owner_id']==user['id']:return row,'owner'
    member=conn.execute('SELECT role FROM members WHERE project_id=? AND user_id=?',(project,user['id'])).fetchone()
    if not member: raise HTTPException(404,'Project not found')
    return row,member['role']

def validate_document(document):
    raw=json.dumps(document,ensure_ascii=False,allow_nan=False)
    if len(raw.encode())>MAX_PROJECT:raise HTTPException(413,'Ontology project exceeds 1.25 MB')
    if not isinstance(document.get('classes'),list) or not isinstance(document.get('base'),str):
        raise HTTPException(422,'Expected a Tāttvikī ontology project JSON with classes and base')
    return raw

@app.get('/api/projects')
def projects(user=Depends(user_auth),conn=Depends(db)):
    rows=conn.execute('''SELECT p.id,p.name,p.version,CASE WHEN p.owner_id=? THEN 'owner' ELSE m.role END AS role FROM projects p LEFT JOIN members m ON m.project_id=p.id AND m.user_id=? WHERE p.owner_id=? OR m.user_id=? ORDER BY p.name''',(user['id'],)*4).fetchall()
    return {'projects':[dict(row) for row in rows]}

@app.post('/api/projects',status_code=201)
def create_project(payload:ProjectCreate,user=Depends(user_auth),conn=Depends(db)):
    raw=validate_document(payload.document)
    project_id=uuid4().hex
    conn.execute('INSERT INTO projects VALUES (?,?,?,1)',(project_id,payload.name,user['id']))
    conn.execute('INSERT INTO revisions VALUES (?,?,?,?,?,?)',(project_id,1,user['id'],raw,'Created project',timestamp()))
    conn.commit()
    return {'id':project_id,'version':1,'role':'owner'}

@app.get('/api/projects/{project_id}')
def get_project(project_id:str,user=Depends(user_auth),conn=Depends(db)):
    p,role=role_for(conn,project_id,user)
    rev=conn.execute('SELECT * FROM revisions WHERE project_id=? AND version=?',(project_id,p['version'])).fetchone()
    return {'id':p['id'],'name':p['name'],'version':p['version'],'role':role,'document':json.loads(rev['document'])}

@app.put('/api/projects/{project_id}')
def save_project(project_id:str,payload:ProjectSave,user=Depends(user_auth),conn=Depends(db)):
    raw=validate_document(payload.document)
    p,role=role_for(conn,project_id,user)
    if role=='viewer':raise HTTPException(403,'Viewer may not edit')
    if payload.expected_version!=p['version']:raise HTTPException(409,'Outdated revision. Reload the shared project before saving; local unsaved edits are preserved.')
    updated=conn.execute('UPDATE projects SET version=version+1 WHERE id=? AND version=?',(project_id,payload.expected_version))
    if updated.rowcount!=1:raise HTTPException(409,'Another editor saved first')
    v=p['version']+1
    conn.execute('INSERT INTO revisions VALUES (?,?,?,?,?,?)',(project_id,v,user['id'],raw,payload.message,timestamp()))
    conn.commit()
    return {'id':project_id,'version':v}

@app.get('/api/projects/{project_id}/history')
def project_history(project_id:str,user=Depends(user_auth),conn=Depends(db)):
    role_for(conn,project_id,user)
    rows=conn.execute('SELECT r.version,r.message,r.created,u.username AS editor FROM revisions r JOIN users u ON u.id=r.editor_id WHERE r.project_id=? ORDER BY r.version DESC LIMIT 100',(project_id,)).fetchall()
    return {'revisions':[dict(row) for row in rows]}

@app.get('/api/projects/{project_id}/history/{version}')
def project_revision(project_id:str,version:int,user=Depends(user_auth),conn=Depends(db)):
    role_for(conn,project_id,user)
    row=conn.execute('SELECT document,message FROM revisions WHERE project_id=? AND version=?',(project_id,version)).fetchone()
    if not row:raise HTTPException(404,'Revision not found')
    return {'version':version,'message':row['message'],'document':json.loads(row['document'])}

@app.post('/api/projects/{project_id}/restore/{version}')
def restore_project(project_id:str,version:int,payload:RestoreInput,user=Depends(user_auth),conn=Depends(db)):
    _,role=role_for(conn,project_id,user)
    if role=='viewer':raise HTTPException(403,'Viewer may not restore')
    rev=project_revision(project_id,version,user,conn)
    return save_project(project_id,ProjectSave(document=rev['document'],expected_version=payload.expected_version,message=f'Restored revision {version}'),user,conn)

@app.post('/api/projects/{project_id}/members')
def set_member(project_id:str,payload:MemberAdd,user=Depends(user_auth),conn=Depends(db)):
    p,role=role_for(conn,project_id,user)
    if role!='owner':raise HTTPException(403,'Only the project owner can manage permissions')
    target=conn.execute('SELECT id FROM users WHERE username=?',(payload.username,)).fetchone()
    if not target:raise HTTPException(404,'User must register before being invited')
    if target['id']==p['owner_id']:raise HTTPException(422,'Owner role cannot be changed')
    conn.execute('INSERT INTO members(project_id,user_id,role) VALUES (?,?,?) ON CONFLICT(project_id,user_id) DO UPDATE SET role=excluded.role',(project_id,target['id'],payload.role))
    conn.commit()
    return {'username':payload.username,'role':payload.role}

@app.delete('/api/projects/{project_id}/members/{username}')
def revoke_member(project_id:str,username:str,user=Depends(user_auth),conn=Depends(db)):
    _,role=role_for(conn,project_id,user)
    if role!='owner':raise HTTPException(403,'Only the project owner can revoke access')
    target=conn.execute('SELECT id FROM users WHERE username=?',(username,)).fetchone()
    if not target:raise HTTPException(404,'Member not found')
    deleted=conn.execute('DELETE FROM members WHERE project_id=? AND user_id=?',(project_id,target['id']))
    if deleted.rowcount!=1:raise HTTPException(404,'Member not found in this project')
    conn.commit()
    return {'revoked':username}
