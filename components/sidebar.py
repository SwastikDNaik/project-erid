import streamlit as st

def sidebar():

    with st.sidebar:

        st.markdown("## 📊 DashBoard")

        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💸 Expenses",
                "📅 Bills & Payments",
                "💰 Income Sources",
                "🎯 Budget Management"
            ]
        )

        st.markdown("---")

        st.markdown(
            "<div style='height: 45vh;'></div>",
            unsafe_allow_html=True
        )

        if st.button("👤 Profile", use_container_width=True):
            st.session_state.show_profile = True

        if st.button("🚪 Logout", use_container_width=True):
            st.warning("Logged out (placeholder)")

    return page