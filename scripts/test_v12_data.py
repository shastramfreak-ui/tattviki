"""Independent semantic graph data checks and algorithm checks against NetworkX."""
from pathlib import Path
import json,subprocess,csv,math
import networkx as nx
from rdflib import Graph
ROOT=Path(__file__).resolve().parents[1]
examples=json.loads((ROOT/'data/graph_examples.json').read_text())['graphs']
assert len(examples)==12
all_nodes=all_edges=0
for g in examples:
 ids=[n['id'] for n in g['nodes']]; idset=set(ids)
 assert len(ids)==len(idset), f'duplicate node IDs in {g["id"]}'
 assert all(n['type'] and n['label'] for n in g['nodes'])
 edgekeys=set()
 for e in g['edges']:
  assert e['source'] in idset and e['target'] in idset, f'dangling endpoint {e}'
  assert e['source']!=e['target'], f'unexpected self loop {e}'
  assert type(e['weight']) in (int,float) and math.isfinite(e['weight']) and e['weight']>=0
  key=(e['source'],e['target'],e['label']);assert key not in edgekeys,f'duplicate edge {key}'
  edgekeys.add(key)
 all_nodes+=len(ids);all_edges+=len(g['edges'])
 assert len(ids)>=25 and len(g['edges'])>=40
 assert g['weightUnit']=='unitless tutorial cost'
# JS calculations cross-check with a widely used graph library, not just known fixtures.
js=r'''const fs=require('fs'),vm=require('vm');const data=JSON.parse(fs.readFileSync('data/graph_examples.json','utf8')).graphs;const ctx={window:{TATTVIKI_GRAPH_EXAMPLES:data}};vm.createContext(ctx);vm.runInContext(fs.readFileSync('assets/graph-lab.js','utf8'),ctx);const alg=ctx.window.TattvikiGraphLab.algorithms;const o=data.map(g=>{const s=g.nodes[0].id,t=g.nodes[9].id;return {id:g.id,bfs:alg.bfs(g,s,t).path,dijkstra:alg.dijkstra(g,s,t),components:alg.components(g).groups.map(a=>a.sort()).sort((a,b)=>a[0].localeCompare(b[0])),degree:alg.degree(g).ranking,rank:alg.pagerank(g).ranking,topo:alg.topo(g)};});process.stdout.write(JSON.stringify(o));'''
out=json.loads(subprocess.check_output(['node','-e',js],cwd=ROOT,text=True))
for g,r in zip(examples,out):
 G=nx.MultiDiGraph();G.add_nodes_from(x['id'] for x in g['nodes']);G.add_weighted_edges_from((e['source'],e['target'],e['weight']) for e in g['edges'])
 # At most one edge between each ordered pair on supplied teaching datasets
 assert G.number_of_edges()==len(g['edges'])
 a,b=g['nodes'][0]['id'],g['nodes'][9]['id']
 try:ref=nx.shortest_path_length(G,a,b);assert len(r['bfs'])-1==ref
 except nx.NetworkXNoPath:assert r['bfs']==[]
 try:cost=nx.dijkstra_path_length(G,a,b);assert abs(r['dijkstra']['cost']-cost)<1e-8
 except nx.NetworkXNoPath:assert r['dijkstra']['path']==[]
 assert sorted([sorted(x) for x in nx.weakly_connected_components(G)])==r['components']
 d={x['id']:x['value'] for x in r['degree']};assert all(d[n]==G.in_degree(n)+G.out_degree(n) for n in G)
 assert sum(x['value'] for x in r['rank'])==__import__('pytest').approx(1,abs=.0001)
 nr=nx.pagerank(G,alpha=.85,weight=None,max_iter=1000,tol=1e-12)
 assert all(abs(nr[x['id']]-x['value'])<.002 for x in r['rank'])
 assert r['topo']['cycle']==(not nx.is_directed_acyclic_graph(G))
 if not r['topo']['cycle']:
  order=r['topo']['order'];pos={v:i for i,v in enumerate(order)}
  assert all(pos[a]<pos[b] for a,b in G.edges())
print('PASS',len(examples),'independent graph comparisons,',all_nodes,'nodes,',all_edges,'directed edges')
# Standards-based RDF fixtures still parse
ttl=list(ROOT.glob('projects/**/*.ttl'))
for f in ttl:
 G=Graph();G.parse(str(f),format='turtle');assert len(G)>0, f'empty Turtle graph {f}'
print('PASS',len(ttl),'RDF/Turtle files parsed, nonempty')
# Check 707-topic CSV agrees with compiled lessons
rows=list(csv.DictReader((ROOT/'CURRICULUM_INDEX.csv').open(encoding='utf-8')))
assert len(rows)==707 and len({r['id'] for r in rows})==707
new=json.loads((ROOT/'data/graph_curriculum.json').read_text())['lessons']
assert all(any(r['id']==x['id'] and r['title']==x['title'] for r in rows) for x in new)
print('PASS',len(rows),'unique curriculum entries and 42 distinct new lesson titles')
