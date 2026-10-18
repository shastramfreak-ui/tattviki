"""Run the fictional study KG example: query RDF and validate using SHACL."""
from pathlib import Path
from rdflib import Graph
from pyshacl import validate

HERE = Path(__file__).resolve().parent

data = Graph().parse(HERE / "studies.ttl", format="turtle")
shapes = Graph().parse(HERE / "shapes.ttl", format="turtle")
query = (HERE / "query.rq").read_text(encoding="utf-8")

print(f"Loaded {len(data)} RDF triples")
print("\nStudy ID | Compound | Indication")
for study_id, compound, indication in data.query(query):
    print(f"{study_id} | {compound} | {indication}")

conforms, report_graph, report_text = validate(
    data_graph=data, shacl_graph=shapes, inference="none", abort_on_first=False
)
print("\nSHACL validation:", "PASS" if conforms else "FAIL")
if not conforms:
    print(report_text)
    raise SystemExit(1)
