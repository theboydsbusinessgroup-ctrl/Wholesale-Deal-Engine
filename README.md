# Wholesale Deal Engine

Autonomous, capital-light real-estate wholesale deal-flow system for personal income generation.

## Mission

Discover legally actionable off-market and distressed real-estate opportunities, underwrite them, pursue seller negotiations, secure assignable contractual interests when appropriate, match contracts with qualified buyers, coordinate disposition/closing, and track realized assignment income.

**Core constraint:** the engine is not designed to acquire, renovate, hold, or finance properties. It targets contract assignment/other legally permitted disposition structures and must reject transactions that create unacceptable capital exposure.

## Operating principles

1. Data-driven opportunity discovery.
2. Conservative underwriting and explicit assumptions.
3. No deceptive representations of ownership or authority.
4. Jurisdiction-specific legal/compliance gates.
5. Attorney/title-company review for transaction documents and exceptions.
6. Human approval for binding commitments until the workflow has been validated.
7. Qualified buyer verification before relying on a disposition.
8. Full audit trail for leads, offers, contracts, disclosures, assignments, communications, and closing milestones.
9. Optimize for expected net assignment income, not lead volume.
10. Escalate anything outside predefined risk, legal, or financial limits.

## Initial operating territory

Texas-first, with an initial focus on the Houston-area market. Geographic expansion is gated by evidence of repeatable deal economics and jurisdiction-specific compliance configuration.

## Pipeline

DISCOVER -> ENRICH -> VERIFY -> UNDERWRITE -> SCORE -> OUTREACH -> NEGOTIATE -> CONTRACT -> COMPLIANCE CHECK -> BUYER MATCH -> DISPOSITION -> ASSIGNMENT/CLOSING -> FEE RECONCILIATION -> LEARNING LOOP

## Initial agent architecture

- Discovery Agent
- Property Intelligence Agent
- Underwriting/Comps Agent
- Seller Outreach Agent
- Negotiation Agent
- Contract/Compliance Gate
- Buyer Acquisition Agent
- Buyer Matching Agent
- Disposition Agent
- Transaction Coordinator
- Closing/Fee Reconciliation Agent
- Risk & Exception Agent
- Performance/Optimization Agent

## Hard safety/compliance boundaries

The engine must not:

- Misrepresent itself as the property owner when it is not.
- Conceal an equitable/contractual interest where disclosure is required.
- Practice law or provide legal advice as a substitute for counsel.
- Circumvent licensing, advertising, disclosure, privacy, telemarketing, or solicitation requirements.
- Fabricate property, title, ownership, buyer, financing, repair, comp, or transaction data.
- Bind the principal to a transaction outside configured authorization limits.
- Spend acquisition capital without explicit authorization.

## Build status

Phase 0: repository initialized.

Next: system specification, data model, scoring model, source adapters, workflow state machine, compliance rule engine, buyer CRM, transaction ledger, and dashboard/API contracts.
