# Tāttvikī advanced enterprise knowledge graph laboratory

This is a **fully executable local lab** using Python, RDFLib, and pySHACL. **All entities are fictional and generated**; they are not clinical facts. The source generator builds a graph connecting research studies, compounds, SKOS concepts, organizations, applications, servers, datasets, publications, and provenance.

## Run (Windows PowerShell, Linux, macOS)

```bash
python -m pip install -r requirements.txt
python generate.py
python run.py
python run.py --break-data
```

The last command **must fail** with a SHACL validation report because it removes the required `ex:investigates` relationship from `Study001`. A nonzero exit status is expected in this negative test.

## Exercises from intermediate to expert

1. Describe three competency questions, a domain model, and stable IRIs. Separate classes, individuals, and SKOS concepts.
2. Open `enterprise.ttl`. Identify how studies connect to compounds and indications. Follow `prov:wasGeneratedBy` to the generating activity.
3. Inspect the four real SPARQL queries in `run.py`: cross-domain joins, grouped aggregates, and provenance joins.
4. Change the first query to use `FILTER`, `OPTIONAL`, and subqueries. Explain how missing data impacts each form.
5. Tighten `shapes.ttl` using `sh:in`, `sh:qualifiedValueShape`, and a node shape with an embedded SPARQL constraint. Create both passing and failing test cases.
6. Add a SKOS concept hierarchy and use SPARQL property paths to traverse narrower/broader chains.
7. Create two conflicting terminology sources; design a mapping strategy (`skos:exactMatch` versus `skos:closeMatch`) and provenance for each assertion.
8. Build a CSV ingestion adapter, use reproducible IDs, add change detection, and measure duplicate resolution.
9. Introduce a named-graph provenance scheme, then discuss access controls and partial deletion by source.
10. Run a controlled GraphRAG experiment: compare vector-only retrieval with graph-expanded retrieval on a held-out question set and record answer fidelity.

## Data model

`ResearchStudy → investigates → Compound`, `ResearchStudy → hasIndication → SKOS Concept`, `ResearchStudy → ownedBy → Organization`, `SoftwareAsset → hostedOn → Server`, `ResearchStudy → usesDataset → Dataset`, `Dataset → prov:wasGeneratedBy → ResearchStudy`. The last relation uses a study as a pedagogical generation activity; in a production ontology, model the actual generating workflow activity separately.

## What is actually executed

- RDF parsing and serialization: **RDFLib**.
- SPARQL `SELECT`, `ORDER BY`, joins and `GROUP BY`/`COUNT`: **RDFLib**.
- SHACL validation and violation reports: **pySHACL**.
- The browser playground remains a deliberately small subset and **does not** use this Python engine.
- No external APIs, payments, or cloud resources required.

Documentation: [RDF 1.1](https://www.w3.org/TR/rdf11-concepts/), [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/), [SHACL](https://www.w3.org/TR/shacl/), [SKOS](https://www.w3.org/TR/skos-reference/).
