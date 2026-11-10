from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,time
root=Path(__file__).resolve().parents[1]
SCRIPTS=['content','curriculum','deepdives','enterprise_curriculum','learning-guides','ai-curriculum','graph-learning','shacl-learning','editorial-patches','shacl-scenarios','shacl-lab','graph-examples','enterprise_cases','studio-templates','studio-graph','studio','advanced','semantic-workbench','ai-lab','graph-lab','app']
CSS=['styles.css','theme-v9.css','learning-v10.css','ai-lab.css','graph-lab.css','shacl-lab.css']
def load(page,route='shacl'):
 page.set_content('<!doctype html><html><head><meta name="theme-color" content="#101827"></head><body><div id="app"></div></body></html>')
 page.evaluate('''()=>{const store={};Object.defineProperty(window,"localStorage",{configurable:true,value:{getItem:k=>store[k]??null,setItem:(k,v)=>store[k]=String(v),removeItem:k=>delete store[k]}});Object.defineProperty(window,"sessionStorage",{configurable:true,value:{getItem:k=>store[k]??null,setItem:(k,v)=>store[k]=String(v)}})}''')
 page.evaluate('(r)=>location.hash="#"+r',route)
 for f in CSS:page.add_style_tag(content=(root/'assets'/f).read_text(encoding='utf-8'))
 for f in SCRIPTS:page.add_script_tag(content=(root/'assets'/(f+'.js')).read_text(encoding='utf-8'))
def go(page,route):
 page.evaluate('(r)=>location.hash="#"+r',route)
 page.wait_for_timeout(70)
checks=[]
def ok(name,test):
 if not test: raise AssertionError(name)
 checks.append(name);print('PASS',name,flush=True)
try:
 time.sleep(.1)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  ctx=browser.new_context(viewport={'width':1440,'height':900},accept_downloads=True)
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  load(page);page.wait_for_timeout(200)
  ok('SHACL route appears',page.get_by_text('SHACL Validation Lab',exact=True).count()>0)
  ok('six scenarios present',page.locator('#shacl-scenario option').count()==6)
  ok('editors exist',page.locator('#shacl-data').count()==1 and page.locator('#shacl-shapes').count()==1)
  page.locator('[data-shacl="run"]').click()
  ok('initial bad graph fails',page.locator('.shacl-status.is-warning').count()==1)
  ok('violations list populated',page.locator('.shacl-issues article').count()>=2)
  page.locator('[data-shacl="good"]').click();page.locator('[data-shacl="run"]').click()
  ok('good fixture conforms',page.locator('.shacl-status.is-success').count()==1)
  page.select_option('#shacl-scenario',value='1')
  ok('scenario switch updates title',page.get_by_text('Catalog datasets require a title',exact=False).count()>0)
  page.locator('[data-shacl="run"]').click();ok('catalog bad fails',page.locator('.shacl-issues article').count()>=2)
  page.locator('#shacl-shapes').fill(page.locator('#shacl-shapes').input_value().replace('sh:in ( ex:Public ex:Internal ex:Restricted )','sh:in ( ex:Secret )'))
  page.locator('[data-shacl="run"]').click();ok('edited shape updates report',page.locator('.shacl-issues article').count()>=2)
  page.locator('[data-shacl="good"]').click();page.locator('[data-shacl="run"]').click();ok('catalog repaired graph passes',page.locator('.shacl-status.is-success').count()==1)
  with page.expect_download() as download:page.locator('[data-shacl="download-shapes"]').click()
  ok('shapes download works',download.value.suggested_filename.endswith('.ttl'))
  page.screenshot(path=str(root/'previews/v13-shacl-dark.png'),full_page=True)
  page.locator('[data-action="theme-toggle"]').first.click();ok('light theme applied',page.locator('html[data-theme="light"]').count()==1)
  page.screenshot(path=str(root/'previews/v13-shacl-light.png'),full_page=True)
  go(page,'learn')
  ok('737 indexed lessons',page.get_by_text('737',exact=False).count()>0)
  go(page,'lesson/shacl-06')
  ok('new SHACL detailed lesson',page.get_by_text('Require and limit values with minCount and maxCount',exact=False).count()>0 and page.locator('.chapter-section').count()==5)
  ok('SHACL lesson action links to lab',page.locator('[data-route="shacl"]').count()>0)
  page.locator('.quiz [data-action="quiz"]').first.click();
  go(page,'studio')
  ok('original Ontology Studio still renders',page.get_by_text('Ontology Studio',exact=False).count()>0)
  go(page,'graphlab')
  ok('Graph Theory Lab still renders',page.get_by_text('Graph Theory Lab',exact=False).count()>0)
  go(page,'retrieval')
  ok('Retrieval lab still renders',page.get_by_text('Retrieval Systems Lab',exact=False).count()>0)
  if errors: print('BROWSER ERRORS:',errors)
  ok('no JS runtime errors',len(errors)==0)
  mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
  mob=mobile.new_page();load(mob);mob.wait_for_timeout(100)
  ok('mobile editors visible',mob.locator('#shacl-data').count()==1)
  mob.screenshot(path=str(root/'previews/v13-shacl-mobile.png'),full_page=True)
  mobile.close();browser.close()
 print('V13 BROWSER CHECKS',len(checks))
finally:pass
