import unittest
from rdflib import Namespace
from rdflib.namespace import RDF, SKOS, DCTERMS, PROV
from generate import build
EX=Namespace('https://tattviki.example/enterprise/')

class EnterpriseLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph,cls.report=build()
    def test_mastering_reduces_duplicate_records(self):
        self.assertEqual(self.report['source_records'],11)
        self.assertEqual(self.report['golden_parties'],5)
    def test_unknown_identity_quarantined(self):
        self.assertEqual(len(self.report['requires_review']),1)
    def test_every_master_has_approved_status(self):
        for party in self.graph.subjects(RDF.type,EX.GoldenParty):
            self.assertTrue(list(self.graph.objects(party,EX.approvedStatus)))
    def test_controlled_codes_have_schemes(self):
        for code in self.graph.subjects(RDF.type,EX.ApprovedCode):
            self.assertIn((code,SKOS.inScheme,EX.PartyStatusScheme),self.graph)
    def test_catalog_contains_lineage(self):
        self.assertIn((EX['dataset-BI_CUSTOMERS'],PROV.wasDerivedFrom,EX['dataset-GOLDEN_PARTIES']),self.graph)
    def test_golden_record_identifier_unique(self):
        ids=[str(v) for p in self.graph.subjects(RDF.type,EX.GoldenParty) for v in self.graph.objects(p,DCTERMS.identifier)]
        self.assertEqual(len(ids),len(set(ids)))

if __name__=='__main__':unittest.main()
