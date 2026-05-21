import streamlit as st
import pandas as pd

from services.ollama_service import ask_ai
from services.finance_service import (
    load_transactions,
    total_income,
    total_expense
)

from database.db import conn


def ai_assistant():

    st.markdown("---")

    st.subheader("🤖 ERID Financial Planner")

    st.caption(
        "Get AI-powered financial planning based on your current financial data."
    )

    # =====================================================
    # LOAD FINANCIAL DATA
    # =====================================================

    df = load_transactions(conn)

    income = total_income(df)

    expense = total_expense(df)

    savings = income - expense

    # =====================================================
    # CREATE CONTEXT
    # =====================================================

    financial_context = f"""
    Total Income: ₹{income}

    Total Expenses: ₹{expense}

    Current Savings: ₹{savings}

    Total Transactions: {len(df)}
    """

    # =====================================================
    # USER GOAL INPUT
    # =====================================================

    user_input = st.text_input(
        "What financial goal do you have?",
        placeholder="Example: I want to buy a bike worth ₹2 lakh"
    )

    # =====================================================
    # GENERATE PLAN
    # =====================================================

    if st.button("📈 Generate Financial Plan"):

        if user_input:

            with st.spinner(
                "Analyzing your financial situation..."
            ):

                try:

                    response = ask_ai(
                        user_input,
                    )

                    # =====================================
                    # AI RESPONSE CARD
                    # =====================================

                    st.markdown("""
                    <div class="card">
                    """, unsafe_allow_html=True)

                    st.subheader("📊 AI Financial Strategy")

                    st.write(response)

                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:

                    st.error(f"⚠️ {e}")

        else:

            st.warning(
                "Please enter a financial goal."
            )