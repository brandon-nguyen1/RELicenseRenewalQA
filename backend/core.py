
import os
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from typing import Any
from langchain import OpenAI

def run_llm(query: str, docsearch: Pinecone) -> Any:
    llm = OpenAI(verbose=True, temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
    rqa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)
    response = rqa(query)
    return response
