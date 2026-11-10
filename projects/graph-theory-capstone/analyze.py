"""Tāttvikī — graph theory capstone. Fictional data only. Requires NetworkX."""
from pathlib import Path
import argparse, json
import networkx as nx
ROOT=Path(__file__).resolve().parents[2]

def load_graph(graph_id='graph-01'):
    data=json.loads((ROOT/'data/graph_examples.json').read_text(encoding='utf-8'))['graphs']
    case=next((g for g in data if g['id']==graph_id),None)
    if not case: raise ValueError(f'Unknown graph {graph_id}; options: '+', '.join(g['id'] for g in data))
    g=nx.MultiDiGraph()
    g.add_nodes_from((n['id'],n) for n in case['nodes'])
    for i,e in enumerate(case['edges']):
        g.add_edge(e['source'],e['target'],key=f'edge-{i}',weight=e['weight'],predicate=e['label'],source_note=e.get('sourceNote','synthetic'))
    return case,g

def report(graph_id='graph-01'):
    case,g=load_graph(graph_id)
    ids=list(g.nodes)
    source,target=ids[0],ids[9]
    try: hops=nx.shortest_path(g,source,target)
    except nx.NetworkXNoPath:hops=[]
    try: cost=nx.dijkstra_path_length(g,source,target,weight='weight')
    except nx.NetworkXNoPath:cost=None
    # Explicitly unweighted PageRank; parallel edges remain distinct contributions.
    pr=nx.pagerank(g,alpha=.85,weight=None)
    degree=dict(g.degree())
    return {
        'example':case['title'], 'id':case['id'], 'fictional':True,
        'nodes':g.number_of_nodes(),'directed_edges':g.number_of_edges(),
        'weak_components':nx.number_weakly_connected_components(g),
        'acyclic':nx.is_directed_acyclic_graph(g),
        'start':source, 'target':target,'bfs_path':hops, 'dijkstra_cost':cost,
        'top_degree':sorted(degree.items(),key=lambda x:(-x[1],x[0]))[:5],
        'top_pagerank':sorted(pr.items(),key=lambda x:(-x[1],x[0]))[:5],
        'interpretation':['BFS minimizes directed hops, not edge weight.',
            'Dijkstra assumes nonnegative weights; weights here are unitless teaching costs.',
            'PageRank is an illustrative connectivity score, not authority or factual correctness.',
            'These are fictional graphs; no operational recommendations should be derived.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--graph',default='graph-01',help='graph-01 through graph-12')
    a=parser.parse_args()
    print(json.dumps(report(a.graph),indent=2))
