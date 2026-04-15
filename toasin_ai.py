import streamlit as st
import requests
import textwrap
from mistralai.client import Mistral


API_KEY = st.secrets["API_KEY"]
AGENT_ID = st.secrets["AGENT_ID"]

# 1) Paste your CV text here
CV_TEXT = """
[PASTE CLEAN TEXT VERSION OF YOUR CV HERE]
"""

# 2) Portfolio links
PORTFOLIO_LINKS = """
Power BI dashboards:
- Sales performance dashboard: https://...
- Customer churn dashboard: https://...

Other portfolio:
- BI & analytics portfolio: https://...
- Math teaching materials: https://...
"""

def ask_toasin_ai(question: str) -> str:
    client = Mistral(api_key=API_KEY)
    
    url = f"https://api.mistral.ai/v1/agents/{AGENT_ID}/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    full_input = f"""
    CV and portfolio context:
    {CV_TEXT}

    Portfolio links:
    {PORTFOLIO_LINKS}

    User question:
    {question}
    """

    full_inputs = [{"role": "user", "content": full_input}]
    
    response = client.beta.conversations.start(agent_id=AGENT_ID, agent_version=3,inputs=full_inputs)
    return response.output_text

st.title("Toasin.AI — Interactive CV Assistant")
st.write("Ask anything about Abu’s experience, skills, and projects.")

question = st.text_area("Your question")

if st.button("Ask"):
    if question.strip():
        with st.spinner("Thinking..."):
            answer = ask_toasin_ai(question)
        st.markdown("### Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question.")
