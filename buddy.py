import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURE GEMINI ---
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual Gemini API key
model = genai.GenerativeModel(model_name="models/gemma-3-1b-it")

# --- PRODUCT KNOWLEDGE BASE (manual grounding for now) ---
dlp_kb = """
🔐 Microsoft Data Loss Prevention (DLP)
Microsoft DLP helps prevent accidental or intentional sharing of sensitive data. 
It protects Exchange, SharePoint, Teams, OneDrive, and endpoints.

Common features:
- Policy tips for real-time education
- Pre-built rules for financial, health, and PII data
- Activity Explorer to review incidents
"""

# --- UI TITLE ---
st.title("🧭 Onboarding Buddy (Microsoft DLP Edition)")
st.markdown("### Personalized tour with smart feedback")

# --- USER INPUT ---
persona = st.text_input("👤 Who are you? (e.g., 'Security analyst at a bank')")
goal = st.text_input("🎯 What do you want to achieve using Microsoft DLP?")

# --- ONBOARD BUTTON ---
if st.button("Generate Onboarding Response"):
    with st.spinner("Thinking..."):
        # --- PROMPT SETUP ---
        prompt = f"""
You are a friendly onboarding buddy for Microsoft DLP.

User persona: {persona}
User goal: {goal}

Product KB:
{dlp_kb}

Your task:
- Greet them
- Understand their goal
- Suggest one thing to try
- Keep it friendly and simple
"""

        time.sleep(1)
        response = model.generate_content(prompt)
        bot_reply = response.text

        # --- DISPLAY BOT REPLY ---
        st.markdown("### 🤖 Onboarding Buddy says:")
        st.write(bot_reply)

        # --- FEEDBACK SECTION ---
        st.markdown("---")
        st.subheader("📝 Your Feedback")

        feedback_choice = st.radio("Was this helpful?", ["👍 Yes", "👎 No"])

        if feedback_choice == "👍 Yes":
            liked_why = st.text_area("What did you like the most?")
        elif feedback_choice == "👎 No":
            disliked_why = st.text_area("What didn’t work for you?")

        # --- SUBMIT FEEDBACK ---
        if st.button("Submit Feedback"):
            with open("feedback_log.txt", "a") as f:
                f.write("\n==========================\n")
                f.write(f"Persona: {persona}\n")
                f.write(f"Goal: {goal}\n")
                f.write(f"Response:\n{bot_reply}\n")
                f.write(f"Helpful: {feedback_choice}\n")
                if feedback_choice == "👍 Yes":
                    f.write(f"Liked what: {liked_why}\n")
                else:
                    f.write(f"Disliked why: {disliked_why}\n")
            st.success("✅ Feedback submitted successfully!")
