import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from utilities import pdfToText
import pinecone

def ingest():

    # initialize embeddings via OpenAI Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    # initialize pinecone with key
    pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENV"])
    pinecone_index_name = os.environ["PINECONE_INDEX_NAME"]

    # retrieve vectorstore from pinecone if it pinecone index exists
    if pinecone_index_name in pinecone.list_indexes():
        existing_index_obj = pinecone.Index(index_name=pinecone_index_name)
    else:
        raise ValueError("Index does not exist")
    
    # get index stats
    stats = existing_index_obj.describe_index_stats()

    # get index info
    if stats['total_vector_count'] > 0:
        docsearch = Pinecone.from_existing_index(index_name=pinecone_index_name, embedding=embeddings)
    else:
        # if pinecone index does not exist, create it
        # convert pdf to text using pdfToText function
        #pdfToText('docs/vrc.pdf')

        # load documents
        loader = TextLoader('docs/vrc.txt')
        raw_documents = loader.load()
        print(f"Loaded {len(raw_documents)} documents")

        # split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separator='\n')
        documents = text_splitter.split_documents(documents=raw_documents)
        print(f"Split {len(documents)} documents")

        print(f"Going to insert {len(documents)} to Pinecone")

        # create vectorstore to use the index for search
        docsearch = Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=pinecone_index_name)
        print("****** Added to Pincecone vectors ******")

    return docsearch