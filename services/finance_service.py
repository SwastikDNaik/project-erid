import pandas as pd

def load_transactions(conn):

    return pd.read_sql_query(
        "SELECT * FROM transactions",
        conn
    )

def total_income(df):

    return (
        df[df["type"] == "Income"]["amount"].sum()
        if not df.empty else 0
    )

def total_expense(df):

    return (
        df[df["type"] == "Expense"]["amount"].sum()
        if not df.empty else 0
    )

def savings(df):

    return total_income(df) - total_expense(df)