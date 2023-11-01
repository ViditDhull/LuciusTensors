from django.shortcuts import render
from django.http import JsonResponse
from utils.prompt_to_sql import generate_sql_query
from utils.code_optimize import optimize_code
from utils.query_pdf import pdf_query_generator

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
    if request.method == 'POST' and request.FILES['query_pdf_file']:
        upload = request.FILES['query_pdf_file']
        user_query = request.POST.get('query_pdf_query')
        try:
            result = pdf_query_generator(upload, user_query)
            response = result['result']
           
        except:
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