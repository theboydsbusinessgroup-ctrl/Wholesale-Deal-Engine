import io
import json
import unittest
from datetime import date
from wholesale.hcad import lookup

class FakeResponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self,*args): self.close()

def opener_with(**changes):
    def opener(url, timeout):
        assert 'acct_num%3D%27' in url and timeout == 10
        row={'acct_num':'1111070000003','tax_year':'2026','owner_name_1':'TEST ENTITY','site_str_num':12011,'site_str_name':'GREENCANYON','site_zip':'77044','total_appraised_val':98898,'total_market_val':98898,'activeAccount_flag':'Y'}
        row.update(changes)
        return FakeResponse(json.dumps({'features':[{'attributes':row}]}).encode())
    return opener

class HcadTests(unittest.TestCase):
    def test_exact_account_address_zip_and_source(self):
        result=lookup('1111070000003','12011 Greencanyon Dr, Houston, TX 77044','77044',opener_with(),date(2026,10,1))
        self.assertEqual(result['tax_roll_owner'],'TEST ENTITY')
        self.assertEqual(result['tax_year'],'2026')
        self.assertNotIn('verified',result)
    def test_mismatched_account_or_address_rejected(self):
        for field in ({'site_str_num':12012},{'site_zip':'77045'},{'acct_num':'1111070000004'}):
            with self.assertRaises(ValueError):
                lookup('1111070000003','12011 Greencanyon Dr, Houston, TX 77044','77044',opener_with(**field))
    def test_bad_account_rejected_before_request(self):
        with self.assertRaises(ValueError):lookup('1111','12011 Greencanyon Dr','77044',opener_with())

if __name__=='__main__':unittest.main()
