import streamlit as st

from services.ollama_service import ask_ai

def ai_assistant():

    st.subheader("🤖 AI Assistant")

    user_input = st.text_input(
        "Ask about your finances..."
    )

    if st.button("Ask AI"):

        if user_input:

            try:

                response = ask_ai(user_input)

                st.success(response)

            except Exception as e:

                st.error(f"⚠️ {e}")