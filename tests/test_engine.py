import copy
import json
import math
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from wholesale.engine import screen

TODAY = date(2026, 10, 1)
EVIDENCE = {'url':'https://example.org/test-evidence', 'observed_at':'2026-10-01', 'verified':True}

def fixture():
    return {'id':'synthetic-subject','address':'SYNTHETIC TEST ONLY','state':'TX','county':'Harris','zip':'77044','property_type':'single_family','sqft':1000,'asking_price':95000,
            'source':dict(EVIDENCE),'requires_acquisition':False,
            'assumptions':dict(repairs_low=20000, repairs_high=30000, repair_contingency=5000, buyer_profit=40000, holding_costs=5000, closing_costs=5000, selling_costs=10000, assignment_fee=10000, wholesaler_costs=2000, capital_exposure=0),
            'repair_evidence':dict(EVIDENCE),'cost_evidence':dict(EVIDENCE),
            'checks':{k:dict(EVIDENCE) for k in ('ownership','title','flood','assignment_rights','seller_disclosure','buyer_disclosure','counsel_review','contact_eligibility')},
            'comps':[dict(id=f'c{i}',sold_price=200000+i*5000,sqft=1000,status='sold',sold_at='2026-09-01',zip='77044',property_type='single_family',renovated=True,verified=True,source=dict(EVIDENCE)) for i in range(3)]}

BUYERS = [{'id':'synthetic-buyer','verified':True,'proof_of_funds':dict(EVIDENCE),'zips':['77044'],'property_types':['single_family'],'max_price':200000,'max_repairs':100000}]

class EngineTests(unittest.TestCase):
    def test_explicit_economics_and_owner_boundary(self):
        r=screen(fixture(),BUYERS,TODAY)
        self.assertEqual(r['economics']['max_contract_price'],93000)
        self.assertEqual(r['economics']['buyer_headroom_after_ask'],10000)
        self.assertEqual(r['economics']['headroom_after_target_fee_and_costs'],-2000)
        self.assertEqual(r['economics']['target_fee_net_of_wholesaler_costs'],8000)
        self.assertIn('asking price exceeds conservative maximum contract price',r['blockers'])
        d=fixture(); d['asking_price']=85000
        self.assertEqual(screen(d,BUYERS,TODAY)['status'],'READY_FOR_OWNER_REVIEW')
    def test_fee_must_cover_wholesaler_costs(self):
        d=fixture();d['asking_price']=85000;d['assumptions']['assignment_fee']=1000
        self.assertIn('target assignment fee does not cover wholesaler costs', screen(d,BUYERS,TODAY)['blockers'])
    def test_sold_price_ranges_never_count_as_exact_comps(self):
        d=fixture();d['comps']=[];d['comp_candidates']=[{'sold_price_range':[250001,285000]}]*3
        r=screen(d,BUYERS,TODAY)
        self.assertEqual(r['unpriced_comp_candidates'],3)
        self.assertEqual(r['accepted_comp_count'],0)
        self.assertIsNone(r['economics'])
    def test_missing_data_not_qualified(self):
        self.assertIsNone(screen({'id':'x','address':'x'},today=TODAY)['economics'])
    def test_duplicate_active_stale_wrong_zip_comps(self):
        for mutation in ({'id':'c0'},{'status':'active'},{'sold_at':'2020-01-01'},{'zip':'99999'}):
            d=fixture();d['comps'][1].update(mutation)
            self.assertEqual(screen(d,BUYERS,TODAY)['accepted_comp_count'],2)
    def test_capital_and_unverified_buyer_block(self):
        d=fixture();d['assumptions']['capital_exposure']=100
        r=screen(d,[],TODAY)
        self.assertIn('capital exposure requires separate owner authorization',r['blockers'])
        self.assertIn('no verified funded buyer match',r['blockers'])
    def test_nonfinite_negative_boolean_rejected(self):
        for v in (math.nan,math.inf,-1,True):
            d=fixture();d['assumptions']['buyer_profit']=v
            with self.assertRaises(ValueError):screen(d,BUYERS,TODAY)
    def test_false_stale_or_future_evidence_blocks(self):
        for value in ({'verified':False},{'observed_at':'2020-01-01'},{'observed_at':'2027-01-01'}):
            d=fixture();d['checks']['title'].update(value)
            self.assertIn('unverified title',screen(d,BUYERS,TODAY)['blockers'])
    def test_cli_append_audit(self):
        import sqlite3
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'input.json').write_text(json.dumps([{'id':'x','address':'x'}]))
            command=[sys.executable,'-m','wholesale',str(p/'input.json'),'--db',str(p/'audit.sqlite'),'--output',str(p/'out.json')]
            for _ in range(2):subprocess.run(command,check=True,capture_output=True)
            with sqlite3.connect(p/'audit.sqlite') as db:self.assertEqual(db.execute('SELECT count(*) FROM events').fetchone()[0],2)

if __name__=='__main__':unittest.main()
