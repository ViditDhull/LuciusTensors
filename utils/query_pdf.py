from utils.api_key import gpt_api_key
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def pdf_query_generator(vec_store, query):

    if query:

        llm = OpenAI(openai_api_key=gpt_api_key)
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=vec_store.as_retriever())
        response = qa_chain({"query": query})

    return response