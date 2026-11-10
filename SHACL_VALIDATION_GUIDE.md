# Learning SHACL by building and testing graphs

**Tāttvikī v13** · Created by **Shubham** · 30-lesson learning path · Six reproducible case studies

> Goal: author SHACL constraints from business requirements, identify focus nodes, validate an RDF data graph, interpret violation reports, and automate the same checks in Python and external graph tools. Examples use original fictional data and no restricted clinical terminologies.

## 1. What SHACL actually does

A data graph answers **what facts are present**. A shapes graph states **which combinations of RDF facts are expected for selected nodes**. A SHACL processor checks the data against the shapes and reports conformance and violations.

An ontology is not a replacement for the shapes graph. For instance, declaring `ex:Dataset rdfs:subClassOf ex:Asset` lets an RDFS reasoner classify datasets as assets. That fact does not, on its own, reject a dataset with no title. A shape such as `sh:minCount 1` can detect that absence.

There are three artifacts to preserve after each validation: (1) the exact data graph, (2) the shapes graph and version, and (3) the machine-readable validation report. Log the processor version and inference mode as well.

## 2. Read a graph before writing its shapes

A tiny source graph might contain:

```turtle
@prefix ex: <https://tattviki.example/education/> .
@prefix dct: <http://purl.org/dc/terms/> .

ex:SalesDataset a ex:Dataset ;
    dct:title "Sales dataset" ;
    ex:steward ex:CatalogTeam ;
    ex:classification ex:Internal .

ex:CatalogTeam a ex:Organization .
```

Before writing validation, translate the business contract into independent statements: every dataset needs at least one title; every steward reference points to an organization; classification must be one of the approved values. The difference between a literal, IRI and blank node matters when you validate a value.

## 3. Create a shape from that contract

```turtle
@prefix ex: <https://tattviki.example/education/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dct: <http://purl.org/dc/terms/> .

ex:DatasetShape a sh:NodeShape ;
    sh:targetClass ex:Dataset ;
    sh:property [
        sh:path dct:title ;
        sh:minCount 1 ;
        sh:datatype xsd:string
    ] ;
    sh:property [
        sh:path ex:steward ;
        sh:minCount 1 ;
        sh:class ex:Organization
    ] ;
    sh:property [
        sh:path ex:classification ;
        sh:minCount 1 ;
        sh:in ( ex:Public ex:Internal ex:Restricted )
    ] .
```

Read the syntax as a sentence: `ex:DatasetShape` selects `ex:Dataset` instances, then checks the values of each indicated predicate. It does not assert that the source data actually contains the expected values.

## 4. Test a failing example deliberately

Remove `dct:title`, change `ex:steward ex:CatalogTeam` to `ex:steward ex:Unknown`, and change `ex:Internal` to `ex:Secret`. Three distinct expectations are violated: a minimum count, a class constraint, and an allowed-value list. A useful report includes the `sh:focusNode`, `sh:resultPath`, `sh:sourceConstraintComponent`, offending `sh:value` when present, and the source shape.

An empty report is **not** enough if the shape targeted zero nodes because of a typo in `sh:targetClass`. Always record the number of focus nodes selected. Also check the difference between a validation execution error and a real nonconformance result.

## 5. Use the browser lab

Open **`#shacl` → SHACL Validation Lab**. The browser provides:

- Editable **data Turtle** and **SHACL Turtle** fields.
- Six domain scenarios: Person, Catalog, SKOS/RDM, Lineage, Retail Order and IoT Observation.
- Passing and intentionally failing graphs for each scenario.
- Live validation reports identifying focus node, property and failed component.
- Exportable `data.ttl` and `shapes.ttl` for external validation.
- Dark/light appearance inherited from the existing site.

The browser checks only a documented subset (direct paths, targetClass/targetNode, counts, datatypes, classes, nodeKind, pattern, `sh:in`, `sh:hasValue`, numeric bounds). It **does not** claim full Turtle/SPARQL parsing, inference, SHACL-AF or arbitrary nested shape support. An unsupported SHACL constraint is explicitly rejected rather than silently treated as a pass.

