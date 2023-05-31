import streamlit as st
from backend.core import run_llm
from ingestion import *

docsearch = ingest()

st.title("RE Renewal Course Q&A")
question = st.text_input("Question: ", placeholder="Type your question here")


if question:
    st.write("")
    with st.spinner("Generating response..."):
        respone = run_llm(query=question, docsearch=docsearch)
        st.write(f"Answer: {respone['result']}")
    

    