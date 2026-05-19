import streamlit as st
import pandas as pd

from database.db import cursor

from services.finance_service import *

from components.charts import budget_pie_chart
from components.ai_assistant import ai_assistant

def show_dashboard(conn):

    df = load_transactions(conn)

    # ================= HEADER =================

    st.markdown("""
    <div style="
        font-size: 36px;
        font-weight: 900;
        color: #6366f1;
        margin-bottom: 10px;
    ">
        ERID
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Overview")

    col1, col2, col3 = st.columns(
        [1, 1.2, 1],
        gap="large"
    )

    # ================= SAVINGS =================

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("💼 Savings")

        st.metric(
            "Current Savings",
            f"₹{savings(df)}"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ================= PIE CHART =================

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("📊 Budget Usage")

        budget_data = pd.read_sql_query(
            "SELECT * FROM budget ORDER BY id DESC LIMIT 1",
            conn
        )

        monthly_budget = 0

        if not budget_data.empty:
            monthly_budget = budget_data.iloc[0]["monthly_budget"]

        expense = total_expense(df)

        if monthly_budget > 0:

            budget_pie_chart(
                expense,
                monthly_budget
            )

            st.write(
                f"### ₹{expense} / ₹{monthly_budget} Used"
            )

        else:
            st.info("Set a monthly budget first")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ================= UPCOMING BILLS =================

    with col3:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("📅 Upcoming Bills")

        bills_df = pd.read_sql_query(
        """
        SELECT * FROM bills
        ORDER BY due_date ASC
        LIMIT 5
        """,
        conn
        )
        if not bills_df.empty:

            for _, row in bills_df.iterrows():

                st.markdown(
                    f"""
                    • {row['name']} — ₹{row['amount']}  
                    📅 {row['due_date']}  
                    🔁 {row['frequency']}
                    """
                )

        else:

            st.info("No upcoming bills")
        
        

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ================= BOTTOM SECTION =================

    st.markdown("---")
    st.markdown("## 💼 Financial Management")

    col4, col5, col6 = st.columns(
        3,
        gap="large"
    )

    # ================= ADD TRANSACTION =================

    with col4:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("➕ Add Transaction")

        transaction_type = st.radio(
            "Type",
            ["Expense", "Income"]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=1.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Bills",
                "Travel",
                "Shopping",
                "Salary",
                "Other"
            ]
        )

        if st.button("Add Transaction"):

            if amount > 0:

                cursor.execute(
                    """
                    INSERT INTO transactions(
                        type,
                        amount,
                        category
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        transaction_type,
                        amount,
                        category
                    )
                )

                conn.commit()

                st.success("Transaction Added!")

                st.rerun()

            else:
                st.warning("Enter valid amount")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ================= GOALS =================

    with col5:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("🎯 Goal Planning")

        goal_amount = st.number_input(
            "Target (₹)",
            value=50000
        )

        saved = st.number_input(
            "Saved (₹)",
            value=15000
        )

        if goal_amount > 0:

            progress = saved / goal_amount

            st.progress(progress)

            st.write(
                f"₹{saved} / ₹{goal_amount}"
            )

            st.write(
                f"Remaining: ₹{goal_amount - saved}"
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ================= INSIGHTS =================

    with col6:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("📈 Insights")

        if not df.empty:

            total_expense_value = df[
                df["type"] == "Expense"
            ]["amount"].sum()

            st.write(
                f"Total Expense: ₹{total_expense_value}"
            )

            expense_df = df[
                df["type"] == "Expense"
            ]

            if not expense_df.empty:

                top_category = expense_df.groupby(
                    "category"
                )["amount"].sum().idxmax()

                st.write(
                    f"Top Spending: {top_category}"
                )

        else:
            st.info("No data yet")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ================= AI ASSISTANT =================

    st.markdown("---")

    ai_assistant()