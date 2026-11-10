import unittest
from analyze import report,load_graph
import networkx as nx
class CapstoneTests(unittest.TestCase):
 def test_all_graphs_are_nonempty_and_valid(self):
  for i in range(1,13):
   case,g=load_graph(f'graph-{i:02d}')
   with self.subTest(case=case['title']):
    self.assertEqual(g.number_of_nodes(),30)
    self.assertGreaterEqual(g.number_of_edges(),50)
    self.assertTrue(all(e['weight']>=0 for e in case['edges']))
 def test_report_correctness(self):
  r=report('graph-02')
  self.assertEqual(r['nodes'],30)
  self.assertEqual(len(r['top_pagerank']),5)
  self.assertTrue(r['fictional'])
 def test_cycle_reporting_matches_graph_theory(self):
  for i in range(1,13):
   _,g=load_graph(f'graph-{i:02d}')
   self.assertEqual(report(f'graph-{i:02d}')['acyclic'],nx.is_directed_acyclic_graph(g))
if __name__=='__main__':unittest.main()
