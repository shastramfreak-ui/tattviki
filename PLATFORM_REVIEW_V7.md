# Tāttvikī v7 — design and functional review

## What went wrong in v6

1. The new "Reason. Validate. Collaborate." functionality was added after the entire v5 ontology editor. Users naturally saw the old editor first, so the update looked nearly identical.
2. The advanced tools mostly required a separate Python backend that is not deployed by GitHub Pages. There was no immediately functional advanced analysis page for public learners.
3. New API features were proven by tests, but their discoverability and public hosting constraints were not adequately checked before release.
4. The older Ontology Studio still presented a "not yet built" comparison panel even though optional server features existed; the wording was corrected.

## What v7 changes

- Dedicated **#semantic** route visible in primary navigation, plus a large homepage launcher.
- Separate dashboard with live model counts, browser mode status, clear actions and four capability tiles.
- Real browser RDFS-subset inference with per-triple explanation; preview recalculates from the current ontology.
- Functional browser quality preview, class and assertion inspectors, filtered relationship view and CSV reports.
- Server-powered SPARQL, OWL RL, pySHACL, DL-style search and collaboration live under a distinct "Full semantic engine" tab, not hidden below the editor.
- Asset cache-busting so deployed UI changes are less likely to be masked by cached scripts/styles.

## Important, honest limitations

- Browser inference derives **named class types** using subclass, domain, range and subproperty schema, but is not a full RDFS closure, RDFLib engine, OWL RL materializer, or OWL 2 DL reasoner.
- Browser quality checks only a documented subset of constraints on explicit types; not SHACL Core conformance.
- The browser relationship inspector shows explicit assertions; it is not a complete graph traversal / SPARQL service.
- The optional experimental HermiT integration has not been end-to-end execution-tested; Java, OWLReady2 and appropriate dependencies are needed.
- Shared accounts, server-side snapshots and permissions are **self-hosted**: a static website cannot securely persist shared projects by itself.
- Do not expose the dev FastAPI backend publicly without further authentication, security hardening, HTTPS, rate limits, quotas and backup strategy.
- Browser test screenshots use local packaged scripts and cannot prove an external GitHub Pages deployment is current; verify Actions and hard-refresh after pushing.

## Repeatable verification

```
node scripts/check_content.cjs
node scripts/test_ui_render.cjs
python scripts/test_semantic_workbench.py
python scripts/test_browser.py
python scripts/test_studio.py
python -m unittest -v backend.tests.test_api
python scripts/test_advanced_browser.py
```

The browser suite requires Playwright and Chromium. GitHub's published workflow checks content and sample RDF exports; it does **not** run every graphical browser test in Actions.
