MIN_OBSERVATIONS = 30


def find_risk_leader(rates, counts):

    raw_segment = max(
        rates,
        key=rates.get
    )

    eligible_segments = {
        segment: rate
        for segment, rate in rates.items()
        if counts.get(segment, 0) >= MIN_OBSERVATIONS
    }

    threshold_segment = max(
        eligible_segments,
        key=eligible_segments.get
    )

    return {
        "raw_segment": raw_segment,
        "raw_rate": rates[raw_segment],
        "raw_count": counts[raw_segment],

        "threshold_segment": threshold_segment,
        "threshold_rate": rates[threshold_segment],
        "threshold_count": counts[threshold_segment]
    }


def generate_insight(
    portfolio,
    risk,
    segmentation
):

    purpose_leader = find_risk_leader(
        segmentation["purpose_default_rate"],
        segmentation["purpose_distribution"]
    )

    grade_leader = find_risk_leader(
        segmentation["grade_default_rate"],
        segmentation["grade_distribution"]
    )

    largest_state = max(
        segmentation["state_distribution"],
        key=segmentation["state_distribution"].get
    )

    state_count = (
        segmentation["state_distribution"]
        [largest_state]
    )

    state_pct = round(
        state_count /
        portfolio["total_loans"] * 100,
        2
    )

    return f"""
Portfolio contains {portfolio['total_loans']} loans.

Total exposure is ${portfolio['total_exposure']:,.0f}.

Average loan size is ${portfolio['average_loan_amount']:,.0f}.

Average interest rate is {portfolio['average_interest_rate']:.2f}%.

Charge-off rate is {risk['chargeoff_rate']}%.

Fully paid rate is {risk['fully_paid_rate']}%.

Current loan rate is {risk['current_rate']}%.

Highest observed grade default rate:
{grade_leader['raw_segment']}
({grade_leader['raw_rate']}%)
based on
{grade_leader['raw_count']} loans.

Applying a minimum threshold of
{MIN_OBSERVATIONS} loans,

highest material grade risk is
{grade_leader['threshold_segment']}
({grade_leader['threshold_rate']}%)
across
{grade_leader['threshold_count']} loans.

Highest observed purpose default rate:
{purpose_leader['raw_segment']}
({purpose_leader['raw_rate']}%)
based on
{purpose_leader['raw_count']} loans.

Applying a minimum threshold of
{MIN_OBSERVATIONS} loans,

highest material purpose risk is
{purpose_leader['threshold_segment']}
({purpose_leader['threshold_rate']}%)
across
{purpose_leader['threshold_count']} loans.

Largest state concentration is
{largest_state}
with
{state_count}
loans
({state_pct}% of portfolio).
"""