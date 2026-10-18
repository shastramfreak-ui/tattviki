# Hands-on project: a tiny clinical studies knowledge graph

**Fictional data for teaching. Not medical or clinical evidence.**

## Goal

Answer the question: **Which fictional studies investigate which compounds for which indications?**

Steps:
1. Read `studies.ttl`. Identify Study, Compound and Indication nodes.
2. Read `query.rq`. Note how SPARQL joins across multiple triples.
3. Read `shapes.ttl`. It requires a study identifier, an investigated product and an indication.
4. Run the graph with open-source Python tools:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install "rdflib>=7,<9" "pyshacl>=0.29,<1"
python run.py
```

5. Remove one `ex:studyId` triple from `studies.ttl` and rerun. Explain the SHACL report.
6. Add a new fictional study and a `skos:altLabel` to an indication. Query it.

Real biomedical ontologies require licensing/attribution review, stable identifiers, governance and expert validation before production use. This is intentionally a tiny standalone learning dataset.
