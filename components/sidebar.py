import streamlit as st

def sidebar():

    # =========================================================
    # SIDEBAR CSS
    # =========================================================

    st.markdown("""
    <style>

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

    /* =========================================================
       REMOVE RADIO DOTS
    ========================================================= */

    div[role="radiogroup"] > label > div:first-child {

        display: none;
    }

    /* =========================================================
       REMOVE RADIO TITLE
    ========================================================= */

    div[data-testid="stRadio"] > label {

        display: none;
    }

    /* =========================================================
       NAV ITEMS
    ========================================================= */

    div[role="radiogroup"] label {

        background: transparent;

        padding: 10px 12px;

        border-radius: 14px;

        margin-bottom: 6px;

        transition: 0.25s ease;

        border: 1px solid transparent;
    }

    /* =========================================================
       NAV HOVER
    ========================================================= */

    div[role="radiogroup"] label:hover {

        background:
        rgba(99,102,241,0.12);

        border:
        1px solid rgba(99,102,241,0.25);

        transform: translateX(3px);
    }

    /* =========================================================
       NAV SELECTED
    ========================================================= */

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

    /* =========================================================
       NAV TEXT
    ========================================================= */

    div[role="radiogroup"] p {

        font-size: 15px;

        font-weight: 600;

        color: white;
    }

    /* =========================================================
       BUTTONS
    ========================================================= */

    .stButton > button {

        width: 100%;

        border-radius: 14px;

        height: 42px;

        border: none;

        background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );

        color: white;

        font-weight: 600;

        transition: 0.3s ease;
    }

    .stButton > button:hover {

        transform: scale(1.02);

        box-shadow:
        0 0 18px rgba(99,102,241,0.35);
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # SIDEBAR
    # =========================================================

    with st.sidebar:
        
    

        # =====================================================
        # LOGO
        # =====================================================

        st.markdown("""
        <div style="
            font-size: 30px;
            font-weight: 800;
            color: white;
            margin-bottom: 12px;
            letter-spacing: -1px;
        ">
                MENU
        </div>
        """, unsafe_allow_html=True)
        

        # =====================================================
        # NAVIGATION
        # =====================================================

        page = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "💸 Expenses",
                "📅 Bills & Payments",
                "💰 Income Sources",
                "🎯 Budget Management"
            ]
        )

        # =====================================================
        # FLEX SPACE
        # =====================================================

        st.markdown(
            "<div style='height: 55vh;'></div>",
            unsafe_allow_html=True
        )

        # =====================================================
        # PROFILE BUTTON
        # =====================================================

        if st.button(
            "👤 Profile",
            use_container_width=True
        ):
            st.session_state.show_profile = True

        # =====================================================
        # LOGOUT BUTTON
        # =====================================================

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.warning("Logged out (placeholder)")

    return page