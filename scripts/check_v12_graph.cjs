const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const graphs=JSON.parse(fs.readFileSync('data/graph_examples.json','utf8')).graphs;
const scope={window:{TATTVIKI_GRAPH_EXAMPLES:graphs}};vm.createContext(scope);
vm.runInContext(fs.readFileSync('assets/graph-lab.js','utf8'),scope);
const a=scope.window.TattvikiGraphLab.algorithms;
assert.equal(graphs.length,12);
let nodes=0,edges=0;
for(const g of graphs){
  const ids=new Set(g.nodes.map(n=>n.id));assert.equal(ids.size,g.nodes.length);
  assert(g.nodes.length>=25);assert(g.edges.length>=40);
  const keys=new Set();
  for(const e of g.edges){assert(ids.has(e.source)&&ids.has(e.target));assert(Number.isFinite(e.weight)&&e.weight>=0);const key=[e.source,e.target,e.label].join('|');assert(!keys.has(key));keys.add(key);}
  const b=a.bfs(g,g.nodes[0].id,g.nodes[9].id),d=a.dijkstra(g,g.nodes[0].id,g.nodes[9].id);
  if(b.path.length){assert.equal(b.path[0],g.nodes[0].id);assert.equal(b.path.at(-1),g.nodes[9].id);}
  if(d.path.length){assert.equal(d.path[0],g.nodes[0].id);assert.equal(d.path.at(-1),g.nodes[9].id);}
  const components=a.components(g).groups;assert.equal(new Set(components.flat()).size,g.nodes.length);
  const ranks=a.pagerank(g).ranking;assert.equal(ranks.length,g.nodes.length);assert(Math.abs(ranks.reduce((s,x)=>s+x.value,0)-1)<1e-7);
  const deg=a.degree(g).ranking;assert.equal(deg.length,g.nodes.length);assert.equal(deg.reduce((s,x)=>s+x.value,0),2*g.edges.length);
  nodes+=g.nodes.length;edges+=g.edges.length;
}
assert.equal(nodes,360);assert.equal(edges,616);
console.log(`PASS 12 curated synthetic multigraphs: ${nodes} nodes, ${edges} edges; BFS, Dijkstra, components, degree and PageRank sanity checks`);
