from pathlib import Path
from rdflib import Graph
ROOT=Path(__file__).parent
p=ROOT/'output/enterprise.ttl'
if not p.exists():
    raise SystemExit('Run python generate.py first')
g=Graph().parse(p,format='turtle')
for queryfile in sorted((ROOT/'queries').glob('*.rq')):
    print('\n###',queryfile.name)
    for row in g.query(queryfile.read_text(encoding='utf8')):
        print(' | '.join(str(v) for v in row))
