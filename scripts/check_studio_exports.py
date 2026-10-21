"""Check generated ontology interoperability using RDFLib. Not an OWL reasoner."""
from pathlib import Path
from rdflib import Graph, URIRef, RDF, RDFS, OWL, Namespace
root=Path(__file__).resolve().parent.parent / 'projects' / 'ontology-studio'
formats={'enterprise-ontology.ttl':'turtle','enterprise-ontology.rdf':'xml','enterprise-ontology.jsonld':'json-ld'}
graphs=[]
for fn,fmt in formats.items():
    graph=Graph();graph.parse(str(root/fn),format=fmt)
    assert len(graph)>=500,(fn,len(graph))
    graphs.append(graph)
    print('Valid',fmt,fn,len(graph),'triples')
for graph in graphs[1:]:
    assert graphs[0].isomorphic(graph),'Ontology serialization mismatch'
NS=Namespace('https://example.org/tattviki/enterprise#')
g=graphs[0]
assert (NS.CuratedDataset,RDFS.subClassOf,NS.Dataset) in g
assert (NS.Dataset,RDF.type,OWL.Class) in g
assert (NS.Customer360,NS.hasContract,NS.ContractV1) in g
from rdflib.namespace import SKOS, SH
assert (NS.Approved,SKOS.prefLabel,None) in g
assert (NS.PartyMasterShape,RDF.type,SH.NodeShape) in g
q='''PREFIX ex: <https://example.org/tattviki/enterprise#>
SELECT ?source WHERE { ex:CuratedParties ex:derivedFrom ?source . } ORDER BY ?source'''
rows=list(g.query(q)); assert len(rows)==2,rows
print('All ontology exports match; SPARQL lineage joins verified:',len(rows))
