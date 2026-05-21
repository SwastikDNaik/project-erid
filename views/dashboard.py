import streamlit as st
import pandas as pd

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from services.finance_service import *
from components.charts import budget_pie_chart
from components.ai_assistant import ai_assistant

# =========================================================
# GLOBAL UI
# =========================================================


# =========================================================
# HELPERS
# =========================================================

def add_transaction(
    conn,
    title,
    transaction_type,
    amount,
    category
):

    cursor = conn.cursor()

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


def get_savings(conn):

    savings_data = pd.read_sql_query(
        "SELECT amount FROM savings WHERE id=1",
        conn
    )

    if savings_data.empty:
        return 0

    return savings_data.iloc[0]["amount"]


def update_savings(conn, amount):

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE savings
        SET amount=?
        WHERE id=1
        """,
        (amount,)
    )

    conn.commit()


def load_paid_bills(conn):

    paid_df = pd.read_sql_query(
        """
        SELECT bill_id, paid_date
        FROM paid_bills
        """,
        conn
    )

    return set(
        zip(
            paid_df["bill_id"],
            paid_df["paid_date"]
        )
    )


def generate_bill_dates(
    start_date,
    frequency,
    today,
    limit=10
):

    dates = []

    current = start_date

    while current.date() < today.date():

        if frequency == "Daily":
            current += timedelta(days=1)

        elif frequency == "Weekly":
            current += timedelta(weeks=1)

        elif frequency == "Monthly":
            current += relativedelta(months=1)

        elif frequency == "Yearly":
            current += relativedelta(years=1)

        else:
            break

    for _ in range(limit):

        dates.append(current)

        if frequency == "Daily":
            current += timedelta(days=1)

        elif frequency == "Weekly":
            current += timedelta(weeks=1)

        elif frequency == "Monthly":
            current += relativedelta(months=1)

        elif frequency == "Yearly":
            current += relativedelta(years=1)

    return dates


# =========================================================
# UI COMPONENTS
# =========================================================

def show_header():

    st.markdown("""
    <div style="
        font-size: 67px;
        font-weight: 900;
        color: #6366f1;
        margin-bottom: 10px;
    ">
        ERID
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown("""
    <div class="main-section-title">
        📊 Financial Overview
    """, unsafe_allow_html=True)
    
    st.markdown("---")


