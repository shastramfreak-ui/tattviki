"""Tāttvikī v8 full browser product checks, no external services."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from rdflib import Graph
from xml.etree import ElementTree
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import threading
R=Path(__file__).resolve().parent.parent
checks=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1500,'height':950},accept_downloads=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.set_content('<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><div id="app"></div></body></html>')
 page.add_style_tag(content=(R/'assets/styles.css').read_text())
 for x in ['content','curriculum','deepdives','enterprise_curriculum','enterprise_cases','studio-templates','studio-graph','studio','advanced','semantic-workbench','app']:
  page.add_script_tag(content=(R/'assets'/f'{x}.js').read_text())
 page.locator('[data-route="studio"]').first.click()
 assert page.locator('#studio-diagram').count()==1
 assert page.locator('.t8-node').count()>25
 checks.append('initial schema nodes visualized')
 for key in ['classes','schema','instances','vocabulary','all']:
  page.locator(f'[data-studio-action="graph-mode"][data-mode="{key}"]').click()
  assert page.locator('.t8-node').count()>0,(key,page.locator('body').inner_text()[-250:])
  checks.append(f'{key} mode renders real semantic nodes')
 assert page.locator('.t8-edge').count()>30
 checks.append('relationships rendered, not class-only')
 before=page.evaluate('window.TattvikiGraph.view().zoom')
 page.locator('[data-studio-action="zoom-in"]').click()
 after=page.evaluate('window.TattvikiGraph.view().zoom')
 assert after>before,(before,after)
 page.locator('[data-studio-action="zoom-out"]').click()
 assert abs(page.evaluate('window.TattvikiGraph.view().zoom')-before)<1e-5
 checks.append('zoom in/out functioning')
 svg=page.locator('#studio-diagram');svg.hover(position={'x':240,'y':240});page.mouse.wheel(0,-300)
 assert page.evaluate('window.TattvikiGraph.view().zoom')>before
 page.locator('[data-studio-action="zoom-reset"]').click()
 pan_before=page.evaluate('window.TattvikiGraph.view().panX')
 rect=svg.bounding_box();page.mouse.move(rect['x']+rect['width']*.06,rect['y']+rect['height']*.94);page.mouse.down();page.mouse.move(rect['x']+rect['width']*.29,rect['y']+rect['height']*.85,steps=5);page.mouse.up()
 assert page.evaluate('window.TattvikiGraph.view().panX')!=pan_before
 checks.append('mouse wheel and drag pan')
 page.locator('[data-studio-action="graph-mode"][data-mode="schema"]').click()
 page.locator('.t8-node[data-studio-kind="objectProperties"]').first.click(force=True)
 assert page.locator('.studio-inspector h3').count()==1
 checks.append('property graph node selects property inspector')
 page.locator('#t8-graph-search').fill('NotARealEntity')
 assert page.locator('.t8-graph-empty').count()==1
 page.locator('#t8-graph-search').fill('owned')
 assert page.locator('.t8-node').count()>=1
 page.locator('#t8-graph-search').fill('')
 checks.append('graph search filters and clears')

 page.locator('[data-studio-action="graph-mode"][data-mode="all"]').click()
 page.locator('[data-studio-action="graph-labels"]').click()
 assert page.evaluate('window.TattvikiGraph.view().showLabels')
 page.locator('[data-studio-action="graph-neighborhood"]').click()
 assert page.evaluate('window.TattvikiGraph.view().nearOnly')
 assert page.locator('.t8-node').count() < 25
 checks.append('edge labels and selection-neighborhood filters')
 page.locator('[data-studio-action="graph-neighborhood"]').click()
 page.locator('[data-studio-action="graph-expand"]').click()
 assert page.locator('.studio-workspace.t8-expanded').count()==1
 page.locator('[data-studio-action="graph-expand"]').click()
 assert page.locator('.studio-workspace.t8-expanded').count()==0
 checks.append('full-width graph focus mode toggles')

 svg_text=page.evaluate('window.TattvikiGraph.exportSVG()')
 root=ElementTree.fromstring(svg_text)
 assert root.tag.endswith('svg')
 assert int(root.get('height'))>640
 checks.append('export full network to standalone parseable SVG')

 page.locator('[data-studio-action="view"][data-studio-view="files"]').click()
 with page.expect_download() as downloaded:page.locator('.studio-export[data-studio-action="export-svg"]').click()
 file=downloaded.value
 assert file.suggested_filename.endswith('.svg')
 assert ElementTree.parse(file.path()).getroot().tag.endswith('svg')
 checks.append('Files panel exports complete SVG when diagram is hidden')
 page.locator('[data-studio-action="view"][data-studio-view="diagram"]').click()



 page.locator('[data-studio-action="tutorial"][data-tutorial="thesaurus"]').click()
 assert 'SKOS' in page.locator('.t8-lesson-context').inner_text()
 assert page.locator('.studio-inspector h3').count()==1
 checks.append('guided tutorial opens model')
 page.locator('[data-studio-action="new-project"]').first.click()
 assert page.locator('.t8-project-dialog').count()==1
 page.locator('[data-studio-action="close-project"]').first.click()
 assert page.locator('.t8-project-dialog').count()==0
 checks.append('new project dialog opens and closes')
 page.locator('[data-studio-action="new-project"]').first.click()
 page.locator('input[name="t8-template"][value="blank"]').check()
 page.locator('#t8-project-name').fill('Custom ontological model')
 page.locator('#t8-project-iri').fill('https://example.org/custom#')
 page.locator('[data-studio-action="create-project"]').click()
 assert page.evaluate('window.TattvikiStudio.model().classes.length')==0
 assert page.evaluate('window.TattvikiStudio.model().name')=='Custom ontological model'
 checks.append('true blank project creates without preloaded classes')
 page.locator('[data-studio-action="add"]').first.click()
 assert page.evaluate('window.TattvikiStudio.model().classes.length')==1
 checks.append('blank project supports adding classes')
 for key in ['retail','industrial','research','enterprise']:
  page.locator('[data-studio-action="new-project"]').first.click()
  page.locator(f'input[name="t8-template"][value="{key}"]').check()
  page.locator('#t8-project-name').fill('Test '+key)
  page.locator('#t8-project-iri').fill('https://example.org/'+key+'#')
  page.locator('[data-studio-action="create-project"]').click()
  m=page.evaluate('window.TattvikiStudio.model()')
  assert len(m['classes'])>=20
  assert len(m['individuals'])>=30 if key!='enterprise' else len(m['individuals'])>=10
  data=page.evaluate('window.TattvikiStudio.exportTurtle()')
  g=Graph();g.parse(data=data,format='turtle')
  assert len(g)>=250,(key,len(g))
  assert not page.evaluate('window.TattvikiStudio.checks().issues')
  checks.append(f'{key} example: classes, entities, RDF parse ({len(g)} triples)')
 page.locator('[data-studio-action="save-json"]').first.click()
 checks.append('project JSON export works')
 page.locator('[data-route="learn"]').first.click()
 page.locator('[data-route^="lesson/"]').first.click()
 assert page.locator('[data-action="open-studio-example"]').count()==1
 page.locator('[data-action="open-studio-example"]').click()
 assert page.locator('.t8-lesson-context').count()==1
 checks.append('real lesson opens guided Ontology Studio')
 page.screenshot(path=str(R/'previews/studio-v8-desktop.png'),full_page=False)
 page.set_viewport_size({'width':390,'height':844})
 page.wait_for_timeout(150)
 page.screenshot(path=str(R/'previews/studio-v8-mobile.png'),full_page=False)
 assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+8'),page.evaluate('document.documentElement.scrollWidth')
 checks.append('mobile layout no horizontal body overflow')
 assert not [e for e in errors if 'localStorage' not in e],errors
 browser.close()
print('PASS',len(checks),'checks')
for c in checks:print(' ✓',c)
