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
            "Once",
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

        if bill_name and amount > 0:

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

        else:
            st.warning("Enter valid details")

    # ================= LOAD BILLS =================

    st.markdown("---")

    st.subheader("📋 Saved Bills")

    bills_df = pd.read_sql_query(
        """
        SELECT * FROM bills
        ORDER BY due_date ASC
        """,
        conn
    )

    if bills_df.empty:

        st.info("No bills added yet")

    else:

        for _, row in bills_df.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                # ================= BILL INFO =================

                with col1:

                    st.markdown(
                        f"""
                        ### {row['name']}
                        💰 ₹{row['amount']}  
                        🔁 {row['frequency']}  
                        📅 {row['due_date']}
                        """
                    )

                # ================= ACTIONS =================

                with col2:

                    # DELETE BUTTON

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{row['id']}"
                    ):

                        cursor.execute(
                            """
                            DELETE FROM bills
                            WHERE id=?
                            """,
                            (row['id'],)
                        )

                        conn.commit()

                        st.rerun()

                # ================= EDIT SECTION =================

                with st.expander("✏️ Edit Bill"):

                    new_name = st.text_input(
                        "Bill Name",
                        value=row['name'],
                        key=f"name_{row['id']}"
                    )

                    new_amount = st.number_input(
                        "Amount",
                        value=float(row['amount']),
                        key=f"amount_{row['id']}"
                    )

                    new_frequency = st.selectbox(
                        "Frequency",
                        [
                            "Once",
                            "Daily",
                            "Weekly",
                            "Monthly",
                            "Yearly"
                        ],
                        index=[
                            "Once",
                            "Daily",
                            "Weekly",
                            "Monthly",
                            "Yearly"
                        ].index(row['frequency']),
                        key=f"freq_{row['id']}"
                    )

                    new_due_date = st.date_input(
                        "Due Date",
                        value=pd.to_datetime(
                            row['due_date']
                        ),
                        key=f"date_{row['id']}"
                    )

                    if st.button(
                        "💾 Save Changes",
                        key=f"save_{row['id']}"
                    ):

                        cursor.execute(
                            """
                            UPDATE bills
                            SET
                                name=?,
                                amount=?,
                                frequency=?,
                                due_date=?
                            WHERE id=?
                            """,
                            (
                                new_name,
                                new_amount,
                                new_frequency,
                                str(new_due_date),
                                row['id']
                            )
                        )

                        conn.commit()

                        st.success("Bill Updated!")

                        st.rerun()