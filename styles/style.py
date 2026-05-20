import streamlit as st

def load_css():

    st.markdown("""
    <style>

    /* =========================================================
       HEADER
    ========================================================= */

    header[data-testid="stHeader"] {

        background: transparent;
    }



    /* =========================================================
       SIDEBAR TOGGLE BUTTON
    ========================================================= */


    /* =========================================================
       MAIN APP
    ========================================================= */

    .stApp {

        background:
        linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #111827
        );

        color: white;
    }

    /* =========================================================
       MAIN CONTAINER
    ========================================================= */

    .block-container {

        padding-top: 1.8rem;

        padding-bottom: 1rem;
    }

    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {

        background:
        linear-gradient(
            180deg,
            #111827,
            #0f172a
        );

        border-right:
        1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar {

        display: none;
    }

    /* =========================================================
       RADIO BUTTONS
    ========================================================= */

    div[role="radiogroup"] > label > div:first-child {

        display: none;
    }

    div[data-testid="stRadio"] > label {

        display: none;
    }

    /* =========================================================
       NAVIGATION ITEMS
    ========================================================= */

    div[role="radiogroup"] label {

        background: transparent;

        padding: 10px 14px;

        border-radius: 14px;

        margin-bottom: 6px;

        transition: 0.25s ease;

        border: 1px solid transparent;
    }

    div[role="radiogroup"] label:hover {

        background:
        rgba(99,102,241,0.12);

        border:
        1px solid rgba(99,102,241,0.25);

        transform: translateX(3px);
    }

    div[role="radiogroup"] label[data-selected="true"] {

        background:
        linear-gradient(
            90deg,
            rgba(99,102,241,0.25),
            rgba(139,92,246,0.18)
        );

        border:
        1px solid rgba(99,102,241,0.35);

        box-shadow:
        0 0 18px rgba(99,102,241,0.18);
    }

    div[role="radiogroup"] p {

        font-size: 15px;

        font-weight: 600;

        color: white;
    }

    /* =========================================================
       CARDS
    ========================================================= */

    .card {

        background:
        rgba(17, 25, 40, 0.62);

        border:
        1px solid rgba(255,255,255,0.08);

        backdrop-filter: blur(14px);

        padding: 22px;

        border-radius: 22px;

        transition: 0.3s ease;

        margin-bottom: 18px;
    }

    .card:hover {

        border:
        1px solid rgba(99,102,241,0.35);

        box-shadow:
        0 0 22px rgba(99,102,241,0.15);
    }

    /* =========================================================
       BUTTONS
    ========================================================= */

    .stButton > button {

        width: 100%;

        border-radius: 14px;

        height: 44px;

        border: none;

        background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );

        color: white;

        font-weight: 600;

        transition: 0.25s ease;
    }

    .stButton > button:hover {

        transform: scale(1.02);

        box-shadow:
        0 0 18px rgba(99,102,241,0.35);
    }

    /* =========================================================
       INPUTS
    ========================================================= */

    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div {

        border-radius: 12px !important;
    }

    /* =========================================================
       METRICS
    ========================================================= */

    [data-testid="stMetric"] {

        background: transparent !important;

        border: none !important;

        box-shadow: none !important;
    }

    /* =========================================================
       TABLES
    ========================================================= */

    .stDataFrame {

        border-radius: 18px;

        overflow: hidden;

        border:
        1px solid rgba(255,255,255,0.08);
    }

    /* =========================================================
       HEADINGS
    ========================================================= */

    h1, h2, h3 {

        letter-spacing: -0.5px;
    }

    </style>
    """, unsafe_allow_html=True)