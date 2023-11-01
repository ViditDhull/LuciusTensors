import os
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from utils.api_key import api_key
from langchain.chains import RetrievalQA

def pdf_query_generator(pdf, query):

    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        
        file_name = pdf.name[:-4]
        file_path = os.path.join("PDF_Embeddings", f"{file_name}.pkl")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                vec_store = pickle.load(f)
        else:
            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            vec_store = FAISS.from_texts(chunks, embeddings)
            with open(file_path, "wb") as f:
                pickle.dump(vec_store, f)

        if query:

            docs = vec_store.similarity_search(query=query, k=3)

            llm = OpenAI(openai_api_key=api_key,)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vec_store.as_retriever())
            response = qa_chain({"query": query})

    return response