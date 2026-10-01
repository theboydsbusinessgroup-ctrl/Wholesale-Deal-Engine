"""MIT-licensed DealCalc MAO primitive; see LICENSE and PROVENANCE.md."""
def mao(
    arv: float,
    rehab_cost: float,
    rule_pct: float = 70,
    desired_profit: float = 0,
    holding_costs: float = 0,
    closing_costs: float = 0,
    wholesale_fee: float = 0,
) -> dict:
    """Maximum allowable offer with explicit cost/profit deductions.

    Formula: ``arv*(rule_pct/100) - rehab_cost - desired_profit
    - holding_costs - closing_costs - wholesale_fee``.

    :returns: ``{max_allowable_offer}``.
    """
    if arv < 0:
        raise ValueError("arv must be non-negative")
    for name, value in (
        ("rehab_cost", rehab_cost),
        ("desired_profit", desired_profit),
        ("holding_costs", holding_costs),
        ("closing_costs", closing_costs),
        ("wholesale_fee", wholesale_fee),
    ):
        if value < 0:
            raise ValueError(f"{name} must be non-negative")
    mao_value = (
        arv * (rule_pct / 100)
        - rehab_cost
        - desired_profit
        - holding_costs
        - closing_costs
        - wholesale_fee
    )
    return {"max_allowable_offer": round(mao_value, 2)}

