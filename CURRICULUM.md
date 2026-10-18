# Tāttvikī curriculum

The curriculum contains **613 distinct topics** across 14 learning paths. It combines 13 original starter lessons, 240 legacy topic-focused micro-lessons across 12 modules, and 360 advanced enterprise lessons across 15 more modules.

**Editorial disclosure:** The 240 legacy micro-lessons have original topic titles and contextual examples, but share a concise three-objective teaching format and general knowledge-check pattern. They are a breadth-first syllabus, not 240 independently peer-reviewed textbook chapters. Advanced mastery comes from the executable labs and official references, and deeper unique content should be added progressively.

## Fundamentals & thinking
- What is information?
- Data versus information versus knowledge
- What is a concept?
- What is an entity?
- What is a relationship?
- What is an attribute?
- Records versus networks
- How graphs represent facts
- Directed versus undirected relationships
- Labels versus identifiers
- Namespaces explained
- What does semantic mean?
- Syntax versus meaning
- Types and instances
- Open versus closed world
- Identifiers and persistence
- Data silos and integration
- Semantic interoperability
- Graph competency questions
- Knowledge graph misconceptions
## Taxonomies & thesauri
- Controlled vocabularies
- Term lists versus concept schemes
- Taxonomy foundations
- Hierarchies and polyhierarchies
- Thesaurus fundamentals
- Broader terms and narrower terms
- Related terms versus synonyms
- Preferred and alternative labels
- Hidden labels for search
- SKOS concept schemes
- SKOS top concepts
- SKOS collections
- SKOS mapping properties
- Exact match versus close match
- Broad match versus narrow match
- Labeling in multiple languages
- Definition and scope notes
- Term governance lifecycle
- Thesaurus quality checks
- Taxonomy migration strategies
## RDF deep dive
- RDF statement model
- Subject predicate object
- IRI syntax and identity
- Literal datatypes
- Language-tagged strings
- Blank nodes
- Turtle prefixes
- Turtle semicolon syntax
- Turtle comma syntax
- Turtle collections
- RDF lists
- RDF containers
- N-Triples and N-Quads
- TriG and named graphs
- JSON-LD context
- RDF/XML overview
- RDF datasets
- RDF-star and quoted triples
- Canonicalization challenges
- RDF parsing errors
## RDFS & ontology architecture
- RDF vocabulary design
- rdf:type semantics
- rdfs:Class
- rdfs:subClassOf
- rdfs:subPropertyOf
- rdfs:domain inference
- rdfs:range inference
- rdfs:label and comment
- Ontology metadata
- Ontology modularization
- Foundational ontologies
- Ontology design patterns
- Competency-question workshops
- Class versus instance modeling
- Part-whole modeling
- Events and processes
- Temporal modeling
- Qualified relations
- Ontology version IRIs
- Ontology anti-patterns
## OWL & description logic
- OWL 2 profiles
- Classes and individuals
- Object versus data properties
- Inverse properties
- Functional properties
- Transitive properties
- Symmetric properties
- Property chains
- Class intersection
- Class union
- Class complement
- Existential restrictions
- Universal restrictions
- Qualified cardinality
- Disjoint classes
- Equivalent classes
- Same individuals versus different individuals
- Open-world reasoning
- Consistency and satisfiability
- Explanation of inferred facts
## SPARQL mastery
- SPARQL SELECT
- PREFIX and BASE
- Basic graph patterns
- Multi-pattern joins
- Variable projection
- DISTINCT
- FILTER expressions
- OPTIONAL matches
- UNION patterns
- BIND expressions
- VALUES clauses
- ORDER BY
- LIMIT and OFFSET
- GROUP BY
- COUNT and SUM
- HAVING
- CONSTRUCT queries
- ASK queries
- Property paths
- Federated SERVICE queries
## SHACL & quality
- Why validate RDF?
- SHACL node shapes
- Target classes
- Property shapes
- Minimum counts
- Maximum counts
- Datatype constraints
- Node-kind constraints
- Class constraints
- Enumerations
- Regular expression patterns
- Value-range constraints
- String-length constraints
- Nested node shapes
- Logical combinations
- Qualified value shapes
- SPARQL-based constraints
- Severity levels
- Validation reports
- Continuous validation in CI
## Knowledge graph engineering
- Source profiling
- CSV to RDF mapping
- JSON to RDF mapping
- R2RML basics
- RML mapping
- Entity resolution
- Deduplication policies
- URI minting strategies
- Data lineage
- Provenance with PROV-O
- Graph ingestion pipelines
- Incremental updates
- Change data capture
- Graph storage models
- Index design
- Query optimization
- Graph partitioning
- Data quality observability
- KG testing strategy
- Deployment and rollback
## Governance & operations
- Ontology ownership
- Change request workflow
- Versioning policies
- Deprecation and replacement
- Backward compatibility
- Review and approval
- Editorial style guidelines
- Naming conventions
- IRI governance
- Metadata catalogs
- Access control
- PII in knowledge graphs
- License and attribution
- FAIR data principles
- Vocabulary publishing
- Semantic versioning pitfalls
- Release notes and changelogs
- Data stewardship
- Performance budgets
- Production incident response
## Biomedical & enterprise use cases
- Clinical study ontologies
- Drug substance identifiers
- Clinical trial endpoints
- Gene Ontology vocabulary management
- ATC classifications
- OBO Foundry ontology mapping considerations
- LOINC observation modeling
- UCUM unit harmonization
- CDISC SDTM metadata
- IDMP identification
- EMA referential data
- HGNC gene identifiers
- UniProt protein integration
- Gene Ontology evidence
- Phenotype modeling with HPO
- Disease terminology mapping
- Data product semantic layers
- Asset management graphs
- Regulatory document graphs
- Supply-chain traceability graphs
## Graph algorithms & GraphRAG
- Property graph versus RDF
- Traversal patterns
- Shortest paths
- Centrality measures
- Community detection
- Link prediction
- Embedding representations
- RDF embeddings
- Entity linking
- Text-to-triple extraction
- GraphRAG architectures
- Graph retrieval evaluation
- Vector versus graph search
- Hybrid graph-vector retrieval
- Subgraph grounding
- LLM hallucination controls
- Graph-aware agents
- Ontology-guided extraction
- Knowledge graph freshness
- Graph unlearning and deletion
## Expert architectures & research
- Temporal RDF designs
- Ontology alignment algorithms
- Schema matching
- Mapping confidence
- Logical inconsistency management
- Rule languages and SWRL
- SHACL versus OWL tradeoffs
- Multi-tenant graph architectures
- Federated knowledge graphs
- Large-scale reasoning
- Streaming graph updates
- SPARQL query planning
- Benchmark design
- Reproducible graph experiments
- Knowledge graph evaluation metrics
- Graph data contracts
- Ontology testing with competency queries
- Semantic API design
- Event-driven semantic systems
- Knowledge graph research gaps


## Enterprise edition v3 — 360 additional distinct topics

The additional tracks span enterprise metadata (catalogs, lineage, DCAT, DCMI, PROV), master data management (party identity, matching, survivorship and stewardship), reference data management (SKOS term lifecycle, controlled vocabularies, versioning), semantics (OWL profiles, shapes, contracts, interoperability), data engineering, policy, domain-specific enterprise use cases, and GraphRAG/agentic workflows.

**Content depth:** the 360 new entries each define a specific topic, a matching source-to-target implementation assignment, a synthetic Turtle example, a negative-path review, a testable acceptance criterion and a source link, but retain a shared lesson layout. They are distinct scoped lessons, not 360 independently peer-reviewed in-depth textbook chapters. The 12 industry case blueprints are more bespoke; executable work is in the linked local labs.

**Safety:** all scenarios are synthetic, and links to vendor tools, standards and terminologies do not transfer their licenses. See the preliminary audit at `LEGAL_AND_DATA_REVIEW.md`.
