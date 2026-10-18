"""Original synthetic lab: metadata catalog + RDM + MDM + lineage to a semantic graph."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, PROV, XSD

ROOT = Path(__file__).parent
DATA = ROOT / 'data'
OUTPUT = ROOT / 'output'
EX = Namespace('https://tattviki.example/enterprise/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')

def rows(filename):
    with (DATA / filename).open(encoding='utf8', newline='') as file:
        return list(csv.DictReader(file))

def iri_segment(text):
    return re.sub(r'[^A-Za-z0-9_-]', '_', str(text))

def normalize(text):
    return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode('ascii').casefold()).strip()

def registration_id(source):
    """Educational deterministic identity rule; production needs stewarded probabilistic review."""
    key = (source.get('registration_key') or '').strip().upper()
    if not key: return None
    return 'M-' + hashlib.sha256(key.encode()).hexdigest()[:12].upper()

def build(break_shape=False):
    graph = Graph()
    for prefix, uri in [('ex',EX),('skos',SKOS),('dct',DCTERMS),('prov',PROV),('dcat',DCAT)]: graph.bind(prefix,uri)
    graph.add((EX.PartyStatusScheme,RDF.type,SKOS.ConceptScheme))
    graph.add((EX.PartyStatusScheme,SKOS.prefLabel,Literal('Party status',lang='en')))
    mapping={}; statuses={}; unmapped_codes=[]
    for r in rows('status_reference.csv'):
        code = r['canonical_code']
        status=EX['status-'+code]
        mapping[(r['source'],r['local_code'])]=status
        statuses[code]=status
        graph.add((status,RDF.type,SKOS.Concept))
        graph.add((status,RDF.type,EX.ApprovedCode))
        graph.add((status,SKOS.inScheme,EX.PartyStatusScheme))
        graph.add((status,SKOS.prefLabel,Literal(r['approved_label'],lang='en')))
        graph.add((status,DCTERMS.hasVersion,Literal(r['version'])))
        source_code=EX['code-'+iri_segment(r['source'])+'-'+iri_segment(r['local_code'])]
        graph.add((source_code,RDF.type,SKOS.Concept))
        graph.add((source_code,SKOS.exactMatch,status))
        graph.add((source_code,SKOS.notation,Literal(r['local_code'])))
        graph.add((source_code,SKOS.prefLabel,Literal(r['local_code'])))

    groups=defaultdict(list); unmatchable=[]
    for system,filename in [('CRM','crm_parties.csv'),('ERP','erp_parties.csv')]:
        for r in rows(filename):
            rid=EX['source-'+system+'-'+iri_segment(r['source_id'])]
            graph.add((rid,RDF.type,EX.SourcePartyRecord))
            graph.add((rid,DCTERMS.identifier,Literal(r['source_id'])))
            graph.add((rid,EX.sourceSystem,Literal(system)))
            graph.add((rid,RDFS.label,Literal(r.get('display_name') or r.get('legal_name'))))
            canonical_status=mapping.get((system,r.get('status_code') or r.get('state_code')))
            if canonical_status: graph.add((rid,EX.normalizedStatus,canonical_status))
            else: unmapped_codes.append({'system':system,'source_id':r['source_id'],'code':r.get('status_code') or r.get('state_code'),'reason':'RDM mapping missing; review required'})
            master=registration_id(r)
            if master: groups[master].append((system,r,rid,canonical_status))
            else: unmatchable.append({'system':system,'source_id':r['source_id'],'reason':'No registration key; routed for steward review'})
    # One golden record per deterministic registration key. Do not assume name equality proves identity.
    for master_id, sources in sorted(groups.items()):
        master=EX['master-'+master_id]
        graph.add((master,RDF.type,EX.GoldenParty))
        graph.add((master,DCTERMS.identifier,Literal(master_id)))
        preferred=sorted(sources,key=lambda row: (row[0]!='ERP',row[1]['source_id']))[0]
        graph.add((master,RDFS.label,Literal(preferred[1].get('legal_name') or preferred[1].get('display_name'))))
        chosen_status=preferred[3]
        if chosen_status: graph.add((master,EX.approvedStatus,chosen_status))
        for sys,row,rid,status in sources:
            graph.add((master,EX.sourceRecord,rid))
            graph.add((master,PROV.wasDerivedFrom,rid))
            if status and status!=chosen_status:
                graph.add((master,EX.conflictingSourceStatus,status))
        graph.add((master,EX.survivorshipPolicy,Literal('ERP-first for legal name and party status; review disagreements')))
    # Dataset catalog descriptions use DCAT, rights links, ownership, and machine-usable lineage.
    for r in rows('catalog.csv'):
        dataset=EX['dataset-'+iri_segment(r['asset_id'])]
        graph.add((dataset,RDF.type,DCAT.Dataset))
        graph.add((dataset,RDF.type,EX.CatalogAsset))
        graph.add((dataset,DCTERMS.identifier,Literal(r['asset_id'])))
        graph.add((dataset,DCTERMS.title,Literal(r['title'])))
        graph.add((dataset,DCTERMS.license,URIRef(r['license'])))
        team=EX['team-'+iri_segment(r['owner_team'])]
        graph.add((dataset,EX.ownedByTeam,team))
        graph.add((team,RDFS.label,Literal(r['owner_team'])))
        graph.add((dataset,EX.classification,Literal(r['classification'])))
        graph.add((dataset,EX.sourceSystem,Literal(r['source_system'])))
        column=EX['column-'+iri_segment(r['asset_id'])+'-'+iri_segment(r['source_column'])]
        graph.add((dataset,EX.hasColumn,column))
        graph.add((column,RDFS.label,Literal(r['source_column'])))
    for r in rows('lineage.csv'):
        src=EX['dataset-'+iri_segment(r['source_asset'])]
        dst=EX['dataset-'+iri_segment(r['target_asset'])]
        activity=EX['run-'+iri_segment(r['source_asset'])+'-to-'+iri_segment(r['target_asset'])]
        graph.add((activity,RDF.type,PROV.Activity))
        graph.add((activity,PROV.used,src))
        graph.add((dst,PROV.wasGeneratedBy,activity))
        graph.add((dst,PROV.wasDerivedFrom,src))
        graph.add((activity,RDFS.label,Literal(r['transformation'])))
        src_col=EX['column-'+iri_segment(r['source_asset'])+'-'+iri_segment(r['source_column'])]
        dst_col=EX['column-'+iri_segment(r['target_asset'])+'-'+iri_segment(r['target_column'])]
        graph.add((dst_col,PROV.wasDerivedFrom,src_col))
    if break_shape:
        affected=next(iter(graph.subjects(RDF.type,EX.GoldenParty)))
        graph.remove((affected,EX.approvedStatus,None))
    return graph, {'source_records':len(rows('crm_parties.csv'))+len(rows('erp_parties.csv')),
                   'golden_parties':len(groups),'requires_review':unmatchable,
                   'unmapped_codes':unmapped_codes,
                   'status_codes':len(statuses),'triples':len(graph)}

def main():
    OUTPUT.mkdir(exist_ok=True)
    bad='--break-shape' in sys.argv
    graph,report=build(bad)
    path=OUTPUT / ('enterprise-invalid.ttl' if bad else 'enterprise.ttl')
    graph.serialize(destination=path,format='turtle')
    (OUTPUT/'quality_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report,indent=2))
    print('Wrote',path)
    try:
        from pyshacl import validate
    except ImportError:
        print('pyshacl missing: install pip install -r requirements.txt for full SHACL validation')
        return 2
    shape_graph=Graph().parse(ROOT/'shapes.ttl',format='turtle')
    conforms,results,report_text=validate(graph,shacl_graph=shape_graph,inference='rdfs')
    (OUTPUT/'shacl-report.txt').write_text(report_text,encoding='utf8')
    print('SHACL conforms:',conforms)
    print(report_text[:1800])
    return 1 if not conforms else 0

if __name__=='__main__':raise SystemExit(main())
