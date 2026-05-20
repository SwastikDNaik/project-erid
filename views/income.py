import streamlit as st
import pandas as pd

from database.db import cursor

def show_income(conn):

    st.title("💰 Income Sources")

    st.markdown("---")

    # ================= ADD INCOME =================

    st.subheader("➕ Add Income Source")

    title = st.text_input(
        "Income Source",
        placeholder="E.g., Salary, Freelancing"
    )

    transaction_type = "Income"

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=1.0,
        value=None,
        placeholder="Enter income amount"
    )

    frequency = st.selectbox(
        "Income Frequency",
        [
            "Single Time",
            "Daily",
            "Weekly",
            "Monthly",
            "Yearly"
        ]
    )

    category = st.selectbox(
        "Category",
        [
            "Salary",
            "Freelancing",
            "Business",
            "Investment",
            "Passive Income",
            "Other"
        ]
    )

    if st.button("Save Income Source"):

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
                    f"{category} ({frequency})"
                )
            )

            conn.commit()

            st.success("Income Source Added!")

            st.rerun()

        else:

            st.warning("Enter valid details")

    # ================= LOAD INCOME =================

    st.markdown("---")

    st.subheader("📋 Income Sources")

    income_df = pd.read_sql_query(
        """
        SELECT * FROM transactions
        WHERE type='Income'
        ORDER BY id DESC
        """,
        conn
    )

    if income_df.empty:

        st.info("No income sources yet")

    else:

        for _, row in income_df.iterrows():

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
                        key=f"delete_income_{row['id']}"
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

                with st.expander("✏️ Edit Income Source"):

                    new_title = st.text_input(
                        "Income Source",
                        value=row['title'],
                        key=f"title_income_{row['id']}"
                    )

                    new_amount = st.number_input(
                        "Amount",
                        value=float(row['amount']),
                        key=f"amount_income_{row['id']}"
                    )

                    frequency_options = [
                        "Single Time",
                        "Daily",
                        "Weekly",
                        "Monthly",
                        "Yearly"
                    ]

                    category_options = [
                        "Salary",
                        "Freelancing",
                        "Business",
                        "Investment",
                        "Passive Income",
                        "Other"
                    ]

                    current_category = row['category']

                    extracted_frequency = "Single Time"
                    extracted_category = "Other"

                    if "(" in current_category:

                        extracted_category = current_category.split(" (")[0]

                        extracted_frequency = current_category.split("(")[1].replace(")", "")

                    new_frequency = st.selectbox(
                        "Frequency",
                        frequency_options,
                        index=frequency_options.index(
                            extracted_frequency
                        )
                        if extracted_frequency in frequency_options
                        else 0,
                        key=f"freq_income_{row['id']}"
                    )

                    new_category = st.selectbox(
                        "Category",
                        category_options,
                        index=category_options.index(
                            extracted_category
                        )
                        if extracted_category in category_options
                        else 0,
                        key=f"category_income_{row['id']}"
                    )

                    if st.button(
                        "💾 Save Changes",
                        key=f"save_income_{row['id']}"
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
                                f"{new_category} ({new_frequency})",
                                row['id']
                            )
                        )

                        conn.commit()

                        st.success(
                            "Income Source Updated!"
                        )

                        st.rerun()