import streamlit as st
import pandas as pd

from database.db import cursor

def show_bills(conn):

    st.title("📅 Bills & Payments")

    st.markdown("---")

    # ================= ADD BILL =================

    st.subheader("➕ Add Bill")

    bill_name = st.text_input(
        "Bill Name"
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=1.0
    )

    frequency = st.selectbox(
        "Billing Frequency",
        [
            "Daily",
            "Weekly",
            "Monthly",
            "Yearly"
        ]
    )

    due_date = st.date_input(
        "Next Due Date"
    )

    if st.button("Save Bill"):

        cursor.execute(
            """
            INSERT INTO bills(
                name,
                amount,
                frequency,
                due_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                bill_name,
                amount,
                frequency,
                str(due_date)
            )
        )

        conn.commit()

        st.success("Bill Added!")

        st.rerun()

    # ================= SHOW BILLS =================

    st.markdown("---")

    st.subheader("📋 Saved Bills")

    bills_df = pd.read_sql_query(
        "SELECT * FROM bills ORDER BY due_date ASC",
        conn
    )

    st.dataframe(
        bills_df,
        use_container_width=True
    )