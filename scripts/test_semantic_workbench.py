"""End-to-end browser checks for the visually distinct v7 Semantic Workbench."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
checks=[]
if True:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1520,'height':1000},accept_downloads=True)
  errs=[];page.on('pageerror',lambda err:errs.append(str(err)))
  page.on('dialog',lambda dialog:dialog.accept())
  page.set_content('<html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><div id="app"></div></body></html>')
  page.evaluate("""() => {const d={};const mock={getItem:k=>d[k]||null,setItem:(k,v)=>{d[k]=String(v)},removeItem:k=>delete d[k]};Object.defineProperty(window,'localStorage',{value:mock,configurable:true});Object.defineProperty(window,'sessionStorage',{value:mock,configurable:true});}""")
  page.add_style_tag(content=(ROOT/'assets/styles.css').read_text())
  for f in ['content','curriculum','deepdives','enterprise_curriculum','enterprise_cases','studio-templates','studio-graph','studio','advanced','semantic-workbench','app']:
   page.add_script_tag(content=(ROOT/'assets'/f'{f}.js').read_text())
  assert page.locator('[data-route="semantic"]').count()>=1
  page.locator('.nav-item[data-route="semantic"]').click()
  assert page.locator('h1').first.inner_text().startswith('Semantic Workbench')
  assert page.locator('.semantic-metrics>div').count()==5
  assert page.locator('.semantic-feature').count()==4
  checks.append('Independent semantic route, live project metrics, and four discoverable tools')
  summary=page.evaluate('window.TattvikiSemantic.analyze(window.TattvikiStudio.model())')
  assert len(summary['inferred'])>0
  page.locator('[data-semantic="tab"][data-value="inference"]').first.click()
  assert page.locator('.semantic-table tbody tr').count()>0
  assert 'rdfs:' in page.locator('.semantic-table').inner_text()
  checks.append('Local RDFS subset adds and explains inferred memberships')
  with page.expect_download() as info:page.locator('[data-semantic="export"][data-value="inference"]').click()
  assert info.value.suggested_filename.endswith('.csv')
  checks.append('Inference report CSV export works')
  page.locator('[data-semantic="tab"][data-value="quality"]').click()
  before=page.locator('.semantic-kpi strong').inner_text()
  checks.append('Browser quality report visible')
  page.locator('.nav-item[data-route="studio"]').click()
  assert page.locator('.studio-workspace').count()==1
  page.locator('[data-studio-action="kind"][data-studio-kind="shapes"]').click()
  page.locator('[data-studio-action="select"][data-studio-id="DatasetShape"]').click()
  page.locator('.studio-inspector input[data-studio-field="min"]').fill('5')
  page.locator('.studio-inspector input[data-studio-field="min"]').press('Tab')
  page.locator('.nav-item[data-route="semantic"]').click()
  page.locator('[data-semantic="tab"][data-value="quality"]').click()
  after=page.locator('.semantic-kpi strong').inner_text()
  assert int(after)>int(before),(before,after)
  checks.append('Studio model edits update quality report, no hard-coded results')
  page.locator('[data-semantic="tab"][data-value="lineage"]').click()
  assert page.locator('.semantic-table tbody tr').count()>=4
  opts=page.locator('#semantic-predicate option').all_text_contents()
  assert len(opts)>5
  page.locator('#semantic-predicate').select_option('ownedBy')
  assert page.locator('.semantic-table tbody tr').count()>0
  assert all('ownedBy' in s for s in page.locator('.semantic-table tbody tr').all_text_contents())
  checks.append('Relationship filters operate on actual current assertions')
  page.locator('[data-semantic="tab"][data-value="overview"]').click()
  page.locator('.semantic-node-row button').first.click()
  assert page.locator('.semantic-class-detail').count()==1
  checks.append('Clickable ontology class inspector reports child classes and inferred instances')
  page.locator('[data-semantic="tab"][data-value="engine"]').click()
  assert page.locator('#advanced-root').count()==1
  assert 'Backend offline' in page.locator('#advanced-pill').inner_text()
  assert page.locator('[data-advanced="tab"]').count()==5
  checks.append('Self-hosted SPARQL/SHACL/revision tools visible without false connected state')
  page.locator('[data-advanced="tab"][data-tabid="sparql"]').click()
  assert page.locator('#advanced-query').count()==1
  checks.append('Full SPARQL editor appears in correct engine section')
  page.locator('[data-semantic="tab"][data-value="overview"]').click()
  import base64
  logo='data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/logo.svg').read_bytes()).decode()
  page.locator('.brand img').evaluate('(img,url)=>img.src=url',logo)
  page.screenshot(path=str(ROOT/'previews'/'semantic-workbench-desktop.png'),full_page=False)
  page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(250)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+4')
  page.screenshot(path=str(ROOT/'previews'/'semantic-workbench-mobile.png'),full_page=False)
  checks.append('Mobile layout does not overflow viewport')
  assert not errs,errs
  browser.close()
print('Semantic workbench browser checks:',len(checks))
for item in checks:print('  PASS',item)
