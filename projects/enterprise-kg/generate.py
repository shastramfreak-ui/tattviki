"""Generate a reproducible synthetic enterprise RDF graph; no patient information."""
from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, RDFS, SKOS, XSD, OWL
from rdflib.namespace import DCTERMS, PROV

ROOT = Path(__file__).resolve().parent
EX = Namespace('https://tattviki.example/enterprise/')
g = Graph()
for prefix, namespace in [('ex', EX), ('skos',SKOS), ('dct',DCTERMS),('prov', PROV),('owl', OWL)]:
    g.bind(prefix, namespace)

for cls in ['Organization','ResearchStudy','Compound','Indication','SoftwareAsset','Server','Publication','Dataset','Researcher']:
    g.add((EX[cls], RDF.type, OWL.Class))
for predicate, label in [('investigates','investigates compound'),('hasIndication','has indication'),('ownedBy','owned by'),('hostedOn','hosted on'),('usesDataset','uses dataset'),('citesPublication','cites publication'),('maintainedBy','maintained by')]:
    g.add((EX[predicate], RDF.type, OWL.ObjectProperty))
    g.add((EX[predicate], RDFS.label, Literal(label, lang='en')))

for i in range(1,11):
    term=EX[f'Indication{i:02d}']
    g.add((term,RDF.type,SKOS.Concept))
    g.add((term,SKOS.prefLabel,Literal(f'Synthetic indication {i}',lang='en')))
    g.add((term,SKOS.inScheme,EX.IndicationScheme))
    if i>1: g.add((term,SKOS.broader,EX[f'Indication{(i-1)//2+1:02d}']))
g.add((EX.IndicationScheme,RDF.type,SKOS.ConceptScheme))
for i in range(1,16):
    asset=EX[f'Compound{i:02d}']
    g.add((asset,RDF.type,EX.Compound))
    g.add((asset,RDFS.label,Literal(f'Demonstration compound {i}',lang='en')))
for i in range(1,9):
    org=EX[f'Organization{i:02d}']
    g.add((org,RDF.type,EX.Organization))
    g.add((org,RDFS.label,Literal(f'Organization {i} (fictional)',lang='en')))
for i in range(1,51):
    study=EX[f'Study{i:03d}']
    g.add((study,RDF.type,EX.ResearchStudy))
    g.add((study,EX.identifier,Literal(f'SYN-{i:04d}')))
    g.add((study,RDFS.label,Literal(f'Fictional research study {i}',lang='en')))
    g.add((study,EX.investigates,EX[f'Compound{(i%15)+1:02d}']))
    g.add((study,EX.hasIndication,EX[f'Indication{(i%10)+1:02d}']))
    g.add((study,EX.ownedBy,EX[f'Organization{(i%8)+1:02d}']))
    g.add((study,DCTERMS.created,Literal(f'2025-{(i%12)+1:02d}-{(i%27)+1:02d}',datatype=XSD.date)))
for i in range(1,21):
    server=EX[f'Server{i:03d}']
    g.add((server,RDF.type,EX.Server))
    g.add((server,EX.identifier,Literal(f'SRV-{i:03d}')))
    g.add((server,EX.ownedBy,EX[f'Organization{(i%8)+1:02d}']))
for i in range(1,61):
    app=EX[f'Application{i:03d}']
    g.add((app,RDF.type,EX.SoftwareAsset))
    g.add((app,EX.identifier,Literal(f'APP-{i:03d}')))
    g.add((app,EX.hostedOn,EX[f'Server{(i%20)+1:03d}']))
    g.add((app,EX.ownedBy,EX[f'Organization{(i%8)+1:02d}']))
    g.add((app,RDFS.label,Literal(f'Synthetic application {i}',lang='en')))
for i in range(1,31):
    dataset=EX[f'Dataset{i:03d}']
    study=EX[f'Study{(i%50)+1:03d}']
    g.add((dataset,RDF.type,EX.Dataset))
    g.add((dataset,EX.identifier,Literal(f'DS-{i:03d}')))
    g.add((dataset,PROV.wasGeneratedBy,study))
    g.add((study,EX.usesDataset,dataset))
for i in range(1,26):
    publication=EX[f'Publication{i:03d}']
    g.add((publication,RDF.type,EX.Publication))
    g.add((publication,DCTERMS.title,Literal(f'Demonstration publication {i}',lang='en')))
    g.add((EX[f'Study{(i%50)+1:03d}'],EX.citesPublication,publication))

outfile=ROOT/'enterprise.ttl'
g.serialize(destination=outfile,format='turtle')
print(f'Generated {len(g)} triples in {outfile.name}')