## 6. Full validation with RDFLib + pySHACL

On a Windows terminal inside `projects/shacl-validation-lab`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python validate.py --scenario catalog --data bad --report reports/catalog-bad.ttl
python validate.py --scenario catalog --data good
python validate.py --all --expect-fixtures
python -m unittest -v test_fixtures.py
```

The one-case **bad** fixture is expected to return a nonzero exit code: that's a correct validation failure, not a crashed implementation. The `--all --expect-fixtures` command checks both positive and negative cases and exits successfully only if all expected outcomes are met. The optional `--inference rdfs` flag changes the pre-inference setting; log this choice with your result. These are **local Python** operations; GitHub Pages alone cannot execute Python for users.

Short API example:

```python
from rdflib import Graph
from pyshacl import validate

data_graph = Graph().parse('fixtures/catalog_bad.ttl', format='turtle')
shapes_graph = Graph().parse('fixtures/catalog_shapes.ttl', format='turtle')
conforms, report, message = validate(
    data_graph=data_graph,
    shacl_graph=shapes_graph,
    inference='none',
    abort_on_first=False,
)
print(conforms)
print(message)
report.serialize('catalog-report.ttl', format='turtle')
```

Prefer RDF report parsing for machine pipelines. A result count is useful but not sufficient for deciding whether an invalid source was corrected; compare focused nodes and constraint components.

## 7. External tool: Apache Jena CLI

After installing Apache Jena and adding its command-line utilities to your environment, use:

```powershell
shacl validate --shapes fixtures\catalog_shapes.ttl --data fixtures\catalog_bad.ttl
shacl validate --shapes fixtures\catalog_shapes.ttl --data fixtures\catalog_good.ttl
```

Apache Jena supports SHACL Core and SHACL-SPARQL. The official [Jena SHACL documentation](https://jena.apache.org/documentation/shacl/) also provides a Java API and Fuseki integration examples. This is a useful second implementation against which to compare your fixtures.

## 8. External tool: GraphDB

For GraphDB, start by configuring a **new repository** with SHACL support rather than assuming the mode can be enabled after creating a standard repository. Load and govern shapes through that version's documented repository mechanism. Exercise a rejected transaction with invalid data; inspect and record its validation output. See [GraphDB's SHACL validation guide](https://graphdb.ontotext.com/documentation/10.8/shacl-validation.html).

The licensing of the *tool* and the licensing of the *data* are separate questions. Tāttvikī's bundled data is fictional; do not upload client-protected graphs to a public validation service.

## 9. Advanced topics to study with full validators

**Nested and logical shapes:** `sh:and`, `sh:or`, `sh:not`, `sh:node`, `sh:qualifiedValueShape`. These support complex acceptance rules but are not implemented in the browser teaching validator.

**Property paths:** `sh:inversePath`, RDF lists of sequences, and alternatives let you validate reverse ownership and multi-step lineage. They require a full processor in this project.

**SHACL-SPARQL:** create query-driven constraints for conditions such as forbidden self-relationships and cross-record uniqueness. Limit untrusted query execution and budget performance against representative graph sizes.

**Reference data:** SKOS multilingual preferred labels may permit one preferred label per language. A naive global `sh:maxCount 1` is therefore too restrictive for multilingual schemes; use language-aware checks in an appropriate processor.

**Production quality gates:** check graph parsing, constraints, competency queries, and version/consumer impact separately. Persist shapes, data snapshots and reports so a future team can reproduce the result.

## 10. Completion checklist

A learner is ready to implement the capstone when they can explain why an RDF graph is well-formed but not SHACL-conformant, create a shape with a correct target and property path, produce one passing and one failing graph, interpret the focused violation, reproduce the outcome in pySHACL or Jena, and explain how a shape change could break an enterprise consumer.

### Primary references

- [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/)
- [SHACL 1.2 development work](https://www.w3.org/TR/shacl-core/) (check the publication status before claiming Recommendation conformance)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [Apache Jena SHACL](https://jena.apache.org/documentation/shacl/)
- [GraphDB SHACL validation](https://graphdb.ontotext.com/documentation/10.8/shacl-validation.html)
