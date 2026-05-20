import streamlit as st
import pandas as pd

from datetime import datetime, timedelta

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

    # ================= SAVINGS & BALANCE =================

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        # ================= CALCULATIONS =================

        total_income_value = total_income(df)

        total_expense_value = total_expense(df)

        savings_data = pd.read_sql_query(
            "SELECT amount FROM savings WHERE id=1",
            conn
        )

        savings_amount = 0

        if not savings_data.empty:
            savings_amount = savings_data.iloc[0]["amount"]

        balance = (
            total_income_value -
            total_expense_value -
            savings_amount
        )

        # ================= DISPLAY =================

        st.subheader("💼 Savings")

        st.metric(
            "Savings",
            f"₹{savings_amount}"
        )

        st.metric(
            "Balance",
            f"₹{balance}"
        )

        st.markdown("---")

        # ================= ADD TO SAVINGS =================

        add_savings = st.number_input(
            "Add To Savings",
            min_value=0.0,
            value=None,
            placeholder="Enter amount",
            key="add_savings"
        )

        if st.button("➕ Move To Savings"):

            if (
                add_savings is not None and
                add_savings > 0 and
                add_savings <= balance
            ):

                new_savings = (
                    savings_amount +
                    add_savings
                )

                cursor.execute(
                    """
                    UPDATE savings
                    SET amount=?
                    WHERE id=1
                    """,
                    (new_savings,)
                )

                conn.commit()

                st.success(
                    "Moved to savings!"
                )

                st.rerun()

            else:

                st.warning(
                    "Invalid amount"
                )

        # ================= REMOVE FROM SAVINGS =================

        remove_savings = st.number_input(
            "Withdraw From Savings",
            min_value=0.0,
            value=None,
            placeholder="Enter amount",
            key="remove_savings"
        )

        if st.button("➖ Withdraw From Savings"):

            if (
                remove_savings is not None and
                remove_savings > 0 and
                remove_savings <= savings_amount
            ):

                new_savings = (
                    savings_amount -
                    remove_savings
                )

                cursor.execute(
                    """
                    UPDATE savings
                    SET amount=?
                    WHERE id=1
                    """,
                    (new_savings,)
                )

                conn.commit()

                st.success(
                    "Withdrawn from savings!"
                )

                st.rerun()

            else:

                st.warning(
                    "Invalid amount"
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
                """,
                conn
            )

            upcoming_bills = []

            today = datetime.today()

            if not bills_df.empty:

                for _, row in bills_df.iterrows():

                    due_date = datetime.strptime(
                        row['due_date'],
                        "%Y-%m-%d"
                    )

                    frequency = row['frequency']

                    # =====================================================
                    # ONCE
                    # =====================================================

                    if frequency == "Once":

                        if due_date.date() >= today.date():

                            paid_check = pd.read_sql_query(
                                """
                                SELECT * FROM paid_bills
                                WHERE bill_id = ?
                                AND paid_date = ?
                                """,
                                conn,
                                params=(
                                    row['id'],
                                    due_date.strftime("%Y-%m-%d")
                                )
                            )

                            if paid_check.empty:

                                upcoming_bills.append({
                                    "id": row['id'],
                                    "name": row['name'],
                                    "amount": row['amount'],
                                    "date": due_date
                                })

                    # =====================================================
                    # DAILY
                    # =====================================================

                    elif frequency == "Daily":

                        current = max(due_date, today)

                        for i in range(10):

                            bill_date = current + timedelta(days=i)

                            paid_check = pd.read_sql_query(
                                """
                                SELECT * FROM paid_bills
                                WHERE bill_id = ?
                                AND paid_date = ?
                                """,
                                conn,
                                params=(
                                    row['id'],
                                    bill_date.strftime("%Y-%m-%d")
                                )
                            )

                            if paid_check.empty:

                                upcoming_bills.append({
                                    "id": row['id'],
                                    "name": row['name'],
                                    "amount": row['amount'],
                                    "date": bill_date
                                })

                    # =====================================================
                    # WEEKLY
                    # =====================================================

                    elif frequency == "Weekly":

                        current = due_date

                        while current.date() < today.date():
                            current += timedelta(days=7)

                        for i in range(10):

                            bill_date = current + timedelta(days=7*i)

                            paid_check = pd.read_sql_query(
                                """
                                SELECT * FROM paid_bills
                                WHERE bill_id = ?
                                AND paid_date = ?
                                """,
                                conn,
                                params=(
                                    row['id'],
                                    bill_date.strftime("%Y-%m-%d")
                                )
                            )

                            if paid_check.empty:

                                upcoming_bills.append({
                                    "id": row['id'],
                                    "name": row['name'],
                                    "amount": row['amount'],
                                    "date": bill_date
                                })

                    # =====================================================
                    # MONTHLY
                    # =====================================================

                    elif frequency == "Monthly":

                        current = due_date

                        while current.date() < today.date():
                            current += timedelta(days=30)

                        for i in range(10):

                            bill_date = current + timedelta(days=30*i)

                            paid_check = pd.read_sql_query(
                                """
                                SELECT * FROM paid_bills
                                WHERE bill_id = ?
                                AND paid_date = ?
                                """,
                                conn,
                                params=(
                                    row['id'],
                                    bill_date.strftime("%Y-%m-%d")
                                )
                            )

                            if paid_check.empty:

                                upcoming_bills.append({
                                    "id": row['id'],
                                    "name": row['name'],
                                    "amount": row['amount'],
                                    "date": bill_date
                                })

                    # =====================================================
                    # YEARLY
                    # =====================================================

                    elif frequency == "Yearly":

                        current = due_date

                        while current.date() < today.date():
                            current += timedelta(days=365)

                        for i in range(10):

                            bill_date = current + timedelta(days=365*i)

                            paid_check = pd.read_sql_query(
                                """
                                SELECT * FROM paid_bills
                                WHERE bill_id = ?
                                AND paid_date = ?
                                """,
                                conn,
                                params=(
                                    row['id'],
                                    bill_date.strftime("%Y-%m-%d")
                                )
                            )

                            if paid_check.empty:

                                upcoming_bills.append({
                                    "id": row['id'],
                                    "name": row['name'],
                                    "amount": row['amount'],
                                    "date": bill_date
                                })

                # =====================================================
                # SORT
                # =====================================================

                upcoming_bills = sorted(
                    upcoming_bills,
                    key=lambda x: x['date']
                )

                # =====================================================
                # SHOW TOP 4
                # =====================================================

                upcoming_bills = upcoming_bills[:4]

                # =====================================================
                # DISPLAY
                # =====================================================

                for bill in upcoming_bills:

                    formatted_date = bill['date'].strftime(
                        "%d %b"
                    )

                    with st.container(border=True):

                        left, right = st.columns([3, 1])

                        with left:

                            st.markdown(
                                f"""
                                **{bill['name']}**  
                                💰 ₹{bill['amount']}  
                                📅 {formatted_date}
                                """
                            )

                        with right:

                            st.write("")

                            if st.button(
                                "✅ Pay",
                                key=f"paid_{bill['id']}_{formatted_date}"
                            ):

                                # ================= ADD EXPENSE =================

                                cursor.execute(
                                    """
                                    INSERT INTO transactions
                                    (title, type, amount, category)
                                    VALUES (?, ?, ?, ?)
                                    """,
                                    (
                                        bill['name'],
                                        "Expense",
                                        bill['amount'],
                                        "Bills"
                                    )
                                )

                                # ================= MARK INSTANCE AS PAID =================

                                cursor.execute(
                                    """
                                    INSERT INTO paid_bills
                                    (bill_id, paid_date)
                                    VALUES (?, ?)
                                    """,
                                    (
                                        bill['id'],
                                        bill['date'].strftime("%Y-%m-%d")
                                    )
                                )

                                conn.commit()

                                st.success("Bill marked as paid!")

                                st.rerun()

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

    # ================= ADD EXPENSE =================

    with col4:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("➕ Add Expense")

        title = st.text_input(
            "Expense Title",
            placeholder="E.g., Grocery Shopping"
        )

        # ================= FIXED TYPE =================

        transaction_type = "Expense"

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=1.0,
            value=None,
            placeholder="Enter amount"
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Bills",
                "Travel",
                "Shopping",
                "Health",
                "Entertainment",
                "Other"
            ]
        )

        # ================= SAVE =================

        if st.button("Save Expense"):

            if (
                title and
                amount is not None and
                amount > 0
            ):

                cursor.execute(
                    """
                    INSERT INTO transactions(
                        title,
                        type,
                        amount,
                        category
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        title,
                        transaction_type,
                        amount,
                        category
                    )
                )

                conn.commit()

                st.success("Expense Added!")

                st.rerun()

            else:

                st.warning("Enter valid details")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
# ================= ADD INCOME =================

    with col5:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("💰 Add Income")

        title = st.text_input(
            "Income Source",
            placeholder="E.g., Salary, Freelancing",
            key="income_title"
        )

        # ================= FIXED TYPE =================

        transaction_type = "Income"

        amount = st.number_input(
            "Income Amount (₹)",
            min_value=0.0,
            step=1.0,
            value=None,
            placeholder="Enter amount",
            key="income_amount"
        )

        category = st.selectbox(
            "Income Category",
            [
                "Salary",
                "Freelancing",
                "Business",
                "Investments",
                "Passive Income",
                "Bonus",
                "Other"
            ],
            key="income_category"
        )

        # ================= SAVE =================

        if st.button("Save Income"):

            if (
                title and
                amount is not None and
                amount > 0
            ):

                cursor.execute(
                    """
                    INSERT INTO transactions(
                        title,
                        type,
                        amount,
                        category
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        title,
                        transaction_type,
                        amount,
                        category
                    )
                )

                conn.commit()

                st.success("Income Added!")

                st.rerun()

            else:

                st.warning("Enter valid details")

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