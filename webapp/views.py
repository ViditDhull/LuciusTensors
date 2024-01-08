import os
from django.shortcuts import render
from utils.prompt_to_sql import generate_sql_query
from utils.code_optimize import optimize_code
from utils.query_pdf import pdf_query_generator
from PyPDF2 import PdfReader
from utils.api_key import gpt_api_key
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


# Home
def index(request):
    return render(request, 'index.html')

# Prompt to SQL
def sql_query_generator(request):
    title = "Prompt to SQL Generator"
    response = None
    
    if request.method == 'POST':
        user_input = request.POST.get('sql_prompt')
        try:
            response = generate_sql_query(user_input)
        except:
            response = "An error occurred while processing your request. Please try again later."
    return render(request, 'sql_query_generator.html', {'title': title, 'response': response})

# Query Pdf
def query_pdf(request):
    title = "Query PDF"
    response = None
    user_query = None
    query_file = None

    try:
        if request.method == 'POST':
            if 'query_pdf_file' in request.FILES:
                query_file = request.FILES['query_pdf_file']

                pdf_reader = PdfReader(query_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_text(text=text)

                embeddings = OpenAIEmbeddings(openai_api_key=gpt_api_key)
                vec_store = FAISS.from_texts(chunks, embeddings)

                file_name = query_file.name[:-4]
                request.session['uploaded_pdf_file_name'] = file_name
                vec_store.save_local(os.path.join("PDF_Embeddings", f"{file_name}"))

            else:
                embeddings = OpenAIEmbeddings(openai_api_key=gpt_api_key)
                file_name = request.session.get('uploaded_pdf_file_name', None)
                vec_store = FAISS.load_local(os.path.join("PDF_Embeddings", f"{file_name}"), embeddings)
        

            user_query = request.POST.get('query_pdf_query')
            result = pdf_query_generator(vec_store, user_query)
            response = result['result']
                
    except Exception as e:
        print(e)
        user_query = request.POST.get('query_pdf_query')
        response = "An error occurred while processing your request. Please try again later."

    return render(request, 'query_pdf.html', {'title': title, 'query': user_query, 'response': response})


# Code Optimizer
def code_optimizer(request):
    title = "Code Optimizer"
    response = None

    if request.method == 'POST':
        user_input = request.POST.get('input_code')
        try:
            response = optimize_code(user_input)
        except:
            response = "An error occurred while processing your request. Please try again later."

    return render(request, 'code_optimizer.html', {'title':title, 'optimized_code':response})

# About
def about(request):
    return render(request, 'about.html')

# Upcoming
def upcoming(request):
    return render(request, 'upcoming.html')