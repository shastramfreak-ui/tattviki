# Tāttvikī Enterprise Retrieval & GraphRAG foundations lab

An **offline, runnable, dependency-free Python capstone** built for training. It reproduces the browser lab's 28 original synthetic enterprise documents, 20 typed entity edges, and six evidence-labelled questions.

## Run

```powershell
cd projects/enterprise-retrieval-rag
python retrieval_lab.py --mode hybrid --role viewer
python retrieval_lab.py --mode graph --role engineer --query "Which assets depend on Northforge Valve-742?"
python retrieval_lab.py --mode graph --role steward --query "Why was Pump-3 service delayed?"
python -m unittest -v test_retrieval.py
```

## Algorithms covered

- **BM25 keyword search:** inverse document frequency, term frequency, and length-normalized ranking. Useful for IDs and part numbers.
- **TF-IDF cosine vectors:** word count vectors with IDF weighting and a fixed, inspectable synonym map. A transparent illustration of cosine geometry **not a neural embedding**.
- **Hybrid Reciprocal Rank Fusion:** combine rank positions, avoiding incomparable raw score ranges. `RRF(d) = Σ 1/(60 + rank(d))`.
- **Graph expansion:** match initial evidence and explicitly named entities, follow no more than `hops` typed relationships, re-rank documents linked to encountered entities.
- **Authorization:** pre-filter corpus by role; returned evidence and evaluation gold labels respect role visibility.
- **Retrieval evaluation:** Recall@k and Precision@k against visible, human-curated gold evidence on the fixed question set. These are *not* benchmarks for production systems.

## Exercises

1. Compare the same six questions for each retrieval mode. Which questions benefit from graph relationships? Which favor an exact keyword?
2. Change `top_k` from 3 to 8. Record both recall and precision, and explain the tradeoff.
3. Switch viewer → engineer → steward for the service delay query. Explain why additional documents are not automatically safe to show everybody.
4. Change the synonym map. Which paraphrases improve, and which exact identifiers risk being harmed?
5. Remove a source document and test whether graph links still have sufficient provenance. What should a production pipeline do when an index and source disagree?
6. Implement nDCG@k and a citation-support evaluator; keep both distinct from language-model answer quality.

## Production extension plan

To build a genuine AI system from this baseline, add a real embedding model in a **separately configured** environment; train/evaluate dimensionality and model migrations; store vectors in an index; implement source-aware chunking and authenticated metadata filtering; and run a hosted or local LLM with citations and prompt-injection protections. For semantic graphs, persist entities and typed relationships with auditable provenance and use a read-only query interface. None of this capstone requires API keys or redistributes third-party data.

See [Microsoft GraphRAG query modes](https://microsoft.github.io/graphrag/query/overview/), [Neo4j retriever patterns](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) and [hybrid RRF mechanics](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking).

**Security warning:** Role-based filtering here operates on public bundled synthetic fixtures. It is not real authentication or access control. In production the source documents, graph links and permissions must be protected by server-side authorization.
