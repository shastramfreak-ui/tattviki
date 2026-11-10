<div align="center">

# Tāttvikī

### Learn ontology engineering. Build knowledge graphs. Explore enterprise semantics.

**A free, open-source learning platform and hands-on semantic engineering workspace.**

[**Website**](https://shastramfreak-ui.github.io/tattviki/) · [**Ontology Studio**](https://shastramfreak-ui.github.io/tattviki/#studio) · [**Semantic Workbench**](https://shastramfreak-ui.github.io/tattviki/#semantic) · [**Curriculum**](CURRICULUM.md) · [**Contribute**](CONTRIBUTING.md)

**Version 13** · **737 learning topics** · **30 new SHACL units** · **12 graph datasets** · **12 enterprise use-case blueprints**

**Created by Shubham**

</div>

![Tāttvikī v9 interactive semantic overview](previews/v9-overview-dark.png)

**[Open the live Studio](https://shastramfreak-ui.github.io/tattviki/#studio)** · [Create a new ontology](https://shastramfreak-ui.github.io/tattviki/#studio) · [View the project templates](previews/studio-v8-new-ontology.png)

> **Deployment note:** The website links above refer to this repository's expected GitHub Pages address. The site is available there only after a successful GitHub Pages deployment.

## New in v13 — SHACL Validation from first shape to production quality gate

**[Open the SHACL Validation Lab](https://shastramfreak-ui.github.io/tattviki/#shacl)** · **[Read 30-lesson SHACL path](CURRICULUM.md#v13--shacl-from-zero-to-production-30-lessons)** · **[SHACL hands-on guide](SHACL_VALIDATION_GUIDE.md)** · **[Python validator & examples](projects/shacl-validation-lab/README.md)**

A new beginner-to-advanced learning path provides **30 individually authored SHACL study chapters** covering node/property shapes, targeting, cardinality, datatypes, class checks, allowed values, numeric bounds, validation reports, inference choices, SPARQL constraints, pySHACL, Apache Jena, GraphDB, and production quality gates.

The browser SHACL Lab contains **six synthetic enterprise scenarios**, each with editable SHACL shapes and passing/failing RDF data. It evaluates a **documented SHACL Core subset** and shows individual constraint results. Download the same Turtle files and reproduce validation in pySHACL or Apache Jena using the included capstone. The full engines do **not** run on GitHub Pages without separate services.

**Repetitive lesson-content audit:** v13 replaces several prominent stock introduction, example and verification templates while retaining all older lesson IDs and saved progress. See [content-review findings](CONTENT_REVIEW_V13.md) and [machine audit](CONTENT_AUDIT_V13.json). This is a structural improvement, not proof that every legacy chapter is entirely non-repetitive.

![SHACL Validation Lab](previews/v13-shacl-dark.png)

## Previous v12 — Graph theory, algorithms, CAG and a consolidated Studio

The standalone **Playground** has been consolidated into the **Ontology Studio Code Lab** (`#studio/code`). RDF/Turtle editing, beginner SPARQL, graph inspection and challenge exercises are retained; the old `#playground` route remains compatible. You can import the **current Studio ontology's Turtle export** into Code Lab. Full OWL/SPARQL/SHACL capabilities still require the optional local backend.

**[Open the new Graph Theory Lab](https://shastramfreak-ui.github.io/tattviki/#graphlab)** for 12 original fictional enterprise/industry networks, **360 nodes and 616 directed relationships**. Compute BFS, Dijkstra, weak components, degree centrality, unweighted PageRank, and topological/cycle checks. Switch between radial, grid and swimlane views; pan, zoom, select, inspect and export.

**42 distinct new lessons** in four learning paths teach graph mathematics, algorithms, graph governance and CAG/CRAG, bringing the total to **707**. The new lessons explain algorithms, graph identity, provenance, graph-RAG patterns and why Cache-Augmented Generation is not the same as Corrective RAG.

[**Read the v12 field guide**](GRAPH_THEORY_AND_CAG_GUIDE.md) · [**Explore the 12 graph datasets**](data/graph_examples.json) · [**Graph algorithms source code**](assets/graph-lab.js)

![Graph Theory Lab](previews/v12-graph-theory-dark.png)

## Previous v11 — AI retrieval, vectors, GraphRAG and context graphs

**52 new distinct advanced lessons** in six dedicated paths: Vector Foundations, Retrieval & RAG, GraphRAG Engineering, Context Graphs & Memory, Agentic Knowledge Systems, and Enterprise AI Architecture.

Every new lesson includes an original technical explanation, an enterprise scenario, explicit failure conditions, a design or executable code example, verification exercises, a topic-specific knowledge check, and links to primary references. Some chapters include additional deep technical explanations. The material is structured for study, but it is **not a replacement for full specialist textbooks or the official documentation**.

**[Launch the browser Retrieval Systems Lab](https://shastramfreak-ui.github.io/tattviki/#retrieval)** — run BM25, a transparent TF-IDF/cosine vector proxy, hybrid reciprocal-rank fusion, and a typed graph-expansion simulation over 28 fictional documents. Compare six questions, three access roles and retrieval metrics. The proxy is **not a neural embedding** and the lab does **not call an LLM or external service**.

**[Run the offline Python lab](projects/enterprise-retrieval-rag/README.md)** — zero API keys, no external dataset downloads. It supports core search algorithms, role-aware visibility, graph traversal and unit tests. Start here if you want reproducible implementation practice.

**[Read the 2026 industry field guide](AI_LANDSCAPE_2026.md)** — compare which retrieval architecture fits each question, plus the role of context graphs and agents.

**[Browse the advanced AI syllabus](AI_CURRICULUM.md)** — definitions, limitations and authoritative technical sources (Microsoft GraphRAG, Neo4j GraphRAG, Azure AI Search, Anthropic contextual retrieval, W3C PROV).

![AI Retrieval Systems Lab](previews/v11-retrieval-dark.png)

## Previous v10 improvements — detailed chapters and progress fixes

Every learning topic now opens a multi-section chapter containing **concept explanations, worked enterprise scenarios, example RDF/SPARQL, tradeoffs, acceptance tests, reflection questions and a knowledge check**. The previous 665 topics and existing visual ontology studio remain available, alongside 42 new study units.

**Progress fix:** answering a quiz correctly immediately marks its lesson complete. The homepage and learning-path dashboard both update; completion and quiz results are saved in the current browser. In Learning Paths you can export a JSON progress backup and restore it later (including on another device).

**Important:** the previous releases only saved a completed lesson when you separately clicked “Mark lesson complete”. Old *unsaved* correct quiz answers cannot be recovered. Already saved completions are preserved. Different site origins such as `localhost`, local files, and the GitHub Pages URL have independent browser storage.

Chapters are larger and more instructional than the previous short summaries; specialist depth still varies. See [Learning content guide and editorial limitations](LEARNING_CONTENT_GUIDE.md) for standards policy, limitations and how to contribute deeper content.

![Expanded v10 chapter](previews/v10-deep-lesson.png)

## Table of contents

- [What is Tāttvikī?](#what-is-tāttvikī)
- [Features and capabilities](#features-and-capabilities)
- [SHACL validation course and full-tool lab](#new-in-v13--shacl-validation-from-first-shape-to-production-quality-gate)
- [Learning-content guide](LEARNING_CONTENT_GUIDE.md)
- [Content review and repetition audit](CONTENT_REVIEW_V13.md)
- [Advanced AI / GraphRAG curriculum](AI_CURRICULUM.md)
- [Graph Theory Lab and consolidated Code Lab](#new-in-v12--graph-theory-algorithms-cag-and-a-consolidated-studio)
- [Retrieval Systems Lab](#retrieval-systems-lab)
- [Explore the learning paths](#explore-the-learning-paths)
- [Get started locally](#get-started-locally)
- [Visual Ontology Studio v9](#visual-ontology-studio-v9)
- [Semantic Workbench](#semantic-workbench)
- [Enterprise projects](#enterprise-projects)
- [Optional advanced backend](#optional-advanced-backend)
- [Deploy to GitHub Pages](#deploy-to-github-pages)
- [Project structure](#project-structure)
- [Tests and quality checks](#tests-and-quality-checks)
- [Privacy, licenses, and responsible use](#privacy-licenses-and-responsible-use)
- [Contributing](#contributing)

## What is Tāttvikī?

**Tāttvikī** makes ontology development, knowledge graphs, and enterprise semantic technologies approachable through guided lessons, editable examples, visual modeling, and executable projects.

It brings together:

- **Foundations:** data and information modeling, vocabularies, taxonomies, thesauri, RDF, RDFS, OWL, SKOS, SPARQL, and SHACL.
- **Ontology engineering:** classes, properties, individuals, axioms, annotations, class hierarchies, model quality, and RDF exports.
- **Enterprise semantics:** metadata catalogs, data lineage, master data management (MDM), reference data management (RDM), governance, integration, and knowledge-graph pipelines.
- **Advanced topics:** reasoning, GraphRAG, semantic interoperability, data products, architecture patterns, and domain-focused implementations.

The **707 entries** consist of foundational lessons, concise micro-lessons, and enterprise topic briefs. They are *not* all full textbook-length chapters. See [CURRICULUM.md](CURRICULUM.md) and [the searchable topic index](CURRICULUM_INDEX.csv).

## Features and capabilities

| Capability | Free browser experience | Optional local backend |
| --- | --- | --- |
| Lessons, quizzes, searchable glossary and progress | ✅ | Not required |
| Studio Code Lab (Turtle, beginner SPARQL, RDF preview) | ✅ Teaching subset | Not required |
| Visual OWL/RDF ontology modeling | ✅ Interactive graph, five layouts, zoom/pan, node dragging, focus | Not required |
| New blank ontology and multi-domain project starters | ✅ | Not required |
| Class/property/individual/SKOS/SHACL graph views | ✅ | Not required |
| Guided lessons linked directly to Studio | ✅ | Not required |
| Classes, properties, individuals, SKOS concepts and selected axioms | ✅ | Not required |
| Turtle, RDF/XML, JSON-LD and diagram export | ✅ | Not required |
| Browser RDFS inference preview and explained findings | ✅ Supported subset | Not required |
| Relationship inspection and structural quality diagnostics | ✅ Supported subset | Not required |
| Graph Theory Lab (12 networks, six graph algorithms) | ✅ Independently checked against NetworkX | Not required |
| General SPARQL execution on an ontology | — | ✅ RDFLib, read-only |
| OWL RL inference and SHACL Core validation | — | ✅ `owlrl` and `pySHACL` |
| Shared projects, access roles and version history | — | ✅ SQLite-backed API |
| Experimental OWL DL classification | — | ⚠️ Optional Java/HermiT adapter |

**Scope matters:** the browser parser, SPARQL practice interpreter, inference preview, and quality checks are educational subsets—not complete implementations of their underlying standards. The local backend supports more advanced features but is **not a production-ready public service**. Full Protégé/WebProtégé feature parity is not claimed.

### The Semantic Workbench

![Semantic Workbench desktop view](previews/semantic-workbench-desktop.png)

In **Semantic Workbench** (`#semantic`), analyze the ontology currently open in the Studio:

- View inferred class memberships and their explanations.
- Inspect explicit relationships and browse classes.
- Run browser-side structural/quality diagnostics.
- Export displayed findings as CSV.
- Switch to the **Full semantic engine** when a separately running backend is available.

The browser-only analysis works on GitHub Pages; the advanced engine and shared revisions do not run on GitHub Pages itself.

## Retrieval Systems Lab

Open `#retrieval` to compare search methods over the same original, synthetic enterprise corpus. Try the role selector: the viewer sees public evidence, while engineers and stewards have different authorized views. Then switch between lexical retrieval, transparent TF-IDF/cosine, RRF and graph expansion. The lab reports a bounded, labelled synthetic evaluation and prints the source evidence rather than generating an unsupported answer.

**Production guidance:** Actual neural embedding generation, approximate nearest-neighbor indexes, LLM-based synthesis, Microsoft GraphRAG indexing, comprehensive safety controls and real enterprise access management all require additional components and independent validation. This free GitHub Pages lab is educational only.

Run `python projects/enterprise-retrieval-rag/retrieval_lab.py --mode hybrid` from the project root to reproduce the Python example. Run the tests from the project folder with `python -m unittest -v test_retrieval.py`.

## Explore the learning paths

| Area | Example subjects |
| --- | --- |
| Semantic foundations | Knowledge representation, identifiers, controlled vocabularies, thesauri |
| RDF and linked data | IRIs, triples, graphs, Turtle, JSON-LD, RDF datasets |
| Ontology modeling | RDFS, OWL classes, properties, constraints, design patterns |
| SKOS and reference data | Concepts, labels, hierarchies, mapping, terminology governance |
| Query and validation | SPARQL, SHACL, competency questions, data-quality checks |
| Knowledge-graph engineering | ETL/ELT, graph construction, integration, lineage, entity resolution |
| Enterprise data management | Metadata, MDM, RDM, master records, cataloging, data contracts |
| Governance and operations | Versioning, stewardship, interoperability, FAIR, change management |
| Advanced and applied topics | Reasoning, graph algorithms, GraphRAG, industry use cases |
| Vector foundations | Embeddings, cosine similarity, sparse/dense retrieval, ANN, HNSW, evaluation |
| Retrieval & RAG | BM25, hybrid RRF, contextual retrieval, reranking, citation verification |
| GraphRAG engineering | Multi-hop, local/global/DRIFT search, communities, entity resolution |
| Context graphs & agents | Temporal context, decisions, agent memory, tool routing, provenance |
| Enterprise AI architecture | Permission-aware retrieval, metadata lineage, index refresh, latency, tests |

Browse all subjects using the **Lessons** section of the website, [CURRICULUM.md](CURRICULUM.md), or [CURRICULUM_INDEX.csv](CURRICULUM_INDEX.csv).

## Get started locally

The main website has **no Node.js build step, account requirement, or paid API dependency**. You only need a modern browser and a small local web server.

### Windows — easiest method

1. Download or clone the repository.
2. Make sure **Python 3** is installed.
3. Double-click [`START_WINDOWS.bat`](START_WINDOWS.bat) from the project root.
4. Open **http://localhost:8000/** if the browser does not open automatically.

Close the server terminal to stop the site.

### Windows, macOS, or Linux — manual method

From the project root:

```bash
python -m http.server 8000
```

Then open **http://localhost:8000/**. Depending on your installation, you may need `python3` or (on Windows) `py -3` instead of `python`.

> Opening `index.html` with `file://` can prevent the updates JSON from loading because browsers restrict local file access. Using a local HTTP server is recommended.


### v9 — Five graph layouts and dual appearance

The Studio includes **five interactive layouts**: **Overview** (grouped semantic domains), **Radial** (type-centered relationships), **Organic** (deterministic spring-network), **Hierarchy** (parent/child levels), and **Swimlanes** (separate entity kinds). The Overview layout initially summarizes every entity category rather than shrinking all entities into a tall column; click any group to explore it.

Use **Focus / Balanced / Expanded / Maximum** density levels in detailed layouts, or switch to **Neighbors** to inspect immediate relationships. The graph supports mouse-wheel zoom, click-to-fit, pointer dragging to pan, node repositioning, and two-finger pinch gestures. The **Focus** button makes the canvas wider, while node selection opens the editable ontology inspector. SVG export captures the currently displayed graph layout and camera view.

Use the **Light mode / Dark mode** button in the top navigation to change the appearance of the *entire* learning website. The choice is stored locally in the browser (no login required).

| Dark mode | Light mode |
| --- | --- |
| ![Midnight Studio overview](previews/v9-overview-dark.png) | ![Light Studio overview](previews/v9-overview-light.png) |

> Large ontology layouts use progressive display limits (45, 80, 150 or 240 visible entities) for browser performance. This is a visual display limit, **not an RDF export or ontology-model limit**. The current node positions in a graph layout are presentation-only; drag positions are not saved as ontology axioms.

## Visual Ontology Studio v9

Open **http://localhost:8000/#studio**. Version 8 adds a genuine multi-relationship SVG graph viewer rather than displaying only the class tree.

![Graph explorer, schema view](previews/v9-overview-dark.png)

The graph shows `rdfs:subClassOf`, class equivalence/disjointness, `rdfs:domain` and `rdfs:range`, `rdfs:subPropertyOf`, `owl:inverseOf`, individual `rdf:type` and object assertions, SKOS broader/scheme links, and SHACL target/path and selected restriction links. Toggle among **Class hierarchy**, **Schema & axioms**, **Individuals**, **SKOS**, and **Everything**. Colored node categories indicate OWL classes, object properties, data properties, individuals, SKOS terms, SHACL shapes and OWL restrictions.

Use **+ / −** or the mouse wheel to zoom, **Fit** to fit the complete filtered graph, and **drag** to pan. **Focus** expands the canvas to the full work area. **Neighbors** isolates the selected entity and its directly linked nodes; **Edge labels** reveals property/predicate names. Search filters entities and their connections. Click a node to edit its details in the inspector. All of this works on static GitHub Pages; no server is needed.

### Create an ontology from scratch

Select **+ New ontology** in the Studio toolbar. Choose **Blank ontology**, enter a title and an HTTP(S) base namespace, and confirm. Blank projects start with zero classes, properties and individuals. Then add classes, relationships, individual assertions, SKOS terms and governance shapes using the sidebar. Export your work as editable project JSON or RDF formats. Projects are stored **locally in the current browser**; export a backup before switching templates or changing devices.

### Large original example ontologies

| New project template | Purpose | Typical generated size |
| --- | --- | ---: |
| **Enterprise 360** | Metadata catalog, MDM, RDM, stewardship, lineage and research | 512 RDF triples |
| **Retail 360 & Supply Chain** | Product/customer/order integration, fulfillment and data products | 824 RDF triples |
| **Industrial Asset Digital Twin** | Equipment/sensors, observations, maintenance and governed telemetry | 680 RDF triples |
| **Open Research Data Integration** | Samples, experiments, FAIR catalogs, provenance and releases | 722 RDF triples |
| **Blank ontology** | Start your own domain or industry model | Empty model |

These generated samples are fictional teaching datasets (not licensed medical terminology or real company data). Counts describe the included example versions; they change when you edit a project.

### Guided training is connected to the editor

On any supported learning page, select **Open in Ontology Studio** to load a guided editing context. The Studio also provides five built-in practice cards covering subclass structures, object properties, individuals/assertions, SKOS vocabularies, and validation. The exercises use the currently open ontology; they do not silently overwrite a learner's project.

The authoring editor supports classes, properties, individuals, selected OWL axioms/restrictions, SKOS, local quality checks, undo/redo, JSON backup/import, and exports in Turtle, RDF/XML, JSON-LD and SVG.

**Known limitations:** The diagram shows explicitly modeled relationships, not a complete logical entailment closure; arbitrary RDF-to-editable-model import, full OWL 2 DL reasoning, advanced SHACL and live team collaboration are not available in the browser-only Studio. Select the optional backend for further semantic processing. This project is independent of Protégé and WebProtégé.

## Semantic Workbench

Open **http://localhost:8000/#semantic** to inspect the current ontology's supported inferred memberships, quality findings and lineage/relationship summaries. The browser-side inference is a *documented subset* of RDFS rather than full OWL 2 DL reasoning. Full RDFLib SPARQL, `owlrl` and `pySHACL` require the separate backend; GitHub Pages does not execute Python services.

For a concrete reference implementation, see [projects/ontology-studio](projects/ontology-studio/README.md), using an original fictional 25-class / 512-triple enterprise ontology.

## Enterprise projects

| Project | What you will implement |
| --- | --- |
| [Study KG](projects/study-kg/README.md) | Introductory RDF modeling, SPARQL and SHACL shapes |
| [Enterprise KG](projects/enterprise-kg/README.md) | Synthetic multi-domain knowledge graph (1,014 triples), queries and validation |
| [Enterprise MDM / RDM / Metadata](projects/enterprise-mdm-rdm-metadata/README.md) | Consolidate fictional CRM/ERP data; SKOS code mapping; DCAT metadata; PROV lineage; SPARQL; SHACL; tests |
| [Ontology Studio example](projects/ontology-studio/README.md) | Model and export an enterprise ontology, run sample queries, import an editable native project |

### Run the enterprise MDM / RDM / metadata capstone

From the repository root:

```bash
cd projects/enterprise-mdm-rdm-metadata
python -m pip install -r requirements.txt
python generate.py
python run_queries.py
python -m unittest -v test_lab.py
```

Optional negative test (intentionally generates a SHACL violation):

```bash
python generate.py --break-shape
```

This final command is intended to demonstrate validation failure. `pySHACL` is needed for full SHACL execution; an unavailable dependency must not be interpreted as a successful validation.

## Optional advanced backend

The **Full semantic engine** tab connects to a separate Python/FastAPI service for advanced SPARQL, OWL RL, SHACL, and revisioned projects.

**Windows setup:** Open two terminal windows from the project root.

**Terminal 1 — website:**

```powershell
py -3 -m http.server 8000
```

**Terminal 2 — semantic backend:**

```powershell
py -m pip install -r backend/requirements.txt
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

Alternatively, use `START_WINDOWS.bat` and `backend/START_ADVANCED_WINDOWS.bat`.

Visit **http://localhost:8000/#semantic**, open the **Full semantic engine** tab, and connect to **http://127.0.0.1:8765**. The FastAPI documentation is available at **http://127.0.0.1:8765/docs**.

For dependency details, local project storage, permissions, limits, HermiT prerequisites and security guidance, read [backend/README.md](backend/README.md).

> **Security:** this backend is for local or trusted development. Do not expose the unmodified development server or its SQLite account database to the public internet. A real public multi-user deployment requires separate secure hosting, HTTPS, authentication hardening, resource controls, backups and privacy protections.

## Deploy to GitHub Pages

Only the static website is published by GitHub Pages. Python services, server-side reasoning, and shared project accounts must be hosted separately.

1. Push the **contents of this project folder** to the root of a public GitHub repository named `tattviki` (do not upload the ZIP as a single file).
2. Open **Settings → Pages** and choose **GitHub Actions** as the build/deployment source.
3. Check the **Actions** tab for the `Publish Tāttvikī and refresh tool releases` workflow.
4. After a successful run, visit `https://<your-username>.github.io/tattviki/`.

This repository already includes [`.github/workflows/pages.yml`](.github/workflows/pages.yml), which publishes on pushes to `main`, supports manual runs, and schedules a refresh of selected software-release **metadata**. It does not automatically rewrite course material or guarantee real-time news.

### Update the existing Tāttvikī repository

If you are editing a previously cloned copy, keep the hidden `.git` directory intact. After replacing or updating files, run:

```powershell
git add -A
git commit -m "Update Tattviki documentation and website"
git push origin main
```

For this specific repository, the expected website URL is **https://shastramfreak-ui.github.io/tattviki/** after GitHub Pages deployment succeeds.

## Project structure

```text
Tattviki/
├── index.html                     # Static application entry point
├── assets/                        # UI, curriculum, Studio and Workbench JS/CSS
├── data/                          # Curated standards and release metadata
├── projects/                      # Hands-on RDF/ontology/enterprise projects
│   ├── study-kg/
│   ├── enterprise-kg/
│   ├── enterprise-mdm-rdm-metadata/
│   └── ontology-studio/
├── backend/                       # Optional FastAPI/SQLite semantic service
├── scripts/                       # Content, export and regression checks
├── previews/                      # Desktop/mobile screenshots
├── .github/workflows/pages.yml    # Automated GitHub Pages deployment
├── CURRICULUM.md                  # Learning pathway overview
├── CURRICULUM_INDEX.csv           # Searchable/exportable lesson list
├── CONTRIBUTING.md                # Contribution guidelines
├── LEGAL_AND_DATA_REVIEW.md       # Publication and licensing review
├── LICENSE                        # MIT source-code license
├── CONTENT-LICENSE.md             # CC BY 4.0 original learning content
└── START_WINDOWS.bat              # Local static-server launcher
```

## Tests and quality checks

| Check | Command |
| --- | --- |
| Curriculum integrity (707 entries) | `node scripts/check_content.cjs` and `node scripts/check_v12_graph.cjs` |
| Page/route rendering | `node scripts/test_ui_render.cjs` |
| Browser interactions | `python scripts/test_browser.py` |
| Ontology Studio regression tests | `python scripts/test_studio.py` |
| **v8 Graph/project/user-flow tests** | `python scripts/test_v8_product.py` |
| Semantic Workbench interactions | `python scripts/test_semantic_workbench.py` |
| Advanced browser/API integration | `python scripts/test_advanced_browser.py` |
| Semantic API unit tests | `python -m unittest -v backend.tests.test_api` |
| RDF-format interoperability | `node scripts/export_studio_demo.cjs` then `python scripts/check_studio_exports.py` |

Browser test scripts require **Playwright and Chromium**; RDF-related checks may require RDFLib and the dependencies documented in the project-specific README files.

```bash
python -m pip install playwright
python -m playwright install chromium
```

The v8 release was tested for core site behavior, editor interactions, semantic-workbench interactions, API routes and RDF export compatibility. These local checks do not replace public deployment testing, accessibility audits, or security review. Optional Java/HermiT reasoning was **not** execution-verified in the build environment.

## Privacy, licenses, and responsible use

- **Creator credit:** Shubham.
- **Code:** [MIT License](LICENSE).
- **Original learning content and educational examples:** [CC BY 4.0](CONTENT-LICENSE.md).
- **Examples:** synthetic/fictional; no real employer or client data is intended for distribution.
- **External ontologies, standards and tools:** follow their own licenses and attribution requirements. Merely being publicly accessible does not mean material can be redistributed.
- **Browser-only experience:** model drafts and learning progress are stored in the local browser. Optional self-hosted account and project data are stored by the backend on the server running it.
- **Brand and publication:** the name *Tāttvikī* should receive trademark clearance before broader commercial branding. See [LEGAL_AND_DATA_REVIEW.md](LEGAL_AND_DATA_REVIEW.md) for the preliminary audit (not a legal opinion).

The interface is an independent educational project and is **not affiliated with Protégé or WebProtégé**.

## Contributing

Contributions are welcome in the form of corrections, runnable tutorials, ontology patterns, synthetic example datasets, quality tests, and well-sourced tool updates. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and [GitHub Issues](https://github.com/shastramfreak-ui/tattviki/issues) for proposed improvements.

Please avoid uploading confidential enterprise schemas, personal information, proprietary vocabulary exports, or third-party material you do not have permission to redistribute.

---

<div align="center">

**Tāttvikī** · Open learning for the semantic web and enterprise knowledge graphs  
**Created by Shubham**

</div>

### v9 visual checks

Run `python scripts/test_v9_graph.py` after installing Playwright and its Chromium browser. The suite exercises all five layouts, domain drill-down, mousewheel zoom, pan, node movement, density controls, site-wide theme switching, RDF export, and mobile layout. See [`PLATFORM_REVIEW_V9.md`](PLATFORM_REVIEW_V9.md).
