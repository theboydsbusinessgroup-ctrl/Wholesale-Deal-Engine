# Harris County public-record lead research — 2026-10-01

The public-record lane is live for **research**, with no paid data provider. It identifies parcels and events; it does not identify willing sellers or establish a wholesale price.

| Signal | Official access | What it can establish | What remains unverified |
| --- | --- | --- | --- |
| Parcel, tax-roll owner, mailing address | [HCAD property downloads](https://hcad.org/pdata/pdata-property-downloads.html), [property search](https://hcad.org/quicksearch/), and [GIS parcel layer](https://www.gis.hctx.net/arcgis/rest/services/HCAD/Parcels/MapServer/0) | Account/address match, current appraisal-roll fields, mailing address | Deed/title, current occupancy, condition, motivation, price. Mailing address differing from situs is an *absentee-owner candidate*, not proof of absence or vacancy. |
| Delinquent taxes | [Tax Office delinquent account search](https://www.hctax.net/Property/DelinquentTax) and [statements](https://www.hctax.net/Property/ViewStatementReceipts) | A dated account statement or reported balance | Current payoff, payment posting, all taxing jurisdictions, title and seller willingness. Recheck with Tax Office. |
| Tax foreclosure sale | [Tax Office dated sale listing](https://www.hctax.net/Property/Listings/TaxSaleListing.cshtml) | Scheduled sale, account/cause, judgment years and listed bid | Actual auction status, ownership/title, encumbrances, occupancy, assignable direct contract. A bid requires capital and is outside this engine's no-acquisition lane. |
| Mortgage foreclosure notice | [County Clerk foreclosure postings](https://cclerk.hctx.net/Applications/WebSearch/FRCL_R.aspx) | Filed notice and scheduled sale as posted | Whether the sale proceeds, reinstatement, underlying debt/payoff, competing liens, or a seller agreement. |
| Deeds and recorded instruments | [County Clerk real-property search](https://cclerk.hctx.net/Applications/WebSearch/RP.aspx) | Recorded documents and filing references | A complete title opinion; use a title company/attorney before commitment. |

HCAD offers downloadable 2026 property records with owner name and mailing address. Keep raw owner and mailing data in ignored `data/` only; public reports use parcel/account identifiers and do not publish personal contact information. Compare normalized mailing and situs addresses only as a lead signal. Exclude PO boxes and ambiguous matches from an automatic absentee inference. A tax-roll name may lag a recorded deed.

## Two official tax-sale research signals

The Tax Office listing showed an October 6, 2026 scheduled sale when observed October 1. Both parcel account/street/ZIP combinations were matched against the HCAD 2026 active GIS roll. These are **not** vetted wholesale opportunities.

| Parcel | Tax-sale listing signal | HCAD appraisal | Next verification |
| --- | --- | ---: | --- |
| 11226 Sagecanyon Dr, 77089; account `1031760000007` | Cause `202467952`; judgment years 2022–2025; listed minimum bid $35,209.10 | $219,523 | Recheck live sale status and delinquent statement; verify recorded title and whether a direct seller channel exists |
| 8106 Blooming Meadow Ln, 77016; account `1305950070011` | Cause `202535779`; judgment years 2023–2025; listed minimum bid $23,604.83 | $242,365 | Same, plus property type, condition and occupancy |

The listed minimum bids are **not asking prices**. Adjudged or appraised values are **not ARV or equity**. The Tax Office says entries can be removed or canceled before sale and cautions that title, liens, location, and condition require independent diligence. `examples/harris-county-record-signals.json` preserves the observed event and unknown fields; `reports/harris-county-record-signals.json` shows both `REVIEW_REQUIRED`, zero accepted comps and no economics. The engine blocks a `county_record_signal` even if someone later enters a tempting auction figure as an asking price. No outreach, bidding, or offer has occurred.

Next pass: recheck the live sale list and tax statement by account, inspect the relevant recorded instruments and notice, confirm parcel type/occupancy, then seek a legitimate direct seller channel. Only after seller authority, repair scope, verified sold comps, title review, no-capital structure and funded buyer evidence should a lead enter underwriting. A filed notice or tax balance by itself is not a substitute for any of these.

Free-tool preflight: [gboogy/hcad-property-taxes](https://github.com/gboogy/hcad-property-taxes) is a 2020 Selenium scraper without a declared license and does not cover the current official sale/foreclosure workflow. It was reviewed but not installed; the existing direct HCAD GIS reader and official county portals are sufficient for this first research pass.
