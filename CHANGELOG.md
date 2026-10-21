# Changelog

## v8.0.0 — Graph Explorer, ontology starters, guided modeling & midnight UI

- Replaced the class-only hierarchy drawing with an interactive multi-type ontology graph displaying subclass, property domain/range, inverse/superproperty, individuals, object assertions, SKOS, shapes and restrictions.
- Added zoom in/out, wheel zoom, fit-to-graph, pointer drag/pan, focus mode, selection-neighborhood filtering, predicate labels and connected entity inspection.
- Added a safe create-new-ontology dialog, true blank models and large original examples for enterprise, retail, industrial assets and open research.
- Connected lessons to the live model and added five hands-on training cards.
- Applied a coordinated dark slate/midnight theme across navigation, editor, panels and modal controls.
- Retained all v7 features and 613 learning topics; no existing user project is overwritten automatically.
- Added regression tests for new templates, graph controls, RDF parsing and desktop/mobile layouts.
- Continued local-only default. Full OWL 2 DL and publicly hosted collaboration are not claimed.

# Tāttvikī release history

## v7 — 2026-10-21: Semantic Workbench UX review and repair
- Split server-only v6 panel away from the v5 ontology editor into a visually distinct full-size Semantic Workbench.
- Added 4 directly usable workflows on static hosting: project diagnostics, inference preview with explanations, quality review, and relationship inspection.
- Added per-class explorer, real-model statistics and CSV exports, refreshed responsive design and versioned browser assets.
- Preserved full RDFLib SPARQL/OWL RL/pySHACL and versioned collaboration behind an explicit self-hosted engine tab; static GitHub Pages does not provide these server APIs.
- Updated advanced browser regression test to follow new route, and added 10 workbench browser tests.

# Changelog

## v5 — Ontology Studio (October 2026)

- New original in-browser ontology designer for OWL/RDFS classes, object/data properties, individuals, annotations, SKOS vocabulary concepts, selected OWL restrictions, and basic SHACL shapes.
- Interactive class hierarchy, inspector, search, guided quick tour, history, JSON backup/import, and browser-local autosave.
- Three RDF-compatible export formats (Turtle, RDF/XML, JSON-LD) verified to represent the same graph using RDFLib; class diagram export as SVG.
- Synthetic enterprise ontology demo: 25 OWL classes, 512 RDF triples; metadata, lineage, MDM, RDM, policies and data products.
- Standalone ontology demo in `projects/ontology-studio`; RDFLib serialization/lineage tests in the publishing workflow.
- Clear UI explanation of unavailable advanced reasoning, collaborative editing, and full SHACL validation.
- No protected terminology examples, proprietary enterprise data or Protégé assets bundled.


## v4 (2026-10) — UI & offline playground reliability
- Creator shown as **Shubham** in site, licenses and docs.
- Removed restricted terminology named examples in favor of Gene Ontology, OBO principles, Wikidata and invented fixtures.
- Upgraded offline Turtle parser (`,`/`;`, multiple statements, language-tagged literals), SPARQL sorting/paging, three example datasets and TTL export.
- Added lesson search/page navigation and professional responsive redesign, Open data sources page, more robust clipboard fallback.
- Added browser interaction regression tests; full parser via CDN remains network dependent.

# Tāttvikī changelog

## v6 — 21 October 2026

- Added an original advanced ontology workbench beneath the existing visual OWL studio.
- Created optional FastAPI/RDFLib backend with real read-only SPARQL, limited RDFS closure, OWL RL via owlrl, and standard SHACL via pySHACL.
- Added optional unverified Owlready2/HermiT OWL DL classification adapter with Java prerequisite and 45-second worker timeout.
- Added explicitly limited named-class DL-style instance queries.
- Added SQLite team projects, hashed authentication tokens, PBKDF2 passwords, owner/editor/viewer authorization, invitations and revocations, optimistic-save conflict checks, immutable revision history and restoration.
- Added 11 API tests and 14 browser integration checks; previous 613-topic course and 512-triple enterprise ontology unchanged.
- Backend stays separate from GitHub Pages; comprehensive production hardening is still required before public server hosting.


## v3 — 18 October 2026

- Rebranded complete learning suite consistently as Tāttvikī with project creator Shubham credited in public UI and license notices.
- Expanded lessons to 613 distinct titles/IDs, including 360 enterprise-specific topics organized across 15 modules.
- Added learning paths for metadata, master data management, reference data management, semantic architecture, enterprise integration, engineering, governance, data products, industry and GraphRAG.
- Created 12 original industry blueprints, each connecting source data, MDM, RDM, ontology, metadata, risk and acceptance criteria.
- Added an interactive browser-local MDM identity candidate scoring demonstration, SKOS RDM code crosswalk tester and lineage example.
- Added separate executable synthetic CRM–ERP–RDM–catalog–PROV–SHACL enterprise capstone with input CSVs, generator, real SPARQL queries and unit tests.
- Published a preliminary copyright, terminology-license, privacy and trademark risk checklist. No definitive trademark/legal clearance claimed.
- Expanded GitHub Pages CI with full semantic lab execution and content uniqueness checks.

## v2

- 253 distinct topics and enterprise KG lab with 1,014 triples.

## v1

- Initial open education website, learning paths and basic in-browser RDF/SPARQL lab.
