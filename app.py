import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# ---------------------------
# Load API Key
# ---------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Sharath AI Assistant", page_icon="🤖")
st.title("🤖 Chat with Sharath AI")
st.write("Ask anything about Sharath's education, projects, and experience.")

# ---------------------------
# Load Resume File
# ---------------------------
try:
    with open("resume.txt", "r", encoding="utf-8") as file:
        resume_context = file.read()
except FileNotFoundError:
    st.error("resume.txt file not found in project folder.")
    st.stop()

# ---------------------------
# Detect Available Gemini Model
# ---------------------------
try:
    models = client.models.list()
    model_name = None

    for model in models:
        if "gemini" in model.name.lower():
            model_name = model.name
            break

    if not model_name:
        st.error("No Gemini model available for this API key.")
        st.stop()

except Exception as e:
    st.error(f"Model detection error: {e}")
    st.stop()

# ---------------------------
# Chat Input
# ---------------------------
user_input = st.text_input("Ask about Sharath:")

if user_input:

    full_prompt = f"""
    You are an AI assistant representing Sharath.

    Answer using the resume information below.
    If the question requires interpretation (like employment status),
    infer logically based on the resume content.
    If information is not available, say it clearly.

    If the answer is not in the resume, say:
    "This information is not available in Sharath's resume."

    Resume:
    {resume_context}

    Question:
    {user_input}
    """

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=full_prompt
        )

        st.write("### 🤖 Answer:")
        st.write(response.text)

    except Exception as e:
        st.error(f"Generation error: {e}")
