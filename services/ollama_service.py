import requests


def ask_ai(user_question, financial_context):

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are ERID AI.

You are a professional financial planning assistant.

Your responsibilities:
- analyze financial goals
- suggest savings strategies
- estimate realistic timelines
- recommend budgeting improvements
- provide practical financial advice

STRICT RULES:
- Keep responses SHORT and structured
- Use bullet points
- Avoid long paragraphs
- Focus only on financial planning
- Use the user's financial data for analysis
- Be realistic and practical
- Refuse unrelated questions politely

RESPONSE FORMAT:

📌 Goal Analysis
📌 Estimated Timeline
📌 Suggested Monthly Savings
📌 Budget Advice
📌 Final Recommendation
"""

    # =====================================================
    # FINAL PROMPT
    # =====================================================

    final_prompt = f"""
{system_prompt}

The user has ONE financial goal.

Your task:
- analyze ONLY the exact goal mentioned
- do NOT invent other goals
- do NOT mention unrelated purchases
- do NOT add assumptions
- keep response concise

Financial Data:
{financial_context}

User Goal:
{user_question}

Respond with:
1. Goal Feasibility
2. Monthly Savings Suggestion
3. Budget Advice
4. Final Recommendation
"""

    # =====================================================
    # OLLAMA REQUEST
    # =====================================================

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": final_prompt,
            "stream": False
        }
    )

    # =====================================================
    # RETURN RESPONSE
    # =====================================================

    return res.json()["response"]