"""Deterministic research screening. No outreach or transaction execution."""
import math
from datetime import date
from statistics import median
from urllib.parse import urlparse
from vendor.dealcalc.mao import mao

COSTS = ('repairs_low', 'repairs_high', 'repair_contingency', 'buyer_profit',
         'holding_costs', 'closing_costs', 'selling_costs', 'assignment_fee',
         'wholesaler_costs', 'capital_exposure')
CHECKS = ('ownership', 'title', 'flood', 'assignment_rights', 'seller_disclosure',
          'buyer_disclosure', 'counsel_review', 'contact_eligibility')

def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
        raise ValueError(f'{name} must be a finite nonnegative number')
    return value

def sourced(evidence, today, days=30):
    if not isinstance(evidence, dict):
        return False
    try:
        age = (today - date.fromisoformat(evidence['observed_at'])).days
        url = urlparse(evidence['url'])
        return url.scheme in ('http', 'https') and bool(url.netloc) and 0 <= age <= days
    except (KeyError, ValueError, TypeError):
        return False

def screen(lead, buyers=(), today=None):
    today = today or date.today()
    if not lead.get('id') or not lead.get('address'):
        raise ValueError('lead needs id and address')
    blockers, warnings = [], []
    if lead.get('state') != 'TX' or lead.get('county') not in ('Harris', 'Fort Bend', 'Montgomery', 'Brazoria', 'Galveston'):
        blockers.append('outside configured Houston-area territory')
    if lead.get('seller_channel') == 'retail_inventory':
        blockers.append('retail inventory channel; wholesale acquisition edge unverified')
    if not sourced(lead.get('source'), today):
        blockers.append('missing or stale listing source')
    for key in ('sqft', 'asking_price'):
        if lead.get(key) is None:
            blockers.append(f'missing {key}')
        else:
            number(lead[key], key)
            if lead[key] <= 0: raise ValueError(f'{key} must be positive')
    costs = lead.get('assumptions', {})
    for key in COSTS:
        if costs.get(key) is None: blockers.append(f'missing assumption: {key}')
        else: number(costs[key], key)
    if all(costs.get(k) is not None for k in ('repairs_low', 'repairs_high')) and costs['repairs_low'] > costs['repairs_high']:
        raise ValueError('repairs_low exceeds repairs_high')
    for key in ('repair_evidence', 'cost_evidence'):
        if not sourced(lead.get(key), today): blockers.append(f'missing or stale {key}')
    if costs.get('capital_exposure') is not None and costs['capital_exposure'] > 0:
        blockers.append('capital exposure requires separate owner authorization')
    if lead.get('requires_acquisition') is not False:
        blockers.append('no-acquisition structure not verified')
    comps, seen = [], set()
    for c in lead.get('comps', []):
        identity = c.get('id')
        if not identity or identity in seen or identity == lead['id']: continue
        seen.add(identity)
        try:
            sale_age = (today - date.fromisoformat(c['sold_at'])).days
            good = (c.get('verified') is True and c.get('status') == 'sold'
                    and sourced(c.get('source'), today) and 0 <= sale_age <= 180
                    and c.get('zip') == lead.get('zip') and c.get('property_type') == lead.get('property_type')
                    and c.get('renovated') is True)
            p, s = number(c['sold_price'], 'sold_price'), number(c['sqft'], 'comp sqft')
            if good and p > 0 and s > 0 and lead.get('sqft') and .75 <= s / lead['sqft'] <= 1.25:
                comps.append(p / s)
        except KeyError: continue
    if len(comps) < 3: blockers.append('need three distinct verified recent renovated sold comps')
    checks = lead.get('checks', {})
    for key in CHECKS:
        check = checks.get(key, {})
        if check.get('verified') is not True or not sourced(check, today):
            blockers.append(f'unverified {key}')
    economics = None
    if len(comps) >= 3 and lead.get('sqft') and all(costs.get(k) is not None for k in COSTS):
        low, base, high = min(comps)*lead['sqft'], median(comps)*lead['sqft'], max(comps)*lead['sqft']
        # Comp range is a screening scenario range, not a statistical confidence interval.
        buyer_max = mao(low, costs['repairs_high'] + costs['repair_contingency'], rule_pct=100,
                        desired_profit=costs['buyer_profit'], holding_costs=costs['holding_costs'],
                        closing_costs=costs['closing_costs'] + costs['selling_costs'])['max_allowable_offer']
        max_contract = round(buyer_max - costs['assignment_fee'] - costs['wholesaler_costs'], 2)
        economics = {'arv_low': round(low,2), 'arv_base': round(base,2), 'arv_high': round(high,2),
                     'buyer_max_all_in_assignment_price': buyer_max, 'max_contract_price': max_contract,
                     'buyer_headroom_after_ask': round(buyer_max-lead.get('asking_price',0),2),
                     'headroom_after_target_fee_and_costs': round(buyer_max-lead.get('asking_price',0)-costs['assignment_fee']-costs['wholesaler_costs'],2),
                     'target_assignment_fee': costs['assignment_fee'],
                     'target_fee_net_of_wholesaler_costs': round(costs['assignment_fee']-costs['wholesaler_costs'],2)}
        if max_contract <= 0: blockers.append('nonpositive maximum contract price')
        if lead.get('asking_price') and lead['asking_price'] > max_contract:
            blockers.append('asking price exceeds conservative maximum contract price')
        if high > low * 1.25: blockers.append('comp dispersion needs analyst review')
        if costs['assignment_fee'] <= costs['wholesaler_costs']:
            blockers.append('target assignment fee does not cover wholesaler costs')
    matches = []
    if economics and lead.get('asking_price'):
        for b in buyers:
            if (b.get('verified') is True and sourced(b.get('proof_of_funds'), today)
                and lead.get('zip') in b.get('zips', []) and lead.get('property_type') in b.get('property_types', [])
                and number(b.get('max_price',0), 'buyer max price') >= lead['asking_price']+costs['assignment_fee']
                and number(b.get('max_repairs',0), 'buyer max repairs') >= costs['repairs_high']+costs['repair_contingency']):
                matches.append(b['id'])
    if not matches: blockers.append('no verified funded buyer match')
    warnings.append('Research output only; no offer, outreach, contract or guaranteed valuation')
    return {'lead_id': lead['id'], 'address': lead['address'], 'status': 'REVIEW_REQUIRED' if blockers else 'READY_FOR_OWNER_REVIEW',
            'as_of': today.isoformat(), 'accepted_comp_count': len(comps), 'economics': economics,
            'buyer_matches': matches, 'unpriced_comp_candidates': len(lead.get('comp_candidates', [])), 'parcel_research': lead.get('parcel_research'), 'blockers': blockers, 'warnings': warnings}
