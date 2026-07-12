import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini Streamlit", layout="centered")
st.title("Gemini AI Chat")
st.markdown("Use the form below to send a prompt to Gemini and receive a response.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY environment variable is not set. Set it before running Streamlit.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

with st.form("gemini_form"):
    model = st.selectbox(
        "Model",
        ["gemini-2.5-flash", "gemini-2.0-pro", "gemini-1.0-pro"],
        index=0,
    )
    prompt = st.text_area("Prompt", height=200)
    submit = st.form_submit_button("Generate Response")

if submit:
    if not prompt.strip():
        st.warning("Please enter a prompt before submitting.")
    else:
        try:
            with st.spinner("Calling Gemini..."):
                result = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
            st.subheader("Gemini Response")
            st.write(result.text)
        except Exception as e:
            st.error(f"Request failed: {e}")

if st.button("Reset"):
    st.experimental_rerun()
