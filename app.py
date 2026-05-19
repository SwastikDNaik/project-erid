import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import sqlite3

# ================= CONFIG =================

st.set_page_config(
    page_title="AI Finance Dashboard",
    layout="wide"
)

# ================= DATABASE =================

conn = sqlite3.connect(
    "Erid_data.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount REAL,
    category TEXT
)
""")

conn.commit()

# ================= LOAD DATA =================

df = pd.read_sql_query(
    "SELECT * FROM transactions",
    conn
)

# ================= CSS =================

st.markdown("""
<style>

/* Remove top gap */
.block-container {
    padding-top: 2rem;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] {
    margin-top: 0px;
}

/* Card UI */
.card {
    padding: 20px;
    border-radius: 16px;
    background-color: #111827;
    border: 1px solid #2d3748;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("## 📊 DashBoard")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💳 Transactions",
            "📅 Bills & Payments",
            "💰 Income Sources",
            "🎯 Budget Management"
        ]
    )

    st.markdown("---")

    st.markdown(
        "<div style='height: 45vh;'></div>",
        unsafe_allow_html=True
    )

    if st.button("👤 Profile", use_container_width=True):
        st.session_state.show_profile = True

    if st.button("🚪 Logout", use_container_width=True):
        st.warning("Logged out (placeholder)")

# ================= DASHBOARD PAGE =================

if page == "🏠 Dashboard":

    # Header
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

        total_income = (
            df[df["type"] == "Income"]["amount"].sum()
            if not df.empty else 0
        )

        total_expense = (
            df[df["type"] == "Expense"]["amount"].sum()
            if not df.empty else 0
        )

        savings = total_income - total_expense

        st.metric(
            "Current Savings",
            f"₹{savings}"
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

        if not df.empty:

            expense_df = df[df["type"] == "Expense"]

            if not expense_df.empty:

                category_sum = expense_df.groupby(
                    "category"
                )["amount"].sum()

                fig, ax = plt.subplots()

                ax.pie(
                    category_sum,
                    labels=category_sum.index,
                    autopct='%1.1f%%'
                )

                ax.axis('equal')

                st.pyplot(fig)

            else:
                st.info("No expenses yet")

        else:
            st.info("Add transactions")

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

        st.markdown("""
        • Electricity — 24 May  
        • Credit Card — 27 May  
        • Netflix — 21 May  
        • Rent — 1 June  
        """)

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

            total_expense = df[
                df["type"] == "Expense"
            ]["amount"].sum()

            st.write(
                f"Total Expense: ₹{total_expense}"
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

    st.subheader("🤖 AI Assistant")

    user_input = st.text_input(
        "Ask about your finances..."
    )

    if st.button("Ask AI"):

        if user_input:

            try:

                res = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "phi3",
                        "prompt": user_input,
                        "stream": False
                    }
                )

                st.success(
                    res.json()["response"]
                )

            except Exception as e:

                st.error(f"⚠️ {e}")

# ================= TRANSACTIONS PAGE =================

elif page == "💳 Transactions":

    st.title("💳 Transactions")

    st.dataframe(df, use_container_width=True)

# ================= BILLS PAGE =================

elif page == "📅 Bills & Payments":

    st.title("📅 Bills & Upcoming Payments")

    st.info("Bills management coming soon")

# ================= INCOME PAGE =================

elif page == "💰 Income Sources":

    st.title("💰 Income Sources")

    income_df = df[df["type"] == "Income"]

    st.dataframe(
        income_df,
        use_container_width=True
    )

# ================= BUDGET PAGE =================

elif page == "🎯 Budget Management":

    st.title("🎯 Budget Management")

    # ================= CALCULATIONS =================

    total_income = (
        df[df["type"] == "Income"]["amount"].sum()
        if not df.empty else 0
    )

    total_expense = (
        df[df["type"] == "Expense"]["amount"].sum()
        if not df.empty else 0
    )

    remaining = total_income - total_expense

    # ================= METRICS =================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Income",
            f"₹{total_income}"
        )

    with col2:
        st.metric(
            "Total Expense",
            f"₹{total_expense}"
        )

    with col3:
        st.metric(
            "Remaining Budget",
            f"₹{remaining}"
        )

    st.markdown("---")

    # ================= SET MONTHLY BUDGET =================

    st.subheader("💰 Set Monthly Budget")

    monthly_budget = st.number_input(
        "Enter Monthly Budget (₹)",
        min_value=0.0,
        step=100.0
    )

    if monthly_budget > 0:

        budget_left = monthly_budget - total_expense

        budget_used = (
            total_expense / monthly_budget
        )

        st.progress(
            min(budget_used, 1.0)
        )

        st.write(
            f"### Budget Used: ₹{total_expense} / ₹{monthly_budget}"
        )

        st.write(
            f"### Remaining Budget: ₹{budget_left}"
        )

        # ================= STATUS =================

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