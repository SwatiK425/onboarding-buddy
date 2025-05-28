import streamlit as st
import google.generativeai as genai

# Setup Gemini API
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API key is missing. Add it in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# UI
st.set_page_config(page_title="Onboarding Buddy", page_icon="🤖")
st.title("👋 Onboarding Buddy")

user_input = st.text_input("What’s the first thing that came to mind when you installed this product?")

if user_input:
    prompt = f"""
    You are an AI onboarding buddy. A user said: "{user_input}"

    Your job is to:
    - Understand what they’re trying to achieve
    - Suggest a relatable way to try the product
    - Use friendly, simple language
    - Avoid technical jargon
    """
    try:
        response = model.generate_content(prompt)
        st.markdown("### 🤖 Buddy says:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Something went wrong: {e}")
