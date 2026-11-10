"""Full SHACL validation example using RDFLib + pySHACL.

Install requirements first; no proprietary terminology or remote data needed.

Examples:
    python validate.py --scenario catalog --data bad
    python validate.py --scenario catalog --data good
    python validate.py --all --expect-fixtures
"""
import argparse
import sys
from pathlib import Path

from rdflib import Graph, Namespace

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
SH = Namespace("http://www.w3.org/ns/shacl#")


def run(scenario: str, variant: str = "good", inference: str = "none", report_path: Path | None = None):
    try:
        from pyshacl import validate
    except ImportError as exc:
        raise SystemExit("pySHACL is not installed. Run: python -m pip install -r requirements.txt") from exc

    data_path = FIXTURES / f"{scenario}_{variant}.ttl"
    shapes_path = FIXTURES / f"{scenario}_shapes.ttl"
    if not data_path.is_file() or not shapes_path.is_file():
        raise FileNotFoundError(f"Unknown scenario or fixture: {scenario}/{variant}")
    data = Graph().parse(data_path, format="turtle")
    shapes = Graph().parse(shapes_path, format="turtle")
    conforms, report_graph, results_text = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference=inference,
        abort_on_first=False,
        meta_shacl=False,
        advanced=False,
        allow_warnings=False,
    )
    components = list(report_graph.objects(None, SH.sourceConstraintComponent))
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_graph.serialize(destination=str(report_path), format="turtle")
    return conforms, components, results_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce SHACL validation across fictional enterprise RDF scenarios")
    parser.add_argument("--scenario", choices=[p.stem.removesuffix('_shapes') for p in FIXTURES.glob('*_shapes.ttl')], default="people")
    parser.add_argument("--data", choices=["good", "bad"], default="bad")
    parser.add_argument("--inference", choices=["none", "rdfs", "owlrl", "both"], default="none")
    parser.add_argument("--report", type=Path, help="Save sh:ValidationReport as RDF Turtle")
    parser.add_argument("--all", action="store_true", help="Validate every fixture pair")
    parser.add_argument("--expect-fixtures", action="store_true", help="Exit zero only if good fixtures pass and bad fixtures fail")
    args = parser.parse_args()
    if args.all:
        successful = True
        for s in sorted(p.stem.removesuffix('_shapes') for p in FIXTURES.glob('*_shapes.ttl')):
            for v in ("good", "bad"):
                conforms, components, _ = run(s, v, args.inference)
                print(f"{s:12s} {v:5s} conforms={str(conforms):5s} validation_results={len(components)}")
                if args.expect_fixtures and conforms != (v == 'good'):
                    successful = False
        return 0 if successful else 1
    conforms, components, text = run(args.scenario, args.data, args.inference, args.report)
    print(f"Scenario={args.scenario} variant={args.data}; conforms={conforms}; issues={len(components)}")
    print(text)
    return 0 if conforms else 1


if __name__ == '__main__':
    sys.exit(main())
