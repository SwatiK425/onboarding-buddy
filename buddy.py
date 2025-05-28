import streamlit as st
import google.generativeai as genai

# Set up Gemini API
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API key is missing. Please add it in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# UI
st.set_page_config(page_title="Onboarding Buddy", page_icon="🤖")
st.title("👋 Welcome to your Onboarding Buddy")

user_input = st.text_input("What’s the first thing that came to mind when you installed this product?")

if user_input:
    prompt = f"""
    You are an AI onboarding buddy for a product. A user said: \"{user_input}\"

    Your job is to:
    - Understand what they’re trying to achieve
    - Explain what the product can do that is most relevant to them
    - Give a quick, relatable example to try
    - Use friendly, simple language
    - Avoid technical jargon
    """

    try:
        response = model.generate_content(prompt)
        st.markdown("### 🤖 Buddy says:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Something went wrong: {e}")
