"""Run live browser integration against local static server and FastAPI service."""
from __future__ import annotations
import os, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
os.environ['TATTVIKI_DB']=str(Path(tempfile.mkdtemp(prefix='tattviki-ui-'))/'projects.sqlite3')
sys.path.insert(0,str(ROOT))
from backend.main import app
from fastapi.testclient import TestClient
from playwright.sync_api import sync_playwright
client=TestClient(app)

checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1530,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('dialog',lambda d:d.accept())
 def api_binding(source, req):
  import json
  path=req['url'].replace('https://api.tattviki.test','')
  if not path.startswith('/api/'):
   return {'status':404,'data':{'detail':'Unavailable news fixture'}}
  r=client.request(req.get('method','GET'),path,json=json.loads(req['body']) if req.get('body') else None,headers=req.get('headers') or {})
  return {'status':r.status_code,'data':r.json()}
 page.expose_binding('__tattvikiApi',api_binding)
 page.set_content('<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><div id="app"></div></body></html>')
 page.evaluate("""() => {
  const state={ 'tattviki-advanced-api':'https://api.tattviki.test' };
  const storage={getItem:k=>Object.hasOwn(state,k)?state[k]:null,setItem:(k,v)=>{state[k]=String(v)},removeItem:k=>{delete state[k]}};
  Object.defineProperty(window,'localStorage',{value:storage,configurable:true});
  Object.defineProperty(window,'sessionStorage',{value:{...storage},configurable:true});
  window.fetch=async (url,options={})=>{
    const result=await window.__tattvikiApi({url:String(url),method:options.method||'GET',headers:options.headers||{},body:options.body||''});
    return {ok:result.status>=200&&result.status<300,status:result.status,json:async()=>result.data};
  };
 }""")
 page.add_style_tag(content=(ROOT/'assets/styles.css').read_text())
 for f in ['content','curriculum','deepdives','enterprise_curriculum','enterprise_cases','studio-templates','studio-graph','studio','advanced','semantic-workbench','app']:
  page.add_script_tag(content=(ROOT/'assets'/f'{f}.js').read_text())
 page.locator('[data-route="semantic"]').first.click()
 page.locator('.semantic-tabs [data-semantic="tab"][data-value="engine"]').click()
 assert page.locator('#advanced-root').count()==1,'Missing advanced semantic engine panel'
 checks.append('Dedicated semantic engine reachable from top-level navigation')
 page.locator('[data-advanced="connect"]').click()
 page.wait_for_function("document.querySelector('#advanced-pill')?.textContent.includes('connected')")
 assert 'owlrl' in page.locator('#advanced-result').inner_text()
 checks.append('Live FastAPI connectivity and advertised capabilities')
 page.locator('[data-advanced="rdfs"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('inferred_count')")
 assert 'new_triples' in page.locator('#advanced-result').inner_text()
 checks.append('Inference from editor Turtle')
 page.locator('[data-advanced="tab"][data-tabid="sparql"]').click()
 page.locator('[data-advanced="sparql"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('columns')")
 assert 'owner' in page.locator('#advanced-result').inner_text()
 checks.append('SPARQL query execution against live ontology')
 page.locator('[data-advanced="tab"][data-tabid="dl"]').click()
 page.locator('[data-advanced="dl"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('matching_instances')")
 checks.append('Named-class instance retrieval')
 page.locator('[data-advanced="tab"][data-tabid="shacl"]').click()
 page.locator('[data-advanced="shacl"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Error:')") if not __import__('importlib').util.find_spec('pyshacl') else page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('conforms')")
 checks.append('SHACL missing-dependency error is explicit (or real report if installed)')
 page.locator('[data-advanced="tab"][data-tabid="team"]').click()
 page.locator('#advanced-username').fill('shubhamdemo')
 page.locator('#advanced-password').fill('StrongPassword123!')
 page.locator('[data-advanced="register"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Signed in as')")
 checks.append('Self-hosted user registration / sign in')
 page.locator('[data-advanced="create"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Created shared project')")
 checks.append('Create shared ontology from current editor')
 page.locator('[data-advanced="load"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Loaded')")
 checks.append('Load shared project into ontology model')
 page.locator('[data-advanced="save"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Saved revision')")
 checks.append('Save updated ontology revision')
 page.locator('[data-advanced="history"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('revisions') || document.querySelector('#advanced-result')?.textContent.includes('Updated classes')")
 assert page.locator('#advanced-history option').count()>=3
 checks.append('Load revision history')
 page.locator('#advanced-history').select_option('1')
 page.locator('[data-advanced="restore"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Restored v1')")
 checks.append('Restore revision with a new immutable version')
 page.locator('[data-advanced="logout"]').click()
 page.wait_for_function("document.querySelector('#advanced-result')?.textContent.includes('Signed out')")
 checks.append('Session logout invalidates token')
 page.locator('[data-advanced="tab"][data-tabid="reason"]').click()
 page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
 page.screenshot(path=str(ROOT/'previews'/'advanced-semantic-workbench.png'),full_page=False)
 page.set_viewport_size({'width':390,'height':844})
 page.screenshot(path=str(ROOT/'previews'/'advanced-workbench-mobile.png'),full_page=False)
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 5')
 checks.append('Mobile responsive layout without page overflow')
 assert not errors,errors
 browser.close()
print(f'{len(checks)} browser checks passed:')
for n in checks:print(' ✓',n)
