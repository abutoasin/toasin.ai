"""
Utility for downloading and extracting CV text from OneDrive.
Used by the main Toasin.AI Streamlit app.
"""

import requests
import docx
from io import BytesIO
import streamlit as st


ONEDRIVE_CV_URL = st.secrets["ONEDRIVE_CV_URL"]  # Direct download URL to CV (.docx)


def load_cv_from_onedrive() -> str:
    """
    Download the CV from OneDrive and extract plain text from the .docx file.

    Returns:
        A single string containing all paragraphs from the CV, separated by newlines.
        Returns an empty string and shows a Streamlit error if download fails.
    """
    response = requests.get(ONEDRIVE_CV_URL)

    if response.status_code != 200:
        st.error(f"Failed to download CV from OneDrive (status {response.status_code}).")
        return ""

    # Wrap raw bytes in an in-memory file-like object so python-docx can read it.
    file_like = BytesIO(response.content)

    # Parse the .docx document and join all paragraphs into one text block.
    document = docx.Document(file_like)
    cv_text = "\n".join(p.text for p in document.paragraphs)

    return cv_text


# Load CV once at import time
CV_TEXT = load_cv_from_onedrive()
