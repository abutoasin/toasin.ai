import requests
import docx
from io import BytesIO
import streamlit as st
from mistralai.client import Mistral


# --- Configuration from Streamlit secrets ---
API_KEY = st.secrets["API_KEY"]          # Mistral API key
AGENT_ID = st.secrets["AGENT_ID"]        # Mistral Agent ID


# load CV
from utils.cv_loader import CV_TEXT
if not CV_TEXT:
    st.error("CV could not be loaded. Check your OneDrive link and direct-download setup.")

# Static portfolio links that the agent can reference in answers
from utils.portfolio_links import PORTFOLIO_LINKS
 



def ask_toasin_ai(question: str) -> str:
    """
    Call the Mistral Agent using the Conversations API (beta) with CV + portfolio context.

    Args:
        question: The recruiter's or user's question.

    Returns:
        The assistant's answer as a plain string.
    """
    # Initialize Mistral client with API key
    client = Mistral(api_key=API_KEY)

    # Build a single user message that includes CV, portfolio links, and the question.
    full_input = f"""
CV and portfolio context:
{CV_TEXT}

Portfolio links:
{PORTFOLIO_LINKS}

User question:
{question}
"""

    # Conversations API expects a list of message-like entries
    inputs = [{"role": "user", "content": full_input}]

    # Start a new conversation using the configured Agent
    # See Mistral Conversations beta docs for structure of inputs/outputs.
    response = client.beta.conversations.start(
        agent_id=AGENT_ID,
        inputs=inputs,
    )

    # Take the first output message's content as the answer
    return response.outputs[0].content





# --- Streamlit UI ---

st.title("Toasin.AI — Interactive CV Assistant")
st.write(
    "Hello, and thank you for taking the time to explore Toasin’s profile. "
    "What would you like to know more about—his background, skills, or recent projects?"
)

question = st.text_area("Your question")

if st.button("Ask"):
    if question.strip():
        with st.spinner("Thinking..."):
            answer = ask_toasin_ai(question)
        st.markdown("### Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question.")
