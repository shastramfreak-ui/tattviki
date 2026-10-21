"""Isolated optional OWL DL classification worker, invoked with an explicit 45-second timeout.
No owl:imports resolution: input imports are removed before classification.
Requires: pip install -r backend/requirements-dl.txt; a Java runtime on PATH.
"""
import json
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
from rdflib import Graph, OWL
from owlready2 import World, sync_reasoner

raw=sys.stdin.read(600_001)
g=Graph().parse(data=raw,format='turtle')
for tr in list(g.triples((None,OWL.imports,None))): g.remove(tr)
original=set(g)
with TemporaryDirectory(prefix='tattviki-hermit-') as tmp:
    source=Path(tmp)/'ontology.rdf'
    g.serialize(destination=str(source),format='xml')
    world=World()
    onto=world.get_ontology(source.as_uri()).load()
    sync_reasoner([onto],infer_property_values=False,debug=0)
    after=world.as_rdflib_graph()
    changed=sorted((tr for tr in after if tr not in original),key=lambda tr:tuple(map(str,tr)))
    rows=[[x.n3() for x in tr] for tr in changed[:300]]
    print(json.dumps({'mode':'hermit','asserted':len(original),'inferred_count':len(changed),'shown':len(rows),'new_triples':rows,'note':'Experimental Owlready2/HermiT classification (Java); generated materialization may vary by backend. Imports disabled.'}))
