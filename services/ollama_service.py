import requests
import re
import math

from ai.financial_context import get_financial_context
from utils.number_parser import normalize_indian_currency


# =====================================================
# EXTRACT GOAL AMOUNT
# =====================================================

def format_currency(amount):

    return f"Rs.{amount:,.0f}"

def extract_goal_amount(text):

    text = text.lower().replace(",", "")

    # Match ₹200000 or 200000
    number_match = re.search(r'₹?\s*(\d+)', text)

    if number_match:
        return int(number_match.group(1))

    return 0


# =====================================================
# AI FUNCTION
# =====================================================

def ask_ai(user_question):

    # =====================================================
    # CLEAN USER INPUT
    # =====================================================

    user_question = normalize_indian_currency(user_question)

    # =====================================================
    # GET FINANCIAL DATA
    # =====================================================

    financial_context = get_financial_context()

    total_income = financial_context["total_income"]
    total_expenses = financial_context["total_expenses"]
    disposable_income = financial_context["disposable_income"]
    current_savings = financial_context["current_savings"]

    # =====================================================
    # EXTRACT GOAL AMOUNT
    # =====================================================

    goal_amount = extract_goal_amount(user_question)

    # =====================================================
    # FINANCIAL CALCULATIONS
    # =====================================================

    remaining_amount = max(
        0,
        goal_amount - current_savings
    )

    # Save 60% of disposable income safely
    recommended_monthly_saving = max(
        1000,
        int(disposable_income * 0.6)
    )

    # Prevent division by zero
    if recommended_monthly_saving > 0:

        estimated_months = math.ceil(
            remaining_amount / recommended_monthly_saving
        )

    else:

        estimated_months = "Not Possible"

    # =====================================================
    # EXPENSE REDUCTION CHECK
    # =====================================================

    high_expenses = []

    for expense in financial_context["expenses"]:

        if not expense["is_essential"] and expense["amount"] > 2000:

            high_expenses.append(
                f"- Reduce {expense['title']} spending (₹{expense['amount']})"
            )

    if not high_expenses:

        high_expenses.append(
            "- Current spending looks balanced"
        )

    expense_advice = "\n".join(high_expenses)

    # =====================================================
    # PRECALCULATED ANALYSIS
    # =====================================================

    analysis_data = f"""
Goal Amount: {format_currency(goal_amount)}

Current Savings: {format_currency(current_savings)}

Remaining Amount Needed: {format_currency(remaining_amount)}

Total Monthly Income: {format_currency(total_income)}

Total Monthly Expenses: {format_currency(total_expenses)}

Disposable Income: {format_currency(disposable_income)}

Recommended Monthly Saving: {format_currency(recommended_monthly_saving)}

Estimated Timeline: {estimated_months} months
"""

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are ERID AI.

You are a professional financial planning assistant.

IMPORTANT RULES:

- NEVER recalculate numbers
- ONLY use the provided calculated values
- DO NOT invent financial values
- DO NOT estimate different timelines
- DO NOT modify currency amounts
- DO NOT abbreviate numbers
- NEVER use k, lakh, crore, M, or shorthand formats
- Always use exact provided values
- Keep responses short
- Use bullet points only
- Avoid long paragraphs
- Focus only on the user's goal
- Give practical and realistic budgeting advice
- Maintain clean formatting

You may:
- suggest reducing unnecessary expenses
- recommend safe savings strategies
- suggest partial use of savings
- suggest improving spending habits

You must:
- stay accurate
- stay concise
- keep sections properly formatted
- keep financial advice realistic
"""

    # =====================================================
    # FINAL PROMPT
    # =====================================================

    final_prompt = f"""
{system_prompt}

USER GOAL:
{user_question}

PRECALCULATED FINANCIAL ANALYSIS:
{analysis_data}

EXPENSE REDUCTION SUGGESTIONS:
{expense_advice}

Generate response in this format:

📌 Goal Analysis
- Goal feasibility
- Short reasoning

📌 Income vs Expenses
- Total income
- Total expenses
- Disposable income

📌 Savings Strategy
- Recommended monthly savings
- Suggested savings usage

📌 Expense Reduction Advice
- Mention unnecessary expenses only
- If none, say spending is balanced

📌 Estimated Timeline
- Mention exact estimated months

📌 Final Recommendation
- Give one concise final financial suggestion
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