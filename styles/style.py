import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .block-container {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] {
        margin-top: 0px;
    }

    .card {
        padding: 20px;
        border-radius: 16px;
        background-color: #111827;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }

    </style>
    """, unsafe_allow_html=True)