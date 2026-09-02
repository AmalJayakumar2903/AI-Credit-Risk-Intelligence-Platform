from backend.ai.ollama_client import generate_response


def generate_risk_explanation(
    portfolio,
    risk,
    risk_drivers,
    recommendations
):

    prompt = f"""
You are a credit risk analyst.

Analyze the following structured credit risk results.

Portfolio:
{portfolio}

Risk:
{risk}

Risk Drivers:
{risk_drivers}

Recommendations:
{recommendations}

Provide a concise professional explanation of the key credit risk findings.

Focus on:
1. Overall portfolio risk
2. Most important risk driver
3. What the risk metrics indicate
4. The most relevant management action

Do not calculate or invent new metrics.
Use only the information provided above.
"""

    return generate_response(prompt)