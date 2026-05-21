import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# =========================================================
# BUDGET PIE CHART
# =========================================================

def budget_pie_chart(df, budget):

    # =====================================================
    # EXPENSE DATA
    # =====================================================

    expense_df = df[
        df["type"] == "Expense"
    ]

    category_expense = expense_df.groupby(
        "category"
    )["amount"].sum()

    total_expense = category_expense.sum()

    remaining = max(
        budget - total_expense,
        0
    )

    # =====================================================
    # PIE DATA
    # =====================================================

    labels = list(
        category_expense.index
    )

    amounts = list(
        category_expense.values
    )

    if remaining > 0:

        labels.append(
            "Remaining"
        )

        amounts.append(
            remaining
        )

    # =====================================================
    # COLORS
    # =====================================================

    colors = [

        "#6366f1",  # Indigo
        "#22c55e",  # Green
        "#f59e0b",  # Orange
        "#ef4444",  # Red
        "#06b6d4",  # Cyan
        "#8b5cf6",  # Purple
        "#14b8a6",  # Teal
        "#94a3b8"   # Gray

    ]

    # =====================================================
    # FIGURE
    # =====================================================

    fig, ax = plt.subplots(

        figsize=(4.5, 4.5),

        facecolor="#0f172a"
    )

    # =====================================================
    # PIE CHART
    # =====================================================

    wedges, texts, autotexts = ax.pie(

        amounts,

        labels=labels,

        autopct='%1.1f%%',

        startangle=90,

        colors=colors[:len(labels)],

        wedgeprops={

            "width": 0.83,

            "edgecolor": "#0f172a",

            "linewidth": 3
        },

        textprops={

            "color": "white",

            "fontsize": 10
        }
    )

    # =====================================================
    # CENTER CIRCLE
    # =====================================================

    centre_circle = plt.Circle(

        (0, 0),

        0.55,

        fc="#0f172a"
    )

    fig.gca().add_artist(
        centre_circle
    )

    # =====================================================
    # CENTER TEXT
    # =====================================================

    ax.text(

        0,

        0.05,

        f"₹{total_expense:,.0f}",

        ha="center",

        va="center",

        fontsize=16,

        color="white"
    )

    ax.text(

        0,

        -0.14,

        "Spent",

        ha="center",

        va="center",

        fontsize=10,

        color="#94a3b8"
    )

    # =====================================================
    # FINAL SETTINGS
    # =====================================================

    ax.axis('equal')

    plt.tight_layout()

    st.pyplot(

        fig,

        transparent=True
    )