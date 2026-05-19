import streamlit as st

from database.models import create_tables
from database.db import conn

from styles.style import load_css

from components.sidebar import sidebar

from views.dashboard import show_dashboard
from views.transactions import show_transactions
from views.bills import show_bills
from views.income import show_income
from views.budget import show_budget

# ================= CONFIG =================

st.set_page_config(
    page_title="AI Finance Dashboard",
    layout="wide"
)

# ================= INIT =================

create_tables()

load_css()

# ================= SIDEBAR =================

page = sidebar()

# ================= PAGE ROUTING =================

if page == "🏠 Dashboard":
    show_dashboard(conn)

elif page == "💳 Transactions":
    show_transactions(conn)

elif page == "📅 Bills & Payments":
    show_bills(conn)

elif page == "💰 Income Sources":
    show_income(conn)

elif page == "🎯 Budget Management":
    show_budget(conn)