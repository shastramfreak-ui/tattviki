"""Independent dataset/shape syntax and quality fixtures.

RDFLib parsing works offline. The optional pySHACL test is enabled when installed.
"""
import unittest
from pathlib import Path
from rdflib import Graph, Namespace, RDF

HERE = Path(__file__).resolve().parent
FIX = HERE / 'fixtures'
SH = Namespace('http://www.w3.org/ns/shacl#')

class Fixtures(unittest.TestCase):
    def test_all_turtle_parses(self):
        files = sorted(FIX.glob('*.ttl'))
        self.assertEqual(len(files), 18)
        for path in files:
            with self.subTest(path=path.name):
                graph = Graph().parse(path, format='turtle')
                self.assertGreater(len(graph), 0)

    def test_shapes_have_targets_and_property_constraints(self):
        paths = sorted(FIX.glob('*_shapes.ttl'))
        self.assertEqual(len(paths), 6)
        for path in paths:
            with self.subTest(path=path.name):
                g = Graph().parse(path, format='turtle')
                shapes = list(g.subjects(RDF.type, SH.NodeShape))
                self.assertTrue(shapes)
                for s in shapes:
                    self.assertTrue(any(g.objects(s, SH.targetClass)))
                    for prop in g.objects(s, SH.property):
                        self.assertTrue(any(g.objects(prop, SH.path)))

    def test_good_and_bad_are_distinct(self):
        for s in ['people','catalog','reference','lineage','retail','sensors']:
            with self.subTest(scenario=s):
                a = Graph().parse(FIX / f'{s}_good.ttl', format='turtle')
                b = Graph().parse(FIX / f'{s}_bad.ttl', format='turtle')
                self.assertNotEqual(set(a), set(b))

    @unittest.skipUnless(__import__('importlib').util.find_spec('pyshacl'), 'pySHACL needs network installation')
    def test_full_pyshacl_pairs(self):
        from validate import run
        for s in ['people','catalog','reference','lineage','retail','sensors']:
            for variant, expected in [('good',True),('bad',False)]:
                with self.subTest(scenario=s,variant=variant):
                    conforms, results, _ = run(s, variant)
                    self.assertEqual(conforms, expected)
                    if variant == 'bad': self.assertGreaterEqual(len(results), 1)

if __name__ == '__main__': unittest.main()