def show_savings_card(
    conn,
    df
):

    total_income_value = total_income(df)

    total_expense_value = total_expense(df)

    savings_amount = get_savings(conn)

    balance = (
        total_income_value -
        total_expense_value -
        savings_amount
    )

    st.markdown("""
    <div class="section-title">
        💼 Savings
    </div>
    """, unsafe_allow_html=True)
    # =====================================================
    # TOP METRICS
    # =====================================================

    col1, col2 = st.columns(2, gap="medium")
    with col1:

        st.markdown(
            f"""
    <div class="stats-card">
        <div class="stats-label">
            Savings
        </div>
        <div class="stats-value">
            ₹{savings_amount:,.0f}
        </div>
    </div>
    """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
    <div class="stats-card balance-card">
        <div class="stats-label">
            Balance
        </div>
        <div class="stats-value balance-value">
            ₹{balance:,.0f}
        </div>
    </div>
    """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # ADD TO SAVINGS
    # =====================================================

    st.markdown("""
    <div style="
        font-size:15px;
        font-weight:600;
        margin-bottom:8px;
    ">
        Add To Savings
    </div>
    """, unsafe_allow_html=True)

    add_savings = st.number_input(
        "",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="add_savings",
        label_visibility="collapsed"
    )

    if st.button(
        "➕ Move To Savings",
        use_container_width=True
    ):

        if (
            add_savings > 0 and
            add_savings <= balance
        ):

            update_savings(
                conn,
                savings_amount + add_savings
            )

            st.success("Moved to savings!")

            st.rerun()

        else:

            st.warning("Invalid amount")

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # WITHDRAW SAVINGS
    # =====================================================

    st.markdown("""
    <div style="
        font-size:15px;
        font-weight:600;
        margin-bottom:8px;
    ">
        Withdraw From Savings
    </div>
    """, unsafe_allow_html=True)

    remove_savings = st.number_input(
        "",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="remove_savings",
        label_visibility="collapsed"
    )

    if st.button(
        "➖ Withdraw From Savings",
        use_container_width=True
    ):

        if (
            remove_savings > 0 and
            remove_savings <= savings_amount
        ):

            update_savings(
                conn,
                savings_amount - remove_savings
            )

            st.success("Withdrawn from savings!")

            st.rerun()

        else:

            st.warning("Invalid amount")

    st.markdown("---")
    


def show_budget_card(
    conn,
    df
):

    st.markdown("""
    <div class="section-title">
        📊 Budget Usage
    </div>
    """, unsafe_allow_html=True)

    budget_data = pd.read_sql_query(
        """
        SELECT *
        FROM budget
        ORDER BY id DESC
        LIMIT 1
        """,
        conn
    )

    monthly_budget = 0

    if not budget_data.empty:

        monthly_budget = budget_data.iloc[0][
            "monthly_budget"
        ]

    expense = total_expense(df)

    if monthly_budget > 0:

        left, center, right = st.columns([0.1, 1, 0.1])

        with center:

            budget_pie_chart(
                df,
                monthly_budget
            )

        usage_percent = round(
            (expense / monthly_budget) * 100,
            1
        )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                margin-top:10px;
                font-size:28px;
                font-weight:700;
            ">
                {usage_percent}%
            </div>

            <div style="
                text-align:center;
                color:#94a3b8;
            ">
                ₹{expense} used of ₹{monthly_budget}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Set a monthly budget first"
        )


def show_bills_card(conn):

    

    st.markdown("""
    <div class="section-title">
        📅 Upcoming Bills
    </div>
    """, unsafe_allow_html=True)

    bills_df = pd.read_sql_query(
        """
        SELECT *
        FROM bills
        ORDER BY due_date ASC
        """,
        conn
    )

    if bills_df.empty:

        st.info("No upcoming bills")

    
        return

    paid_set = load_paid_bills(conn)

    upcoming_bills = []

    today = datetime.today()

    for _, row in bills_df.iterrows():

        due_date = datetime.strptime(
            row['due_date'],
            "%Y-%m-%d"
        )

        frequency = row['frequency']

        # =================================================
        # ONCE
        # =================================================

        if frequency == "Once":

            if due_date.date() >= today.date():

                key = (
                    row['id'],
                    due_date.strftime("%Y-%m-%d")
                )

                if key not in paid_set:

                    upcoming_bills.append({
                        "id": row['id'],
                        "name": row['name'],
                        "amount": row['amount'],
                        "date": due_date
                    })

        # =================================================
        # RECURRING
        # =================================================

        else:

            bill_dates = generate_bill_dates(
                due_date,
                frequency,
                today
            )

            for bill_date in bill_dates:

                key = (
                    row['id'],
                    bill_date.strftime("%Y-%m-%d")
                )

                if key not in paid_set:

                    upcoming_bills.append({
                        "id": row['id'],
                        "name": row['name'],
                        "amount": row['amount'],
                        "date": bill_date
                    })

    # =====================================================
    # SORT + LIMIT
    # =====================================================

    upcoming_bills = sorted(
        upcoming_bills,
        key=lambda x: x['date']
    )[:4]

    # =====================================================
    # DISPLAY
    # =====================================================

    for bill in upcoming_bills:

        formatted_date = bill['date'].strftime(
            "%d %b"
        )

       
        st.markdown("---")

        left, right = st.columns([3, 1])

        with left:

            st.markdown(
                f"""
                <div class="bill-card">
                    <div class="bill-top">
                        <div class="bill-title">
                            {bill['name']}
                        </div>
                        <div class="bill-amount">
                            ₹{bill['amount']}
                        </div>
                    </div>
                    <div class="bill-date">
                        📅 {formatted_date}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.write("")

            if st.button(
                "✅ Pay",
                key=f"paid_{bill['id']}_{formatted_date}"
            ):

                add_transaction(
                    conn,
                    bill['name'],
                    "Expense",
                    bill['amount'],
                    "Bills"
                )

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO paid_bills(
                        bill_id,
                        paid_date
                    )
                    VALUES (?, ?)
                    """,
                    (
                        bill['id'],
                        bill['date'].strftime(
                            "%Y-%m-%d"
                        )
                    )
                )

                conn.commit()

                st.success(
                    "Bill marked as paid!"
                )

                st.rerun()




def show_expense_form(conn):

    

    st.markdown("""
    <div class="section-title">
        ➕ Add Expense
    </div>
    """, unsafe_allow_html=True)

    title = st.text_input(
        "Expense Title",
        placeholder="E.g., Grocery Shopping"
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        value=0.0,
        step=1.0
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

    if st.button("Save Expense"):

        if title and amount > 0:

            add_transaction(
                conn,
                title,
                "Expense",
                amount,
                category
            )

            st.success(
                "Expense Added!"
            )

            st.rerun()

        else:

            st.warning(
                "Enter valid details"
            )



def show_income_form(conn):

    st.markdown("""
    <div class="section-title">
        💰 Add Income
    </div>
    """, unsafe_allow_html=True)

    title = st.text_input(
        "Income Source",
        placeholder="E.g., Salary",
        key="income_title"
    )

    amount = st.number_input(
        "Income Amount (₹)",
        min_value=0.0,
        value=0.0,
        step=1.0,
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

    if st.button("Save Income"):

        if title and amount > 0:

            add_transaction(
                conn,
                title,
                "Income",
                amount,
                category
            )

            st.success(
                "Income Added!"
            )

            st.rerun()

        else:

            st.warning(
                "Enter valid details"
            )


def show_insights(df):

    

    st.markdown("""
    <div class="section-title">
        📈 Insights
    </div>
    """, unsafe_allow_html=True)

    if df.empty:

        st.info("No financial data yet")

        return

    expense_df = df[
        df["type"] == "Expense"
    ]

    income_df = df[
        df["type"] == "Income"
    ]

    total_expense_value = expense_df[
        "amount"
    ].sum()

    total_income_value = income_df[
        "amount"
    ].sum()

    st.metric(
        "💸 Expenses",
        f"₹{total_expense_value}"
    )

    st.metric(
        "💰 Income",
        f"₹{total_income_value}"
    )

    if total_income_value > 0:

        savings_rate = (
            (
                total_income_value -
                total_expense_value
            )
            / total_income_value
        ) * 100

        st.metric(
            "📈 Savings Rate",
            f"{savings_rate:.1f}%"
        )

    if not expense_df.empty:

        top_category = expense_df.groupby(
            "category"
        )["amount"].sum().idxmax()

        st.info(
            f"🔥 Highest Spending: {top_category}"
        )



# =========================================================
# MAIN DASHBOARD
# =========================================================

def show_dashboard(conn):

    df = load_transactions(conn)

    show_header()

    # =====================================================
    # TOP SECTION
    # =====================================================

    col1, col2, col3 = st.columns(
        [1, 1.2, 1],
        gap="large"
    )

    with col1:
        show_savings_card(conn, df)

    with col2:
        show_budget_card(conn, df)

    with col3:
        show_bills_card(conn)

    # =====================================================
    # MIDDLE SECTION
    # =====================================================

    st.markdown("---")

    st.markdown("""
    <div class="main-section-title">
        💼 Financial Management
    </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("---")

    col4, col5, col6 = st.columns(
        3,
        gap="large"
    )

    with col4:
        show_expense_form(conn)

    with col5:
        show_income_form(conn)

    with col6:
        show_insights(df)


    # =====================================================
    # AI ASSISTANT
    # =====================================================

    ai_assistant()