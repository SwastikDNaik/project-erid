import streamlit as st
import pandas as pd

from database.db import cursor

def show_transactions(conn):

    st.title("💸 Expenses")

    st.markdown("---")

    # ================= ADD EXPENSE =================

    st.subheader("➕ Add Expense")

    title = st.text_input(
        "Expense Title",
        placeholder="E.g., Grocery Shopping"
    )

    # Automatically set as Expense
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

    if st.button("Save Expense"):

        if title and amount and amount > 0:

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

    # ================= LOAD EXPENSES =================

    st.markdown("---")

    st.subheader("📋 Expense History")

    df = pd.read_sql_query(
        """
        SELECT * FROM transactions
        WHERE type='Expense'
        ORDER BY id DESC
        """,
        conn
    )

    if df.empty:

        st.info("No expenses yet")

    else:

        for _, row in df.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                # ================= INFO =================

                with col1:

                    st.markdown(
                        f"""
                        ### {row['title']}
                        💰 ₹{row['amount']}  
                        📂 {row['category']}
                        """
                    )

                # ================= DELETE =================

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_transaction_{row['id']}"
                    ):

                        cursor.execute(
                            """
                            DELETE FROM transactions
                            WHERE id=?
                            """,
                            (row['id'],)
                        )

                        conn.commit()

                        st.rerun()

                # ================= EDIT =================

                with st.expander("✏️ Edit Expense"):

                    new_title = st.text_input(
                        "Title",
                        value=row['title'],
                        key=f"title_{row['id']}"
                    )

                    new_amount = st.number_input(
                        "Amount",
                        value=float(row['amount']),
                        key=f"amount_{row['id']}"
                    )

                    categories = [
                        "Food",
                        "Bills",
                        "Travel",
                        "Shopping",
                        "Health",
                        "Entertainment",
                        "Other"
                    ]

                    new_category = st.selectbox(
                        "Category",
                        categories,
                        index=categories.index(
                            row['category']
                        )
                        if row['category'] in categories
                        else 0,
                        key=f"category_{row['id']}"
                    )

                    if st.button(
                        "💾 Save Changes",
                        key=f"save_transaction_{row['id']}"
                    ):

                        cursor.execute(
                            """
                            UPDATE transactions
                            SET
                                title=?,
                                amount=?,
                                category=?
                            WHERE id=?
                            """,
                            (
                                new_title,
                                new_amount,
                                new_category,
                                row['id']
                            )
                        )

                        conn.commit()

                        st.success(
                            "Expense Updated!"
                        )

                        st.rerun()