import streamlit as st
import requests
from dotenv import load_dotenv
import os

# --- Load the API key from the .env file ---
load_dotenv()
API_KEY = os.getenv("SERPER_API_KEY")

# --- Function to search using Serper.dev ---
def search_google(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
        results = data.get("organic", [])[:3]  # Top 3 results only

        if not results:
            return "No results found."

        reply = []
        for result in results:
            reply.append({
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", "")
            })

        return reply

    except Exception as e:
        return f"Error: {e}"

# --- Page Setup ---
st.set_page_config(page_title="QuickLook AI", layout="centered")

# --- Custom Style ---
st.markdown("""
    <style>
        .main-title {
            font-size: 28px;
            font-weight: bold;
            color: #0066cc;
        }
        .result-box {
            background-color: #e9f1fa;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title and Instructions ---
st.markdown('<div class="main-title">QuickLook AI</div>', unsafe_allow_html=True)
st.write("Enter any topic or question below to get top Google search results.")
st.info("Note: This tool is built for research purposes only and does not provide conversation-like responses.")

# --- Input and Button ---
question = st.text_input("Enter your research topic or question:")

if st.button("Get Info"):
    if question.strip() == "":
        st.warning("Please enter a valid topic or question.")
    else:
        with st.spinner("Searching..."):
            response = search_google(question)

        if isinstance(response, str):
            st.error(response)
        else:
            for res in response:
                st.markdown(f"""
                    <div class="result-box">
                        <h4>{res['title']}</h4>
                        <p>{res['snippet']}</p>
                        <a href="{res['link']}" target="_blank">Read more</a>
                    </div>
                """, unsafe_allow_html=True)
