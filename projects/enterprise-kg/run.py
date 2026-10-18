"""Real executable RDFLib SPARQL and pySHACL lab. Usage: python run.py [--break-data]."""
from pathlib import Path
import sys
from rdflib import Graph, Namespace
from pyshacl import validate
from generate import EX, ROOT

if not (ROOT/'enterprise.ttl').exists():
    from generate import outfile # auto-generation at import

data = Graph().parse(ROOT/'enterprise.ttl',format='turtle')
if '--break-data' in sys.argv:
    data.remove((EX.Study001,EX.investigates,None))

queries = {
    'Research studies and compounds': '''PREFIX ex: <https://tattviki.example/enterprise/>
        SELECT ?study ?compound ?indication WHERE {
          ?study a ex:ResearchStudy ; ex:investigates ?compound ; ex:hasIndication ?indication .
        } ORDER BY ?study LIMIT 8''',
    'Applications and hosting servers': '''PREFIX ex: <https://tattviki.example/enterprise/>
        SELECT ?application ?server WHERE {
          ?application a ex:SoftwareAsset ; ex:hostedOn ?server .
        } ORDER BY ?application LIMIT 8''',
    'Study counts by compound': '''PREFIX ex: <https://tattviki.example/enterprise/>
        SELECT ?compound (COUNT(?study) AS ?studies) WHERE {
          ?study ex:investigates ?compound .
        } GROUP BY ?compound ORDER BY DESC(?studies) LIMIT 8''',
    'Provenance joins across studies and datasets': '''PREFIX ex: <https://tattviki.example/enterprise/>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        SELECT ?study ?dataset WHERE {
          ?study ex:usesDataset ?dataset .
          ?dataset prov:wasGeneratedBy ?study .
        } ORDER BY ?study LIMIT 8'''
}
print('Loaded',len(data),'RDF triples')
for name,query in queries.items():
    print('\n==',name,'==')
    results=list(data.query(query))
    for row in results:print(' | '.join(str(v).rsplit('/',1)[-1] for v in row))
    print('Rows shown:',len(results))
shapes = Graph().parse(ROOT/'shapes.ttl',format='turtle')
conforms,report_graph,report_text=validate(data_graph=data,shacl_graph=shapes,inference='rdfs',abort_on_first=False)
print('\nSHACL:', 'PASS' if conforms else 'FAIL')
if not conforms:
    print(report_text[:3500]);sys.exit(1)
