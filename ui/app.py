"""
UI entrypoint.

Phase 0/2 goal: prove this container runs and renders.
Phase 7 goal: real chat UI with nation/authority dropdown + citations display.
"""

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="Article4", page_icon="🏠")
st.title("Article4")
st.caption("Not legal advice. Verify with your local planning authority.")

nation = st.selectbox("Nation", ["england", "wales"])
authority = st.text_input("Local authority", placeholder="e.g. ealing, gwynedd")
question = st.text_input("Your question", placeholder="Do I need permission for a rear extension?")

if st.button("Ask") and question:
    try:
        resp = requests.get(
            f"{API_URL}/ask",
            params={"nation": nation, "authority": authority, "q": question},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        st.write(data["answer"])
        st.caption(data["disclaimer"])
    except requests.RequestException as e:
        st.error(f"Couldn't reach the API yet — is it running? ({e})")