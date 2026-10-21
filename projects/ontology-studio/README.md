# Tāttvikī Ontology Studio — enterprise modeling demonstration

This example is **entirely synthetic**. It describes fictional CRM/ERP, metadata catalog, RDM statuses, MDM parties, studies, products, pipelines, stewardship, quality checks and data lineage. It contains no real patient information or exported restricted terminology.

## What it contains

- `enterprise-ontology.ttl`: full OWL/RDFS/SKOS + SHACL example serialized as Turtle.
- `enterprise-ontology.rdf`: equivalent RDF/XML ontology, suitable for loading in Protégé Desktop.
- `enterprise-ontology.jsonld`: equivalent Linked Data serialization.
- `editable-ontology-project.json`: **native studio project backup** that can be imported using **Files & imports** inside Tāttvikī's Ontology Studio.
- `queries/`: real SPARQL queries for class hierarchies, ontology schema, and metadata lineage.

All ontology serializations are generated from `assets/studio.js` by `scripts/export_studio_demo.cjs`. They are RDF graph isomorphic, tested with RDFLib by `scripts/check_studio_exports.py`.

## Hands-on walkthrough

1. Go to **Ontology Studio** on the public Tāttvikī website.
2. Select `Dataset` under Classes. Inspect and change the `SubClassOf` relationship or create a new class.
3. Select **Object properties** → `ownedBy`. Inspect its domain, range and inverse `owns`. Optionally mark it functional.
4. Select **Individuals** → `CuratedParties`. Add a property assertion or change a synthetic source code.
5. Select **Thesaurus (SKOS)** → `Approved`. Add an alternative English label. SKOS concepts and their schemes are exported.
6. Select **SHACL shapes** → `PartyMasterShape`. Set minimum count to `3`, then choose **Inspect**; the teaching checker shows sample-data violations. Return count to `1`.
7. Go to **Files & imports** → **Export OWL/Turtle**, **RDF/XML**, or **JSON-LD** to use in other programs.
8. Click **Backup JSON** to save all editor state. Import that JSON in the same interface to resume editing.

## Run real queries and parse the exports

```bash
python -m pip install rdflib
python scripts/check_studio_exports.py
```

Run the above commands from the project **root**, not this folder.

For a query example in Python:

```python
from rdflib import Graph
from pathlib import Path
g = Graph().parse('projects/ontology-studio/enterprise-ontology.ttl', format='turtle')
query = Path('projects/ontology-studio/queries/metadata-lineage.rq').read_text()
for row in g.query(query):
    print(row)
```

## Accuracy and limitations

- The site creates **explicit RDF/OWL statements** but does not perform OWL 2 DL classification or infer new statements. Import the export into Protégé for HermiT or another compatible reasoner.
- The browser offers structural validation and a **subset** of SHACL property checks; this is not full SHACL validation. Full SHACL engines include pySHACL, RDF4J and TopBraid SHACL tooling.
- The editor does not import arbitrary TTL/RDF/XML into its visual forms. Use its own project JSON for lossless round-trip editing, or open Turtle/RDF/XML files in external ontology tools.
- `.owl.ttl` is Turtle syntax (not OWL/XML). `.rdf` is RDF/XML.
- GitHub Pages hosts only the client-side interface and examples. Collaboration, access control, full OWL import resolution, plugin support, versioned team editing and complete reasoning require separate software/services.
