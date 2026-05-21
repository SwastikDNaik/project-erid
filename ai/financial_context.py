import json
from database.db import cursor


def get_financial_context():

    # ==========================================
    # FETCH INCOME
    # ==========================================

    cursor.execute("""
    SELECT title, amount
    FROM transactions
    WHERE type = 'Income'
    """)

    income_rows = cursor.fetchall()

    income_sources = []

    total_income = 0

    for row in income_rows:

        income_sources.append({
            "source": row[0],
            "amount": row[1]
        })

        total_income += row[1]

    # ==========================================
    # FETCH EXPENSES
    # ==========================================

    cursor.execute("""
    SELECT title, amount, category
    FROM transactions
    WHERE type = 'Expense'
    """)

    expense_rows = cursor.fetchall()

    expenses = []

    total_expenses = 0

    for row in expense_rows:

        ESSENTIAL_CATEGORIES = [
            "Rent",
            "Food",
            "Bills",
            "Transport",
            "Medicine",
            "Electricity",
            "Internet"
        ]

        expenses.append({
            "title": row[0],
            "amount": row[1],
            "category": row[2],
            "is_essential": row[2] in ESSENTIAL_CATEGORIES
        })

        total_expenses += row[1]

    # ==========================================
    # FETCH SAVINGS
    # ==========================================

    cursor.execute("""
    SELECT amount
    FROM savings
    WHERE id = 1
    """)

    savings = cursor.fetchone()[0]

    # ==========================================
    # FETCH BUDGET
    # ==========================================

    cursor.execute("""
    SELECT monthly_budget
    FROM budget
    ORDER BY id DESC
    LIMIT 1
    """)

    budget_row = cursor.fetchone()

    monthly_budget = budget_row[0] if budget_row else 0

    # ==========================================
    # FETCH BILLS
    # ==========================================

    cursor.execute("""
    SELECT name, amount, due_date
    FROM bills
    """)

    bills_rows = cursor.fetchall()

    upcoming_bills = []

    for row in bills_rows:

        upcoming_bills.append({
            "name": row[0],
            "amount": row[1],
            "due_date": row[2]
        })

    # ==========================================
    # FINAL STRUCTURED DATA
    # ==========================================

    disposable_income = total_income - total_expenses

    financial_context = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "disposable_income": disposable_income,
        "monthly_budget": monthly_budget,
        "current_savings": savings,
        "income_sources": income_sources,
        "expenses": expenses,
        "upcoming_bills": upcoming_bills
    }

    return financial_context