# AI retrieval, GraphRAG and context graphs — advanced curriculum

> Updated 26 October 2026. Original educational text; linked vendor/standards references are not redistributed.

These are **52 additional, distinct lessons**. Each has a concept explanation, an enterprise case, a failure analysis, a design or runnable code example, a verification exercise, and a topic-aligned quiz.

These topics distinguish exact lexical retrieval, teaching TF-IDF, learned embeddings, graph traversal, RAG generation and agentic decision logic. Do not treat them as interchangeable.

## Vector foundations

Embeddings, metrics, ANN indexes and relevance testing

- **[What an embedding represents](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-01)** — A text embedding is a learned numerical representation, not a bag of individual facts; neighboring vectors often correspond to similar meaning.
- **[Cosine similarity and geometry](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-02)** — Cosine divides the dot product by vector norms to compare directions. Identically directed nonzero vectors score 1, orthogonal vectors 0 and opposite vectors -1.
- **[Dense versus sparse retrieval](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-03)** — Dense embeddings encode learned features across most coordinates; sparse representations emphasize a small number of lexical or learned term dimensions.
- **[Dot product, normalization and distance](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-04)** — Dot product combines vector direction and magnitude; Euclidean distance measures geometric separation. Their rankings differ for non-normalized data.
- **[Choosing and versioning embedding models](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-05)** — Embedding model selection must consider supported languages, input length, domain vocabulary, cost, latency, safety and query-document alignment.
- **[Approximate nearest neighbors and HNSW](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-06)** — Approximate nearest-neighbor indexes trade search speed and memory for imperfect nearest-neighbor recall; HNSW organizes navigable proximity layers.
- **[Vector index filtering and authorization](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-07)** — Metadata filters narrow candidates by tenant, classification, date and permission; the order of filtering and ANN retrieval affects both relevance and security.
- **[Multimodal vectors and representation alignment](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-vector-08)** — Multimodal retrieval may align text, images and other signals into one shared or cross-linked embedding space; compatibility is model-dependent.

## Retrieval & RAG

BM25, chunking, fusion, reranking and grounded answers

- **[RAG pipeline stages and boundaries](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-01)** — RAG separates ingestion, transformation, indexing, retrieval, ranking, context assembly and grounded generation. Failures can occur at any stage independently.
- **[Chunking by structure and meaning](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-02)** — Chunk boundaries should respect section headings, tables, cross-references and paragraph semantics; fixed token windows are only a baseline.
- **[BM25 lexical retrieval](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-03)** — BM25 ranks passages with query-term occurrence, document-length normalization and inverse document frequency. It is valuable for rare exact tokens.
- **[Hybrid search and reciprocal rank fusion](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-04)** — Hybrid retrieval combines keyword and vector-ranked lists. RRF adds 1/(k+rank) for each list; it combines positions rather than incomparable raw scores.
- **[Cross-encoder reranking](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-05)** — A reranker scores a query together with each candidate document and can improve precision, but introduces additional inference cost.
- **[Contextual retrieval and parent context](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-06)** — Contextual retrieval can prepend a concise description of a chunk's surrounding document context before indexing, improving disambiguation.
- **[Query rewriting and multi-query search](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-07)** — Query transformations may expand acronyms, split compound questions or generate complementary subqueries, then reconcile their evidence.
- **[Evidence citations and answer faithfulness](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-08)** — A grounded answer should link each material claim to an accessible passage, provenance record or graph fact. Citation presence alone is insufficient.
- **[RAG evaluation, recall and faithfulness](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-09)** — Retrieval Recall@k tests whether the evidence was found; answer accuracy and faithfulness test different downstream questions.
- **[Prompt injection and retrieval trust](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-rag-10)** — Retrieved content is untrusted evidence, not instructions. The model must not execute embedded commands or reveal restricted context.

## GraphRAG engineering

Graph extraction, traversal, community search and evidence

- **[GraphRAG versus vector-only RAG](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-01)** — GraphRAG adds explicit entity/relation structure to retrieval; it does not require one storage technology or one universal retrieval algorithm.
- **[Entity and relationship extraction](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-02)** — Graph construction identifies mentions, canonical entities, relation types and source spans. Schema-guided extraction reduces type drift.
- **[Entity resolution and canonicalization](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-03)** — Entity resolution links aliases or duplicate mentions to stable IDs using constraints, matching signals and human stewardship.
- **[Multi-hop graph retrieval](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-04)** — A multi-hop query follows typed edges across several entities, enabling relationship reasoning beyond single-passage similarity.
- **[Local search versus global search](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-05)** — Local search combines entity neighborhoods and supporting text for focused questions; global search analyzes synthesized community reports for corpus-wide themes.
- **[Community detection and report hierarchies](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-06)** — Community-detection groups strongly connected entities; hierarchical summaries help broad exploration but require costly indexing.
- **[DRIFT search and adaptive expansion](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-07)** — DRIFT in Microsoft GraphRAG blends local detail with broader context through iterative query expansion.
- **[Text-to-Cypher and query safety](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-08)** — Text-to-Cypher translates user language into structured graph queries; generated queries must be restricted to validated read-only access.
- **[Graph-grounded evidence and provenance](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-09)** — Graph edges must link back to the documents, records, timestamps and extraction decisions that justify them.
- **[GraphRAG benchmarking and ablation](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-graphrag-10)** — Compare vector-only, lexical, hybrid and graph-assisted variants on identical questions, judged evidence and access rules.

