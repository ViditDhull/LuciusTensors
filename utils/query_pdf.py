from utils.api_key import openai_api_key
from langchain.chains import RetrievalQA
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def pdf_query_generator(pdf_file, query):

    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
    chunks = text_splitter.split_text(text=text)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vec_store = FAISS.from_texts(chunks, embeddings)
    
    llm = OpenAI(openai_api_key=openai_api_key)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vec_store.as_retriever())
    response = qa_chain({"query": query})

    return response