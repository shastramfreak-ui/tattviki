# Tāttvikī v12 — Graph Theory, Graph Algorithms, and CAG

**Creator: Shubham** · Original fictional examples only · Free learning material

## Why the learning platform has two distinct labs

**Ontology Studio** is where an ontology is *authored*: identifiers, OWL/RDFS classes, object/data properties, individuals, axioms, SKOS and sample SHACL shapes. It now contains a **Code Lab** (`#studio/code`) for Turtle editing, beginner SPARQL practice and inspecting RDF triples. The old `#playground` bookmark resolves to the Code Lab for backwards compatibility, but there is no duplicate Playground item in navigation.

**Graph Theory Lab** (`#graphlab`) is where *algorithms are taught*: BFS, Dijkstra, connected components, degree centrality, PageRank and directed-cycle/topological checks. It can use one of 12 synthetic networks or take a **read-only snapshot** of the current Studio model. Analysis in the Graph Theory Lab does not edit RDF or validate OWL semantics. The separate AI Retrieval Lab (`#retrieval`) continues to compare BM25, a TF-IDF/cosine teaching proxy, hybrid RRF and graph-assisted retrieval.

## Technical ideas taught in the new lessons

| Learning path | Practical focus | Common mistake |
| --- | --- | --- |
| Graph theory essentials (12) | Nodes, directed and weighted edges, cycles, trees, components, density, subgraphs, representations | Confusing an undirected drawing with RDF predicates |
| Graph algorithms (12) | BFS, DFS, Dijkstra, Bellman–Ford, topological sort, SCC, degree, betweenness, PageRank, community methods, MST, complexity | Choosing an algorithm without checking weights or direction |
| Enterprise graph patterns (10) | RDF/property graph comparison, SHACL vs OWL, data lineage, identity resolution, provenance, temporal graphs, federation, permissions, releases and GraphRAG | Treating graph proximity as verified business truth |
| Cache and augmented generation (8) | CAG, KV-cache prefill, cache invalidation, warm/cold economics, security isolation, RAG/GraphRAG comparison and CRAG | Calling vector similarity a KV cache, or equating CAG with CRAG |

Each of the 42 topic pages contains a specific technical definition, business problem, failure case, worked exercise, verification steps and a knowledge check. Subjects remain educational study units, not replacements for specialist books or formal standards.

## Graph Theory Lab datasets

The lab contains twelve independent fictitious networks: enterprise metadata lineage, supply chain, industrial digital twins, research provenance, cybersecurity, retail operations, urban transit, public-sector reporting, cloud infrastructure, reference-data governance, scholarly citations and support knowledge.

The downloadable `data/graph_examples.json` is the canonical source. Across the twelve examples it contains **360 unique nodes and 616 directed relationships**. Relationships in each network describe a fictional case; additional explicitly marked *algorithm-expansion edges* permit substantial traversals. All edge weights are **nonnegative unitless teaching costs**, not travel durations, currency, risk scores or observed production measures.

Each dataset is validated for unique identifiers, existing endpoints, reasonable sizes and nonnegative weights. NetworkX independently checks the browser calculations, including directed shortest paths, weak connectivity, centrality, PageRank and cycle detection. Because different predicate types can connect an ordered node pair, these are **directed multigraphs**, not simple directed graphs. The library comparisons preserve multiplicity. Negative-weight shortest path, full Louvain clustering and OWL reasoning are covered conceptually but are **not** claimed as implemented browser calculations.

## How to try it

1. Open `#learn` and select **Graph theory essentials**. Work through nodes, direction, paths, connectivity and trees first.
2. Open `#graphlab`, choose **Supplier risk**, and select BFS or Dijkstra. Compare hop count and weighted cost.
3. Switch to **Grid**, **Radial** or **Swimlanes**. Zoom with the wheel or `+`/`−`; pan by dragging the empty canvas. Select nodes to inspect typed outgoing/incoming relationships.
4. Choose **Weak components**, **Degree centrality**, **PageRank**, or **DAG / cycle audit**. Write down what each calculation *does not* prove.
5. Open `#studio`, create classes and individuals, then return to `#graphlab` and choose **Use current Studio model**. The displayed graph is a read-only graph projection and analyzes explicit statements, not inferred OWL facts.
6. Go to `#studio/code`, use **Load ontology from Studio** to populate Turtle. The in-browser parser only supports a Turtle/SPARQL teaching subset; use the optional full parser or Python backend for advanced OWL/SHACL/SPARQL features.
7. Export a graph JSON sample and inspect the nodes, edge labels, edge weights and validation metadata.

## CAG ≠ CRAG ≠ GraphRAG

- **CAG — Cache-Augmented Generation:** preloads a *bounded* corpus into a long-context model and reuses prepared KV cache. Useful for relatively stable, manageable source collections and repeated questions. Requires a model-specific cache, sufficient memory, safe permission boundaries and version-based invalidation. **This website does not run a transformer or measure actual KV-cache GPU latency.**
- **RAG:** retrieves source passages at request time. Useful for larger, frequently changing collections if retrieval and metadata filters are robust.
- **GraphRAG:** brings entities, relations, graph neighborhoods and possibly community summaries into retrieval. A local graph traversal question differs from a global corpus-wide thematic question.
- **CRAG — Corrective RAG:** evaluates retrieval quality and takes corrective actions when retrieved passages are weak. This is unrelated to the KV-caching meaning of CAG.

## Open references (links, not redistributed content)

- NetworkX graph theory algorithms: https://networkx.org/documentation/stable/reference/algorithms/index.html
- RDF 1.1 Concepts: https://www.w3.org/TR/rdf11-concepts/
- SPARQL 1.1 Query Language: https://www.w3.org/TR/sparql11-query/
- Microsoft GraphRAG official documentation: https://microsoft.github.io/graphrag/
- Cache-Augmented Generation paper (Chan et al., 2025): https://doi.org/10.1145/3701716.3715490
- Corrective Retrieval Augmented Generation (2024): https://arxiv.org/abs/2401.15884

These sources remain owned by their publishers. Tāttvikī uses original explanations and invented teaching records; references are attribution links, not license grants for source material.

## Verification commands

From the website root:

```bash
node scripts/check_content.cjs
python scripts/check_learning_guides.py
node scripts/test_ui_render.cjs
python scripts/test_v12_data.py
python scripts/test_v12_browser.py
```

`test_v12_data.py` uses `networkx`, `rdflib` and `pytest` in addition to Node.js; the website itself requires none of them. `test_v12_browser.py` needs Playwright and a local Chromium installation. The GitHub Pages publishing workflow runs the content checks; full semantic backend checks still depend on separately installed Python packages.
