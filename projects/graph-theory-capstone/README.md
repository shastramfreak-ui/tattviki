# Graph theory capstone — a reproducible enterprise graph report

This capstone uses original fictional graph datasets from `../../data/graph_examples.json`. It computes paths, components, directed cycles, degree and unweighted PageRank using the independently maintained open-source NetworkX library. It does **not** modify the ontology stored in the Studio and does not call an LLM.

From the project root:

```bash
python -m pip install -r projects/graph-theory-capstone/requirements.txt
python projects/graph-theory-capstone/analyze.py --graph graph-02
cd projects/graph-theory-capstone
python -m unittest -v test_graph.py
```

The twelve IDs range from `graph-01` to `graph-12`. Compare this report with the browser `#graphlab` results. A directed multigraph can contain multiple predicate-typed edges between a pair of nodes. These samples give edges positive **unitless teaching weights**; do not interpret the numbers as physical durations or real risks.

Suggested advanced extension: record edge provenance in a named graph, add a temporal validity field, write SHACL rules for required identifiers and introduce user-authorized graph filtering before any retrieval pipeline. Also measure changes to reachability after removing each edge and explain their business interpretation.
