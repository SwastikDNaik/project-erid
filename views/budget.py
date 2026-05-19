import streamlit as st
import pandas as pd

from database.db import cursor

from services.finance_service import *

def show_budget(conn):

    st.title("🎯 Budget Management")

    df = load_transactions(conn)

    total_income_value = total_income(df)
    total_expense_value = total_expense(df)

    remaining = (
        total_income_value -
        total_expense_value
    )

    # ================= METRICS =================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Income",
            f"₹{total_income_value}"
        )

    with col2:
        st.metric(
            "Total Expense",
            f"₹{total_expense_value}"
        )

    with col3:
        st.metric(
            "Remaining Budget",
            f"₹{remaining}"
        )

    st.markdown("---")

    # ================= LOAD BUDGET =================

    budget_data = pd.read_sql_query(
        "SELECT * FROM budget ORDER BY id DESC LIMIT 1",
        conn
    )

    saved_budget = 0

    if not budget_data.empty:
        saved_budget = budget_data.iloc[0]["monthly_budget"]

    # ================= INPUT =================

    monthly_budget = st.number_input(
        "Enter Monthly Budget (₹)",
        min_value=0.0,
        value=float(saved_budget),
        step=100.0
    )

    # ================= SAVE =================

    if st.button("Save Budget"):

        cursor.execute(
            """
            INSERT INTO budget(monthly_budget)
            VALUES (?)
            """,
            (monthly_budget,)
        )

        conn.commit()

        st.success("Budget Saved!")

        st.rerun()

    # ================= PROGRESS =================

    if monthly_budget > 0:

        budget_left = (
            monthly_budget -
            total_expense_value
        )

        budget_used = (
            total_expense_value /
            monthly_budget
        )

        st.progress(
            min(budget_used, 1.0)
        )

        st.write(
            f"### Budget Used: ₹{total_expense_value} / ₹{monthly_budget}"
        )

        st.write(
            f"### Remaining Budget: ₹{budget_left}"
        )

        if budget_left < 0:

            st.error(
                "⚠️ You exceeded your monthly budget!"
            )

        elif budget_used > 0.8:

            st.warning(
                "⚠️ You already used more than 80% of your budget."
            )

        else:

            st.success(
                "✅ Your budget is under control."
            )