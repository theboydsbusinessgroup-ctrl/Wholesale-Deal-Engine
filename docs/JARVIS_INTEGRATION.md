# JARVIS Integration

## Purpose

JARVIS is the portfolio-level orchestration, intelligence, alerting, and income-visibility layer. Wholesale Deal Engine remains the operational source of truth for property, seller, buyer, contract, disposition, and closing records.

JARVIS must not become a duplicate property/transaction database.

## Integration boundary

Wholesale Deal Engine -> normalized telemetry/events -> JARVIS

JARVIS -> commands/priority signals -> Wholesale Deal Engine

Commands must be routed through the engine's own authorization and compliance gates. JARVIS cannot bypass transaction controls.

## Telemetry contract

The Wholesale Deal Engine should expose these normalized metrics:

```text
opportunities_discovered
opportunities_qualified
seller_conversations_active
offers_submitted
contracts_pending
contracts_active
contracts_at_risk
buyer_matches
assignments_pending
closings_pending
closed_assignments
realized_assignment_income
expected_assignment_income
estimated_transaction_costs
net_realized_income
capital_exposure
average_assignment_fee
median_days_to_contract
median_days_to_assignment
contract_to_assignment_rate
assignment_to_close_rate
source_conversion_rate
buyer_response_rate
seller_response_rate
active_exceptions
critical_exceptions
human_review_queue
last_successful_scan
last_successful_underwriting_run
last_successful_buyer_match_run
data_freshness
integration_health
engine_health
```

## Event types

- `deal.discovered`
- `deal.qualified`
- `seller.contact_started`
- `offer.created`
- `offer.accepted`
- `contract.pending_signature`
- `contract.executed`
- `contract.compliance_hold`
- `buyer.match_created`
- `buyer.selected`
- `assignment.pending`
- `assignment.executed`
- `title.exception`
- `closing.scheduled`
- `closing.completed`
- `assignment_fee.realized`
- `deal.cancelled`
- `human_review.required`
- `engine.error`

Every event requires an event ID, deal ID, timestamp, source, schema version, confidence where applicable, and authorization context.

## JARVIS commands

JARVIS may request:

- prioritize a market/source/lead segment
- prioritize an exception
- pause/resume a non-binding discovery workflow
- request a fresh underwriting run
- request a buyer re-match
- request a portfolio report
- surface a deal for human review

JARVIS may not directly:

- sign a purchase contract
- sign an assignment contract
- alter approved offer limits
- move money
- bypass legal/compliance gates
- override title/escrow holds
- expose protected credentials

## Income model

JARVIS should distinguish:

1. Pipeline value — estimated future assignment income.
2. Contracted expected fee — fee expected under an active assignment path.
3. Realized assignment income — money actually received.
4. Transaction costs — documented costs attributable to the deal.
5. Net realized income — realized income minus known attributable costs.

Never report pipeline value as earned income.

## Alerts

JARVIS should receive and prioritize:

- contract deadline approaching
- seller/buyer communication requiring attention
- assignment window at risk
- buyer qualification failure
- title/escrow exception
- compliance hold
- unexpected capital exposure
- deal economics deterioration
- stale property data
- stale comps/valuation
- source outage
- automation failure
- closing failure

Alert priority should consider severity, financial impact, deadline, confidence, and reversibility.

## Privacy/security

JARVIS receives only the minimum information required for portfolio orchestration. Sensitive seller/buyer PII, documents, payment information, credentials, and detailed transaction records remain in the domain system or approved secure service. Use opaque IDs and deep links where possible.

## Portfolio dashboard

Add a **Wholesale Deal Engine** module to JARVIS with:

- live pipeline count
- active contracts
- assignment pipeline dollars
- realized assignment income
- net realized income
- capital exposure
- deals by stage
- deals requiring human action
- top sources
- buyer liquidity
- closing calendar
- engine health
- scan/data freshness

The module should answer: **What deals exist, what is likely to pay, what has actually paid, what is at risk, and what—if anything—requires Eric's attention?**

## Implementation sequence

1. Add Wholesale Deal Engine to JARVIS portfolio registry.
2. Define shared event schema and versioning.
3. Add read-only telemetry adapter.
4. Add dashboard card/module.
5. Add alert routing.
6. Add command interface limited to safe/non-binding actions.
7. Add authenticated bidirectional integration after validation.
8. Keep transaction signing, money movement, and compliance overrides outside JARVIS authority.
