from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.api_key import g_api_key
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

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

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key = g_api_key)
        vec_store = Chroma.from_texts(chunks, embeddings)
        

        if query:

            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                               google_api_key = g_api_key,
                              convert_system_message_to_human=True)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vec_store.as_retriever())
            response = qa_chain({"query": query})

    return response