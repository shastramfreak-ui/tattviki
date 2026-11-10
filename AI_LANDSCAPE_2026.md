# Retrieval, GraphRAG and context graphs: a 2026 architecture field guide

**Last editorial review:** 26 October 2026  
**Scope:** Original educational explanations plus external primary references. This is not a market ranking and not a product endorsement.

## Start with the task, not a product name

Enterprise questions fall into different shapes:

| Question shape | First technique to evaluate | Why | What can fail |
|---|---|---|---|
| Find `VALVE-742` | BM25 / exact fields | Preserves rare identifiers | Analyzer strips punctuation or the ID is absent |
| Find meaning-related documents | Dense vector embeddings | Can bridge paraphrases | High similarity is not evidence of truth |
| Find policies and part codes together | Hybrid BM25 + vectors | Balances term precision with semantics | Poor fusion or permissions undermine both branches |
| Trace Supplier → Component → Asset | Typed graph traversal | Follows explicit dependencies | Broken entity resolution or missing source evidence |
| Identify broad themes across a corpus | Community reports / global search | Organizes aggregate patterns | Outliers and exceptions may be omitted |
| Explain why a past action was approved | Context graph with event/decision provenance | Reconstructs policy, evidence and time | Current-state-only graphs misrepresent history |
| Coordinate several sources/tools | Agentic query planning | Decomposes dependent subtasks | Tool misuse, budget drift and unauthorized actions |

A good semantic system may combine several approaches. **Do not use GraphRAG only because a graph is available.** Measure whether explicit multi-hop relationships or corpus-level synthesis improve representative business questions over simpler retrieval.

## Where vectors fit

An embedding is a vector produced by a trained encoder. Semantic similarity varies by model and task. Store model ID, dimensionality, normalization settings and source ID. A vector hit is a *candidate*. Verify its relevance and freshness before allowing a generated answer to rely on it.

Dense retrieval is not the same thing as sparse/lexical retrieval. Dense encoders can retrieve paraphrases. BM25 typically handles exact codes, names and rare tokens well. Some systems also use learned sparse representations or late-interaction retrieval, which should be evaluated against corpus and latency constraints instead of being treated as universally better.

An approximate nearest-neighbor index such as HNSW can scale retrieval but trades perfect nearest-neighbor recall for performance. Its accuracy must be measured against exhaustive search on a sampled evaluation set.

### The educational lab's scope

The browser lab intentionally computes **TF-IDF vectors with cosine similarity** and a fixed visible synonym map. This teaches geometry and ranking with no API keys. It does **not** create neural embeddings or demonstrate ANN index performance. Those are separate engineering lessons requiring a trained model and production-grade vector index.

## Where RAG fits

A useful retrieval-augmented system separates the document lifecycle (capture → parse → chunk → annotate → index) from the query lifecycle (authorize → rewrite/plan → retrieve → fuse → rerank → assemble evidence → generate → validate/cite). These stages have independently measurable error rates.

**RRF** is one way to combine rank lists without comparing uncalibrated raw scores. If a document is 2nd in BM25 and 1st in vector search, its score in a standard teaching configuration is `1/(60+2) + 1/(60+1)`. Remember that `60` is the fusion constant, not the number of nearest neighbors.

Contextual retrieval enriches chunks with grounded parent-document information before indexing. Keep raw and enriched text separately, and always cite the original section. Reranking can improve ordering of already-retrieved candidates but cannot retrieve missing evidence.

## What GraphRAG actually adds

**Graph construction** identifies entities, canonical identifiers, relationships and supporting text spans. Its quality depends on extraction, entity resolution, predicate design and provenance governance.

**Graph retrieval** combines structural relationships with text evidence. Neo4j's GraphRAG tooling describes, among others, vector retrievers, hybrid retrievers, vector-plus-Cypher expansion and Text2Cypher strategies. Implementations differ in storage, security and inference semantics.

**Microsoft GraphRAG** documents distinct query modes: local search, global search and DRIFT search. Local is useful for entity-centered questions, global for corpus-wide themes built from community reports, and DRIFT for combining localized inquiry with broader iterative exploration. Building community reports may add substantial indexing cost; it is not a free upgrade.

GraphRAG does not automatically entail OWL reasoning, SHACL validation or an RDF triplestore. You can use an ontology to govern graph types and predicates, but the retrieval approach itself is not an ontology language.

## Context graphs: useful, emerging, not a new RDF standard

In 2026 industry literature, *context graph* is used to describe knowledge that surrounds decisions and agent workflows: actors, events, policies, prior actions, approvals, temporal state and evidence. There is no single universally adopted normative context-graph schema. You can represent many of these relationships using RDF/PROV-O, a property graph, event logs, or a hybrid.

For example, a static KG might say `Supplier-A supplies Valve-742`. A context-aware decision record could also capture that an exception was proposed, evidence considered, policy revision, approver, valid-time range, recorded-time range, and the eventual decision. Without that information, agents may confuse past approvals with current authorization.

Separate **session memory** (ephemeral user conversation), **enterprise knowledge** (governed canonical facts), **event history** and **decision records**. Never casually copy private conversation text into a shared organizational graph.

## Agentic retrieval and knowledge tools

An agent can select among exact lookup, SQL, a semantic index, graph traversal and external services. Design tools with clear input schemas, typed output, read-only access where appropriate, rate/time budgets, security boundaries and explicit failure codes. Model Context Protocol (MCP) standardizes a way to expose resources, prompts and tools; it does not by itself guarantee that tool results are correct or access-controlled.

For high-impact MDM merges, ontology publication, payment execution or sensitive access approvals, prefer **propose → inspect semantic diff → human approval → execute → audit**, rather than unrestricted tool autonomy.

## A measurable production acceptance plan

1. Curate source-labelled questions from real use cases, including single-document, exact code, multi-hop, aggregate and temporal questions.
2. Run at least BM25-only, vector-only, hybrid, hybrid plus reranker, and hybrid plus graph traversal on the **same** labelled set.
3. Measure Recall@k and nDCG@k for retrieval, and separately verify answer claims and citations. Track abstentions.
4. Red-team authorization: ensure restricted records and graph links never appear in retrieved context or derivative summaries.
5. Test deletion, index lag, schema changes, model upgrades, conflicting identities and historical replay.
6. Measure p95 latency, indexing cost, retrieval cost and operational ownership before declaring the system production-ready.

## Primary references checked in October 2026

- [Microsoft GraphRAG indexing overview](https://microsoft.github.io/graphrag/index/overview/)
- [Microsoft GraphRAG query modes](https://microsoft.github.io/graphrag/query/overview/)
- [Neo4j GraphRAG Python retrievers](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html)
- [Azure AI Search hybrid retrieval](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview/)
- [Azure AI Search RRF ranking](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking)
- [Anthropic contextual retrieval, published September 2024](https://www.anthropic.com/research/contextual-retrieval)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [Gartner's September 2026 context-graph abstract](https://www.gartner.com/en/documents/8384981) (the full report may require a subscription)

**Publication and licensing:** These are external reference links, not copied documentation or proof of interoperability. All capstone entities and enterprise records in Tāttvikī v11 are fictional.
