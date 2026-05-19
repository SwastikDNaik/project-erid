import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def budget_pie_chart(expense, budget):

    remaining = max(
        budget - expense,
        0
    )

    pie_data = pd.DataFrame({
        "Category": [
            "Used",
            "Remaining"
        ],
        "Amount": [
            expense,
            remaining
        ]
    })

    fig, ax = plt.subplots()

    ax.pie(
        pie_data["Amount"],
        labels=pie_data["Category"],
        autopct='%1.1f%%'
    )

    ax.axis('equal')

    st.pyplot(fig)