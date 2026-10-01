"""Read-only enrichment from the Harris County public HCAD GIS parcel service."""
import json
import re
from datetime import date
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = 'https://www.gis.hctx.net/arcgis/rest/services/HCAD/Parcels/MapServer/0/query'
FIELDS = 'acct_num,tax_year,owner_name_1,site_str_num,site_str_name,site_zip,total_appraised_val,total_market_val,new_owner_date,activeAccount_flag'

def lookup(account, address, zip_code, opener=urlopen, today=None):
    if not re.fullmatch(r'\d{13}', account):
        raise ValueError('HCAD account must contain 13 digits')
    if not re.fullmatch(r'\d{5}', zip_code):
        raise ValueError('ZIP must contain 5 digits')
    match = re.fullmatch(r'\s*(\d+)\s+([A-Za-z\s]+?)\s+(?:Dr|Drive|St|Street|Ln|Lane|Ct|Court|Rd|Road)?\s*(?:,.*)?', address, re.I)
    if not match:
        raise ValueError('address needs street number and name')
    number, street = match.group(1), re.sub(r'[^A-Z]', '', match.group(2).upper())
    params = {'where':f"acct_num='{account}'",'outFields':FIELDS,'returnGeometry':'false','f':'json'}
    url = BASE + '?' + urlencode(params)
    with opener(url, timeout=10) as response:
        payload = json.load(response)
    features = payload.get('features', [])
    if len(features) != 1:
        raise ValueError('HCAD account did not resolve uniquely')
    record = features[0]['attributes']
    official_street = re.sub(r'[^A-Z]', '', (record.get('site_str_name') or '').upper())
    if str(record.get('acct_num')) != account or str(record.get('site_str_num')) != number or official_street != street or str(record.get('site_zip'))[:5] != zip_code:
        raise ValueError('HCAD account address mismatch')
    return {'account':account,'tax_year':record.get('tax_year'),'tax_roll_owner':record.get('owner_name_1'),
            'appraised_value':record.get('total_appraised_val'),'market_value':record.get('total_market_val'),
            'active_account':record.get('activeAccount_flag') == 'Y',
            'source':{'url':url,'observed_at':(today or date.today()).isoformat()},
            'note':'Tax-roll ownership and assessed values are informational; verify deed, title, and sale comps independently.'}
