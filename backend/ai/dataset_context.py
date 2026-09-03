def build_dataset_context(run):

    context = f"""
Credit Risk Dataset Analysis

Dataset:
{run.dataset_name}

Dataset Type:
{run.dataset_type}

Analysis Confidence:
{run.confidence}

Total Loans:
{run.total_loans}

Charge-off Rate:
{run.chargeoff_rate}

Top Risk Grade:
{run.top_risk_grade}
"""

    return context