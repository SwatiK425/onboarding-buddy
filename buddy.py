import streamlit as st
import google.generativeai as genai
import datetime

# --- SETUP ---

# Configure Gemini API
genai.configure(api_key="AIzaSyD_uKqUnDhj7eV0WzNe4IH-z0bwwSe36mM")  # Replace with your Gemini API key

model = genai.GenerativeModel("models/gemma-3-1b-it")  # Use working model

# Load KB (manual RAG)
with open("dlp_kb.txt", "r") as file:
    dlp_kb = file.read()

# --- MEMORY ---

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_goal" not in st.session_state:
    st.session_state.user_goal = ""

# --- UI START ---

st.title("🧠 AI Onboarding Buddy")
st.subheader("Helping you onboard to Microsoft DLP, your way.")

# Ask user name
if not st.session_state.user_name:
    name = st.text_input("👋 What's your name?")
    if name:
        st.session_state.user_name = name

# Ask user goal
if st.session_state.user_name and not st.session_state.user_goal:
    goal = st.text_input(f"Hi {st.session_state.user_name}, what's the first thing you want to achieve?")
    if goal:
        st.session_state.user_goal = goal

# Trigger onboarding
if st.session_state.user_goal:
    st.markdown("✅ Loading your personalized onboarding...")

    prompt = f"""
    You are a helpful onboarding bot for Microsoft Data Loss Prevention (DLP).

    User: {st.session_state.user_name}
    Goal: {st.session_state.user_goal}

    Product KB:
    {dlp_kb}

    Based on the goal, explain 2 product capabilities that would help, and suggest one thing they can try right now. Be friendly, specific, and practical.
    """

    response = model.generate_content(prompt)
    st.write("🤖 Onboarding Buddy says:")
    st.markdown(response.text)

    # --- FEEDBACK ---

    st.divider()
    st.subheader("📣 Give Feedback")

    feedback_col1, feedback_col2 = st.columns(2)
    with feedback_col1:
        liked = st.button("👍 Yes, it helped")
    with feedback_col2:
        disliked = st.button("👎 No, didn’t help")

    if liked:
        detail = st.text_input("What did you like the most?")
        if detail:
            with open("feedback_log.txt", "a") as f:
                f.write(f"{datetime.datetime.now()} | {st.session_state.user_name} | 👍 | {detail}\n")
            st.success("Thanks! Your feedback is recorded.")

    if disliked:
        reason = st.text_input("Why didn’t it help?")
        if reason:
            with open("feedback_log.txt", "a") as f:
                f.write(f"{datetime.datetime.now()} | {st.session_state.user_name} | 👎 | {reason}\n")
            st.warning("We appreciate your input. We’ll improve!")

