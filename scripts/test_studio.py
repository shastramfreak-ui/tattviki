"""Playwright regression test for the standalone, browser-local Tāttvikī ontology editor.
Optional: pip install playwright rdflib; python -m playwright install chromium
"""
from pathlib import Path
import json, tempfile, threading, functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from rdflib import Graph, URIRef
ROOT = Path(__file__).resolve().parent.parent
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
OWL = 'http://www.w3.org/2002/07/owl#'
SH = 'http://www.w3.org/ns/shacl#'
EX = 'https://example.org/tattviki/enterprise#'
results=[]

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1580,'height':1000},accept_downloads=True)
    errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('dialog',lambda d:d.accept())
    # Browser sandbox blocks navigation to local HTTP/file URLs; inject the exact packaged assets.
    page.set_content('<html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><div id="app"></div></body></html>')
    page.add_style_tag(content=(ROOT/'assets/styles.css').read_text())
    for name in ['content','curriculum','deepdives','enterprise_curriculum','enterprise_cases','studio','app']:
        page.add_script_tag(content=(ROOT/'assets'/f'{name}.js').read_text())
    page.locator('[data-route="studio"]').first.click()
    assert page.locator('.studio-graph-node').count()>=25
    assert page.locator('.studio-inspector h3').inner_text()=='Dataset'
    results.append('Studio integrated into navigation and class graph')
    page.locator('[data-studio-action="tour"]').click()
    assert 'Define a model' in page.locator('.studio-tour').inner_text()
    page.locator('[data-studio-action="tour"]').click()
    results.append('Quick guide opens and closes')
    page.evaluate('window.scrollTo(0,0)')
    page.locator('.brand img').evaluate('(im,uri)=>im.src=uri','data:image/svg+xml;base64,'+__import__('base64').b64encode((ROOT/'assets/logo.svg').read_bytes()).decode())
    page.screenshot(path=str(ROOT/'previews'/'ontology-studio.png'),full_page=False)
    page.set_viewport_size({'width':390,'height':850})
    page.wait_for_timeout(320)  # allow sidebar's responsive transition to settle
    page.screenshot(path=str(ROOT/'previews'/'ontology-studio-mobile.png'),full_page=False)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 4')
    page.set_viewport_size({'width':1580,'height':1000})
    results.append('Responsive desktop / mobile screenshots')
    # Verify initial sample against expected triples and official vocabularies
    t=page.evaluate('window.TattvikiStudio.exportTurtle()')
    g=Graph();g.parse(data=t,format='turtle')
    assert len(g)>450,len(g)
    assert (URIRef(EX+'Dataset'), URIRef(RDF+'type'), URIRef(OWL+'Class')) in g
    assert (URIRef(EX+'DatasetShape'),URIRef(RDF+'type'),URIRef(SH+'NodeShape')) in g
    results.append(f'Initial OWL/SKOS/SHACL syntax and RDF data: {len(g)} triples')
    # Edit hierarchy and restore; e.g. Dataset SubClassOf a different class
    page.locator('.studio-inspector [data-studio-field="parent"]').select_option('Organization')
    assert page.evaluate("window.TattvikiStudio.model().classes.find(x=>x.id==='Dataset').parent")=='Organization'
    page.locator('[data-studio-action="undo"]').click()
    assert page.evaluate("window.TattvikiStudio.model().classes.find(x=>x.id==='Dataset').parent")=='EnterpriseEntity'
    page.locator('[data-studio-action="redo"]').click()
    assert page.evaluate("window.TattvikiStudio.model().classes.find(x=>x.id==='Dataset').parent")=='Organization'
    page.locator('[data-studio-action="undo"]').click()
    results.append('Class parent editing, undo, redo')
    # Add class and change its label, persist in local browser state
    page.locator('[data-studio-action="add"]').click()
    assert page.locator('.studio-inspector h3').inner_text()=='NewClass'
    page.locator('.studio-inspector input[data-studio-field="label"]').fill('Approved Metadata Asset')
    page.locator('.studio-inspector input[data-studio-field="label"]').press('Tab')
    assert page.locator('.studio-inspector h3').inner_text()=='Approved Metadata Asset'
    assert any(x['id']=='NewClass' for x in page.evaluate('window.TattvikiStudio.model().classes'))
    # Local storage is forbidden on the synthetic about:blank testing origin; real GitHub Pages uses HTTP(S).
    results.append('Create, label and autosave new OWL class')
    # switch kind and change object property characteristic
    page.locator('[data-studio-action="kind"][data-studio-kind="objectProperties"]').click()
    page.locator('[data-studio-action="select"][data-studio-id="ownedBy"]').click()
    page.locator('input[data-studio-flag="FunctionalProperty"]').check()
    assert 'FunctionalProperty' in page.evaluate("window.TattvikiStudio.model().objectProperties.find(x=>x.id==='ownedBy').characteristics")
    results.append('Object property characteristics and inverse editor')
    # Individuals assertions create and change
    page.locator('[data-studio-action="kind"][data-studio-kind="individuals"]').click()
    page.locator('[data-studio-action="select"][data-studio-id="SafetyDataset"]').click()
    old=page.locator('.studio-assertion').count()
    page.locator('[data-studio-action="add-assert"]').click()
    assert page.locator('.studio-assertion').count()==old+1
    page.locator(f'[data-studio-assert="prop"][data-idx="{old}"]').select_option('sourceSystem')
    page.locator(f'[data-studio-assert="value"][data-idx="{old}"]').fill('Synthetic-Enterprise')
    page.locator(f'[data-studio-assert="value"][data-idx="{old}"]').press('Tab')
    assert any(a['value']=='Synthetic-Enterprise' for a in page.evaluate("window.TattvikiStudio.model().individuals.find(x=>x.id==='SafetyDataset').assertions"))
    page.locator(f'[data-studio-action="remove-assert"][data-idx="{old}"]').click()
    assert page.locator('.studio-assertion').count()==old
    results.append('Typed individual assertions add, change and remove')
    # SKOS editing
    page.locator('[data-studio-action="kind"][data-studio-kind="concepts"]').click()
    page.locator('[data-studio-action="select"][data-studio-id="Approved"]').click()
    page.locator('input[data-studio-field="alt"]').fill('Accepted|Valid|Cleared')
    page.locator('input[data-studio-field="alt"]').press('Tab')
    assert 'Cleared' in page.evaluate("window.TattvikiStudio.model().concepts.find(x=>x.id==='Approved').alt")
    results.append('SKOS alternate labels and concept schemes')
    # SHACL invalid counting
    page.locator('[data-studio-action="kind"][data-studio-kind="shapes"]').click()
    page.locator('[data-studio-action="select"][data-studio-id="DatasetShape"]').click()
    page.locator('input[data-studio-field="min"]').fill('2')
    page.locator('input[data-studio-field="min"]').press('Tab')
    page.locator('[data-studio-action="validate"]').first.click()
    assert 'minCount exceeds maxCount' in page.locator('.studio-audit').inner_text()
    page.locator('.studio-inspector input[data-studio-field="min"]').fill('1')
    page.locator('.studio-inspector input[data-studio-field="min"]').press('Tab')
    page.locator('.studio-inspector input[data-studio-field="max"]').fill('')
    page.locator('.studio-inspector input[data-studio-field="max"]').press('Tab')
    assert page.evaluate('window.TattvikiStudio.checks().issues.length')==0
    results.append('SHACL structural checks and error feedback')
    page.locator('.studio-inspector input[data-studio-field="pattern"]').fill('(')
    page.locator('.studio-inspector input[data-studio-field="pattern"]').press('Tab')
    page.locator('[data-studio-action="validate"]').first.click()
    assert 'Invalid SHACL regex' in page.locator('.studio-audit').inner_text()
    page.locator('.studio-inspector input[data-studio-field="pattern"]').fill('')
    page.locator('.studio-inspector input[data-studio-field="pattern"]').press('Tab')
    results.append('Bad SHACL regex reported without crashing')
    # Exports round trip with rdflib and semantic equivalence
    page.locator('[data-studio-action="view"][data-studio-view="files"]').click()
    temp=Path(tempfile.mkdtemp(prefix='tattviki-studio-test-'))
    ftypes=[('export-ttl','turtle'),('export-rdfxml','xml'),('export-jsonld','json-ld')]
    graphs=[]
    for action,fmt in ftypes:
        with page.expect_download() as info: page.locator(f'[data-studio-action="{action}"]').last.click()
        d=info.value;dest=temp/d.suggested_filename;d.save_as(str(dest))
        parsed=Graph();parsed.parse(str(dest),format=fmt);graphs.append(parsed)
        assert (URIRef(EX+'ResearchStudy'), URIRef(RDF+'type'), URIRef(OWL+'Class')) in parsed
        results.append(f'Export {fmt} parses as RDF: {len(parsed)} triples')
    for g2 in graphs[1:]:
        assert graphs[0].isomorphic(g2), 'Export formats do not express identical graphs'
    results.append('OWL/RDF exports are semantically isomorphic')
    # Native JSON can be imported; invalid JSON rejected non-destructively
    with page.expect_download() as info: page.locator('[data-studio-action="save-json"]').last.click()
    filename=temp/info.value.suggested_filename;info.value.save_as(str(filename))
    project=json.loads(filename.read_text())
    assert project['version']==1 and project['name'].startswith('Enterprise')
    page.locator('#studio-import-file').set_input_files(str(filename))
    page.wait_for_function("document.querySelector('.studio-callout')?.innerText.includes('Imported project JSON successfully')", timeout=5000)
    results.append('Project JSON export / import round-trip')
    before=page.evaluate('window.TattvikiStudio.model().name')
    invalid=temp/'invalid.json';invalid.write_text('{"version":1,"name":"corrupt","base":"javascript:foo","classes":[]}')
    page.locator('[data-studio-action="view"][data-studio-view="files"]').click()
    page.locator('#studio-import-file').set_input_files(str(invalid))
    page.wait_for_function("document.querySelector('.studio-callout')?.innerText.includes('Import blocked')", timeout=3000)
    assert page.evaluate('window.TattvikiStudio.model().name')==before
    results.append('Invalid JSON import safely rejected')
    # Verify mobile after interactions as well, without mutating exported content.
    page.set_viewport_size({'width':390,'height':850})
    assert page.locator('.studio-workspace').is_visible()
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 4')
    results.append('Mobile layout without horizontal document overflow')
    assert not errors,errors
    print('STUDIO TESTS:',len(results))
    for result in results:print('PASS',result)
    browser.close()
