import streamlit as st
import requests
import textwrap

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

    response = requests.post(url, json={"input": full_input}, headers=headers)
    response.raise_for_status()
    return response.json()["output"]

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
