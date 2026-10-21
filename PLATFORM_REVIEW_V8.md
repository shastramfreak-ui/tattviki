# Tāttvikī v8 — Product review and acceptance checks

## Scope
A browser-local ontology editor enhancement. The network visualization displays authored relationships for OWL classes, object/data properties, typed individuals and object assertions, SKOS concepts, SHACL and selected restrictions. It is not a complete reasoning engine or arbitrary graph database browser.

## Functional acceptance
- Five graph modes and seven categories of semantic entities.
- Zoom buttons, wheel zoom, fit-to-graph and pointer dragging; zoom state stored in current editor session.
- Full-width focus mode, direct-neighbor filter, edge-label toggle and entity search.
- Node selection opens the existing structured inspector; edits affect future graph renders and RDF outputs.
- Blank new ontology project with name and namespace; sample starter projects (all synthetic).
- Guided tutorial cards and learning page → Studio navigation.
- No new web API keys, tracking services or proprietary controlled vocabularies.

## Checks
Run `python scripts/test_v8_product.py` for the 24 v8 browser product checks. Run `python scripts/test_studio.py` and the older regression tests. `node scripts/test_ui_render.cjs`, `node scripts/check_content.cjs`, `node scripts/export_studio_demo.cjs` and `python scripts/check_studio_exports.py` verify the static rendering, curriculum and RDF examples.

Some browser tests inject local packaged assets rather than navigating to a hosted origin because this build environment blocks HTTP navigation. They test interactive JavaScript, DOM and RDF behavior but do not prove production deployment or browser storage persistence on GitHub Pages. Run deployment smoke tests after publishing.

## Limitations
Graph layout is a deterministic semantic category layout; very large models can require zooming/panning and graph filtering. The browser graph caps rendering at 260 selected entities to stay responsive. Native project JSON is the only full visual-editor import format. Full OWL 2 DL and backend-powered features remain optional and separately hosted. Mobile and dark-theme checks are best-effort; a professional WCAG accessibility audit remains advisable.
