from playwright.sync_api import sync_playwright
from pathlib import Path
import tempfile
root=Path(__file__).resolve().parent.parent
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,headless=True,args=['--no-sandbox'])
 def setup(width=1440,height=950):
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,accept_downloads=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content('<html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><div id="app"></div></body></html>')
  page.add_style_tag(content=(root/'assets/styles.css').read_text())
  for f in ['content','curriculum','deepdives','enterprise_curriculum','enterprise_cases','studio','app']:
   page.add_script_tag(content=(root/'assets'/f'{f}.js').read_text())
  return page,errors
 pg,errors=setup()
 def goto(route,needle):
  pg.locator(f'.nav-item[data-route="{route}"]').click()
  assert needle in pg.locator('body').inner_text(),(route,pg.locator('body').inner_text()[:200]);results.append('Route '+route)
 for path,expect in [('studio','Ontology Studio'),('learn','Your path to graph expertise'),('enterprise','12 implementation blueprints'),('workbench','MDM × RDM × metadata workbench'),('tools','Tool explorer'),('methods','Methodologies'),('updates','Latest updates'),('glossary','Glossary'),('publishing','Legal, licensing'),('about','Shubham'),('datasets','Explore openly reusable sources'),('project','Build a knowledge graph'),('playground','Play with real graph ideas'),('home','Make data meaningful')]:
  try:goto(path,expect)
  except Exception as e:print('FAIL route',path,str(e)[:200]);raise
 import base64
 pg.locator('.brand img').evaluate('(im,uri)=>im.src=uri', 'data:image/svg+xml;base64,'+base64.b64encode((root/'assets/logo.svg').read_bytes()).decode())
 pg.screenshot(path=str(Path(tempfile.gettempdir())/'Tattviki_v4_desktop.png'),full_page=False)
 goto('learn','613 focused topics')
 pg.locator('#learningSearch').fill('crosswalk')
 assert 'matching topics' in pg.locator('body').inner_text()
 assert pg.locator('.line-item').count()>0
 assert pg.locator('.line-item').count()<=24
 results.append('Search learning library')
 pg.locator('#learningSearch').fill('')
 assert pg.locator('.line-item').count()==24,pg.locator('.line-item').count()
 pg.locator('[data-learnpage="1"]').click()
 assert 'page 2 of' in pg.locator('.filter-counter').inner_text()
 results.append('Lesson paging')
 # learning filters route after search
 pg.locator('.line-item').first.click()
 assert pg.locator('.quiz-option').count()==3
 # click correct answer via browser data from course
 lessonid=pg.evaluate('location.hash.slice(8)')
 ans=pg.evaluate('(id)=>window.OT.lessons.find(l=>l.id===id)?.quiz?.answer',lessonid)
 pg.locator(f'[data-action="quiz"][data-answer="{ans}"]').click()
 pg.locator('[data-action="complete"]').click()
 assert 'Completed' in pg.locator('body').inner_text()
 results.append('Quiz completion')
 goto('playground','Play with real graph ideas')
 for i in range(3):
  pg.locator(f'[data-challenge="{i}"]').click()
  pg.locator('[data-action="run-query"]').click()
  t=pg.locator('.result-body').inner_text()
  assert 'Query completed' in t,(i,t)
  expected=[3,2,2][i]
  assert f'{expected} results' in t,(i,t)
  results.append(f'Challenge {i} expected {expected}')
 # sample load enterprise with a semicolon and comma
 pg.locator('[data-dataset="catalog"]').click()
 pg.locator('[data-action="run-query"]').click()
 assert '2 results' in pg.locator('.result-body').inner_text(),pg.locator('.result-body').inner_text()
 results.append('Enterprise catalog load + SPARQL')
 pg.locator('[data-tab="turtle"]').first.click()
 pg.locator('[data-action="check-turtle"]').click()
 assert 'syntax accepted' in pg.locator('.result-body').inner_text().lower(),pg.locator('.result-body').inner_text()
 results.append('Turtle shorthand validation')
 pg.locator('#codeEditor').fill('@prefix ex: <https://example.org/> .\nex:Person a ex:Class .\nex:Asha ex:knows ex:Ravi, ex:Mira ; ex:age 24 .')
 pg.locator('[data-action="check-turtle"]').click()
 assert '4 triples' in pg.locator('.result-body').inner_text(),pg.locator('.result-body').inner_text()
 results.append('Turtle object lists and typed integer')
 pg.locator('[data-tab="graph"]').first.click()
 assert pg.locator('.graph-node').count()>=3
 pg.locator('.graph-node').first.click()
 assert 'SELECTED NODE' in pg.locator('.graph-inspect').inner_text()
 results.append('Graph interaction')
 pg.locator('[data-tab="sparql"]').first.click()
 pg.locator('#codeEditor').fill('PREFIX ex: <https://example.org/>\nSELECT ?p WHERE {\n ?p a ex:Class .\n} LIMIT 1')
 pg.locator('[data-action="run-query"]').click()
 assert '1 result' in pg.locator('.result-body').inner_text(),pg.locator('.result-body').inner_text()
 results.append('Custom SELECT')
 # advanced offset and order
 pg.locator('[data-action="load-dataset"][data-dataset="learners"]').click()
 pg.locator('#codeEditor').fill('PREFIX ex: <https://example.org/>\nSELECT ?p WHERE {\n ?p ex:enrolledIn ?c .\n} ORDER BY DESC(?p) LIMIT 1 OFFSET 1')
 pg.locator('[data-action="run-query"]').click()
 assert '1 result' in pg.locator('.result-body').inner_text(),pg.locator('.result-body').inner_text()
 results.append('SPARQL ORDER + LIMIT + OFFSET')
 with pg.expect_download() as d:
  pg.locator('[data-action="download-rdf"]').click()
 assert d.value.suggested_filename=='tattviki-graph.ttl'
 results.append('RDF download')
 pg.locator('.brand img').evaluate('(im,uri)=>im.src=uri', 'data:image/svg+xml;base64,'+base64.b64encode((root/'assets/logo.svg').read_bytes()).decode())
 pg.screenshot(path=str(Path(tempfile.gettempdir())/'Tattviki_v4_playground.png'),full_page=False)
 goto('workbench','MDM × RDM × metadata workbench')
 pg.locator('#sourceSystem').select_option('ERP');pg.locator('#localCode').fill('S')
 pg.locator('[data-action="map-code"]').click()
 assert 'SUSPENDED' in pg.locator('#rdmResult').inner_text()
 pg.locator('#localCode').fill('NOT_A_CODE');pg.locator('[data-action="map-code"]').click()
 assert 'QUARANTINE' in pg.locator('#rdmResult').inner_text()
 pg.locator('#matchThreshold').fill('0.91');pg.locator('#matchThreshold').dispatch_event('input')
 assert '91%' in pg.locator('body').inner_text()
 results.append('RDM mappings and MDM threshold')
 pg.locator('[data-action="search-open"]').click()
 pg.locator('#globalSearch').fill('SPARQL')
 assert pg.locator('.search-result').count()>0
 pg.keyboard.press('Escape')
 assert pg.locator('.search-modal').count()==0
 results.append('Global search, escape')
 assert not errors, errors
 print('DESKTOP PASSES',len(results));print('\n'.join('PASS '+r for r in results))
 m,me=setup(width=390,height=844)
 assert m.locator('.mobile-toggle').is_visible()
 m.locator('.mobile-toggle').click()
 assert 'open' in m.locator('.sidebar').get_attribute('class')
 m.locator('[data-route="playground"]').first.click()
 assert 'Play with real graph ideas' in m.locator('body').inner_text()
 m.locator('.brand img').evaluate('(im,uri)=>im.src=uri', 'data:image/svg+xml;base64,'+base64.b64encode((root/'assets/logo.svg').read_bytes()).decode())
 m.screenshot(path=str(Path(tempfile.gettempdir())/'Tattviki_v4_mobile.png'),full_page=False)
 assert not me,me
 print('PASS Mobile navigation / responsive view')
 browser.close()