## Context graphs & memory

Temporal context, decisions, agent memory and replay

- **[What is an enterprise context graph?](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-01)** — A context graph extends linked enterprise knowledge with operational state, decisions, workflow events and evidence relevant to an agent's actions; the term is emerging rather than a single fixed W3C standard.
- **[Temporal knowledge and valid-time facts](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-02)** — Time-sensitive context distinguishes when a fact was true in the real world from when the system learned or recorded it.
- **[Decision provenance and approval rationale](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-03)** — A decision record should capture proposed action, constraints, evidence, reviewer, outcome and affected version.
- **[Agent memory versus knowledge graphs](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-04)** — Agent conversation memory records interactions and state; a knowledge graph represents reusable structured entities and relations. Both can interact but serve different needs.
- **[Context assembly and token budgets](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-05)** — Context assembly selects the smallest sufficient relevant evidence from vector hits, graph paths, rules and recent events.
- **[Event-driven context updates](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-06)** — Enterprise context may change via CDC, workflow events and API updates; retrieval indexes and graph edges must indicate freshness.
- **[Context graph access governance](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-07)** — Context is often the most sensitive layer because it combines identities, decisions, incidents and access patterns.
- **[Context graph validation and replay](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-context-08)** — Replay a recorded agent decision using the same facts, policy revision and context snapshot to assess reproducibility.

## Agentic knowledge systems

Tool routing, plans, permissions, and observable actions

- **[Agentic retrieval and question planning](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-01)** — An agentic retrieval workflow may plan subqueries, select evidence tools, inspect results and stop when evidence is sufficient.
- **[Tool routing across SQL, graph and vectors](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-02)** — A router chooses SQL for aggregates, graphs for paths, keyword search for IDs, and vector retrieval for paraphrases.
- **[Retrieval plans and query decomposition](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-03)** — Decomposing a question creates dependent subqueries whose evidence can be joined by entity ID and time.
- **[Tool-output validation and schema contracts](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-04)** — Agent tool output must match typed schemas and distinguish evidence, uncertainty, errors and permission denials.
- **[Human approval and reversible actions](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-05)** — High-impact actions require bounded automation, human approval and an audit trail that records policy and evidence.
- **[Grounded planning and uncertainty](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-06)** — A planning agent should distinguish known facts, inferred implications, assumptions and unanswered questions.
- **[Graph-based agent evaluation](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-07)** — Task benchmarks should evaluate tool-selection, evidence correctness, authorization, latency and completion—not only language fluency.
- **[Agent trace observability](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-agent-08)** — Execution traces reveal query planning, retrieval stages, source access, reasoning steps exposed by tooling, and final citation support.

## Enterprise AI architecture

Governance, freshness, metadata, benchmarking and deployment

- **[Reference architecture for enterprise RAG](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-01)** — A production architecture separates connectors, ingestion, identity, embeddings, graph, retrieval, reranking, generation and governance planes.
- **[Metadata, lineage and retrieval provenance](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-02)** — Every retrieved chunk and graph edge should link to a catalog asset, source version, processing run and steward.
- **[Index refresh, CDC and consistency](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-03)** — Ingestion pipelines need idempotent updates, tombstones, concurrency controls and explicit freshness guarantees.
- **[PII minimization and permission-aware RAG](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-04)** — Personal data and privileged business information require source-level minimization and consistent retrieval ACL enforcement.
- **[Cost, latency and accuracy budgets](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-05)** — GraphRAG indexing, model calls, reranking and multi-hop traversals have different costs; design for measurable tradeoffs.
- **[Model and prompt version changes](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-06)** — Changes to embedding models, extractors, prompts or ontologies may alter rankings and graph edges even when source data is unchanged.
- **[GraphRAG deployment decision framework](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-07)** — Choose document RAG, hybrid retrieval or GraphRAG by question mix, relation complexity, freshness, privacy and operating cost.
- **[Responsible use, licenses and evaluation governance](https://shastramfreak-ui.github.io/tattviki/#lesson/ai-production-08)** — Evaluation corpora, third-party vocabularies, model weights and uploaded documents each have separate rights and obligations.

## Technical sources

- [Microsoft GraphRAG indexing](https://microsoft.github.io/graphrag/index/overview/) and [query modes](https://microsoft.github.io/graphrag/query/overview/)
- [Neo4j GraphRAG retrievers](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html)
- [Azure AI Search hybrid retrieval](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview/) and [RRF](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking)
- [Anthropic contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)

**Teaching limitations:** The browser lab performs BM25 and a TF-IDF vector proxy, plus a small curated entity graph. It does not call an LLM, generate neural embeddings or implement Microsoft GraphRAG end-to-end.
