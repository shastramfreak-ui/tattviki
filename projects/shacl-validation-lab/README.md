# SHACL Validation: from shapes to reports

This is the **full-validator companion** to Tāttvikī's browser SHACL Validation Lab. All example data is synthetic and original, with no proprietary clinical terminologies.

## Files

- `fixtures/*_data.ttl` — data graphs (`good` and `bad` variants)
- `fixtures/*_shapes.ttl` — actual SHACL shapes, reusable in external tools
- `validate.py` — RDFLib + pySHACL validator and RDF report export
- `test_fixtures.py` — fixture parsing tests; optional pySHACL execution tests

Six domain scenarios: People/HR, metadata catalog, SKOS/RDM, pipeline lineage, retail orders and sensor observations.

## Install and run on Windows

```powershell
cd projects\shacl-validation-lab
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python validate.py --scenario people --data bad --report reports/people-bad.ttl
python validate.py --scenario people --data good
python validate.py --all --expect-fixtures
python -m unittest -v test_fixtures.py
```

**Exit codes:** running one *invalid* graph returns code 1; this is expected and shows that the quality gate correctly detected invalid data. `--all --expect-fixtures` returns 0 if all intentionally good/bad expectations hold.

The script writes the machine-readable **sh:ValidationReport RDF** when given `--report`. Inspect focus nodes, result paths, constraint components and severities; do not rely on the text message alone.

## Alternative: Apache Jena (external tool)

With Apache Jena CLI installed and available in `PATH`, run from this folder:

```powershell
shacl validate --shapes fixtures\catalog_shapes.ttl --data fixtures\catalog_bad.ttl
shacl validate --shapes fixtures\catalog_shapes.ttl --data fixtures\catalog_good.ttl
```

Command syntax is documented at <https://jena.apache.org/documentation/shacl/>. It is an independent SHACL implementation; behavior can differ depending on settings and supported extensions.

## Alternative: GraphDB

1. Create a **new** GraphDB repository with SHACL support enabled (the vendor does not generally allow retrofitting the flag to an existing repository).
2. Load your shapes using the shape graph / import mechanism documented for your precise GraphDB version.
3. Insert the `good` and `bad` RDF datasets as separate transactions, observing violation behavior.
4. Inspect validation results and consider how shape versioning affects existing data.

Vendor reference: <https://graphdb.ontotext.com/documentation/10.8/shacl-validation.html>. **Do not upload sensitive enterprise production data to public hosted validators.**

## Important conceptual distinctions

- RDF **syntax validity** is separate from SHACL **constraint validity**.
- SHACL's shapes/data graphs are separate from ontology reasoning; inference mode changes some outcomes.
- A valid RDF graph may be non-conformant to a SHACL shape and still be logically consistent under OWL.
- Tāttvikī browser validation is a **teaching subset**; for full SHACL Core, SPARQL, advanced paths, meta-SHACL, etc., use pySHACL or Jena.

Primary reference: <https://www.w3.org/TR/shacl/>
