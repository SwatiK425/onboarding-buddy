import streamlit as st
import google.generativeai as genai

# Set up the API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Create the model instance
model = genai.GenerativeModel(model_name="gemini-pro")  # ✅ use correct model_name param

# Streamlit UI
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
