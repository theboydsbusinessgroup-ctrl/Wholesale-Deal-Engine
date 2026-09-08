# System Architecture

## 1. Objective

Build a low-touch automated deal engine that converts publicly and lawfully accessible real-estate signals into qualified wholesale opportunities and, where legally permitted, assignment transactions. The system is an income-producing system for the principal, not a business intended for sale.

## 2. State machine

`DISCOVERED -> ENRICHING -> UNDERWRITTEN -> QUALIFIED -> OUTREACH -> NEGOTIATING -> OFFERED -> CONTRACT_PENDING -> CONTRACTED -> COMPLIANCE_REVIEW -> DISPOSITION -> BUYER_SELECTED -> ASSIGNMENT_PENDING -> TITLE_ESCROW -> CLOSING_PENDING -> CLOSED`

Terminal states: `REJECTED`, `NURTURE`, `CANCELLED`, `FAILED`, `CLOSED_NO_FEE`.

Every transition requires timestamp, actor, reason, confidence, source references, and relevant evidence.

## 3. Opportunity record

Minimum fields:

- Property address and parcel/APN
- County/state
- Owner/entity name
- Ownership confidence
- Property type
- Beds/baths/square footage/year built where available
- Occupancy/vacancy signal
- Equity/debt indicators
- Tax status
- Distress signals
- Listing status/history
- Comparable sales set
- ARV estimate and confidence interval
- Repair estimate/range and confidence
- Expected transaction costs
- Buyer target margin
- Target assignment fee
- Maximum allowable contract price
- Seller asking price
- Offer price and rationale
- Deal score
- Risk score
- Source provenance
- Last verification timestamp

## 4. Deal scoring

Score each opportunity using weighted dimensions:

- Seller motivation signal
- Discount/equity potential
- ARV confidence
- Repair confidence
- Market liquidity
- Buyer demand
- Time-to-close feasibility
- Title/legal risk
- Capital exposure
- Assignment spread
- Data quality

Do not use a single fixed percentage-of-ARV rule. The underwriting engine must calculate a deal-specific maximum allowable offer from explicit assumptions.

## 5. Capital protection

Hard reject or escalate any opportunity where the expected path requires the principal to purchase or carry the asset, fund renovations, obtain acquisition financing, or expose capital beyond configured limits. Small transaction obligations such as earnest money or option consideration must be modeled explicitly rather than assumed to be zero.

## 6. Seller workflow

Discovery -> identity/ownership verification -> contact eligibility check -> outreach -> qualification -> motivation/timeline -> property condition -> price discovery -> offer -> counteroffer loop -> contract preparation -> execution/verification.

The agent must identify itself and its role accurately. It must never fabricate urgency, competing offers, ownership, authority, property condition, buyer interest, or closing certainty.

## 7. Buyer workflow

Build a buyer database from lawful sources and transaction signals. Store investment criteria, geographic preferences, price range, asset type, rehab tolerance, proof-of-funds status where lawfully obtained, response history, and completed transaction history where available.

Match buyers to contracted opportunities using weighted fit rather than broadcasting every property indiscriminately.

## 8. Disposition workflow

Before marketing a contract interest, run:

1. Contract assignment-right verification.
2. Required disclosure verification.
3. Jurisdiction/advertising compliance check.
4. Buyer qualification check.
5. Title/escrow coordination readiness check.

Market the contractual/equitable interest accurately. Do not represent the principal as owner of property the principal does not own.

## 9. Texas compliance gate

The first jurisdiction profile is Texas. The implementation must maintain configurable rules for equitable-interest transactions, written disclosures, licensing boundaries, advertising, solicitation, privacy, and transaction documents. Legal rules must be sourced from authoritative current materials and reviewed by qualified Texas counsel before production use.

No AI component may override a compliance gate.

## 10. Human escalation

Escalate when:

- A seller requests legal interpretation.
- Contract language falls outside approved templates.
- Title issues appear.
- Ownership is uncertain.
- A counteroffer exceeds authorization parameters.
- Assignment rights are unclear.
- Required disclosures cannot be verified.
- Buyer qualification is insufficient.
- Closing/title company identifies an exception.
- Any transaction would expose capital beyond configured limits.

## 11. Auditability

Store immutable or append-only event records for every material decision. Every generated valuation, offer, message, contract event, buyer match, disclosure, and closing milestone must have provenance and version information.

## 12. Dashboard

Primary views:

- Live deal pipeline
- New opportunities
- Active seller negotiations
- Contracts at risk
- Buyer marketplace
- Expected assignment income
- Closed assignment income
- Capital exposure
- Upcoming deadlines
- Exceptions requiring human action
- Source/channel performance
- Conversion funnel
- Model confidence and underwriting assumptions

## 13. Optimization loop

Continuously measure source-to-contract conversion, contract-to-assignment conversion, assignment spread, days in stage, seller response rate, buyer response rate, fallout rate, and realized net income. Reallocate automated effort toward strategies with the highest validated expected net assignment income while maintaining compliance and risk constraints.
