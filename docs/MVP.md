# Research MVP — 2026-10-01

## Implemented
- JSON batch lead intake, provenance and freshness checks.
- Houston-area county allowlist; does not implement a geographic radius.
- Three distinct verified renovated closed sales, same ZIP/type, within 180 days and 25% of subject size. These are basic filters; an analyst must still review location, condition and adjustments.
- Low/base/high comp-price-per-square-foot scenarios. These are not statistical confidence intervals or appraisals.
- Conservative explicit MAO: low ARV less high repairs, repair contingency, buyer profit, holding, closing and selling costs, target assignment fee and wholesaler costs. The buyer price test uses asking price plus assignment fee; wholesaler costs reduce fee net, not buyer purchase price. Fee headroom is distinguished from actual fee income.
- Buyer fit with evidence of funds, ZIP/type, price and repair criteria.
- Unknown/stale evidence blocks readiness. Positive capital exposure requires separate authorization.
- Research results and input snapshots appended to SQLite with hashes.

## Input
See examples/houston-public-lead.json. Assumptions must include every COSTS field listed in wholesale/engine.py; zero must be explicit. All currency is USD. `repairs_low <= repairs_high`. Cost evidence should link to an accessible reviewed budget; repair evidence to an inspection or estimate. A source object has `url` and ISO `observed_at`. Checked evidence additionally has `verified: true`. Evidence freshness is 30 days.

Comps need id, sold_price, sqft, sold_at, status=sold, ZIP, property_type, renovated=true, verified=true and source. No asking price can serve as a sold comp. Buyers need id, verified=true, proof_of_funds source object, zips, property_types, max_price and max_repairs.

Checks: ownership, title, flood, assignment_rights, seller_disclosure, buyer_disclosure, counsel_review, contact_eligibility. These are operator attestations with references, not automatic legal determinations. Requires_acquisition must be false; capital_exposure defaults to unknown and must be explicitly supplied. Unknown earnest money or option liabilities cannot be assumed zero.

## First actual run
12011 Greencanyon Dr, Houston, TX 77044; HAR MLS 60157671. Retrieved 2026-10-01. HAR showed active at $119,999, 1,136 square feet. HCAD GIS account 1111070000003 matches street and ZIP; tax year 2026 shows SWE CASAS LLC, active, $98,898 assessed/market value. This is a tax-roll record, not a deed or sales comp. SWE Homes directly markets the property with owner financing, so the lead is deprioritized as retail inventory. The two public listing prices reflect different financing terms; no wholesale discount is evidenced. This is a public listed research candidate, not an off-market lead. No verified sold comps, repair budget, ownership/title evidence, contract/disclosures, capital obligations or verified buyer were available. Result: REVIEW_REQUIRED, economics=null. Unknowns remain unknown.

## Remaining production work
Approved repeatable discovery adapters, parcel/ownership enrichment, authorized closed-sale data, condition/flood/title review, private buyer CRM, stage transitions, approved contracts/disclosures, outreach eligibility and owner approvals. No scheduler, hosted API or live Jarvis telemetry is installed by this MVP. Existing telemetry adapter remains separate; Jarvis cannot block local execution.

Next useful action: prioritize a new seller-direct research candidate; retain Greencanyon as a low-priority control case. For any candidate, obtain three recent comparable closed sales plus a repair estimate. Re-screen with a funded buyer; reject if conservative economics do not fit. Synthetic unit tests exercise complete calculations but are not real deal evidence.

## Texas source check
TREC source retrieved 2026-10-01: https://www.trec.texas.gov/article/sale-equitable-interests-real-estate-clarified (published 2017-07-07). It distinguishes accurately marketing a contractual interest from offering property one does not own. This source alone is not a full current-law review. The earlier claim about wholesale-specific additional 2026 rules was not established during this session; do not use that claim as an implemented rule. Counsel review remains required by the original architecture before production transactions.

## GitHub-first preflight
Query: site:github.com real estate underwriting python wholesale calculator.
Reviewed dealcalcpro2026/dealcalc-core at 876db9c4fcc0ad7275d3fd58e72cda12cbe6d4e1: MIT, pure arithmetic, minimal maintenance history. Used its MAO function with rule_pct=100 and explicit costs; retained license and provenance. No paid service, MCP dependency, installer or external inference required. Other institutional commercial underwriting candidates do not fit this single-family assignment screening task.

Public HCAD assessment data can enrich parcel attributes but cannot substitute for verified renovated closed-sale prices. Github-first candidates reviewed: RafaelPinto/hcad_pred (appraisal data), mosswild/res_prop_mcp (government/portal aggregation), HomeHarvest (portal scraping). None was installed for this phase because they do not reliably provide authorized verified Houston sold comps with condition evidence.

### HCAD enrichment
`--enrich-hcad` queries the Harris County GIS parcel layer only for Harris leads carrying a 13-digit `parcel_account`. The adapter validates returned account, street number/name and ZIP, and records its query URL and observation date. It does not verify title, ownership for conveyance, sale price, liens or flood zone. A failed lookup leaves an error field and screening continues. No recurring remote scan or seller contact is scheduled.
