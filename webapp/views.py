import base64
from io import BytesIO
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

    query_file = request.session.get('query_file', None)

    if request.method == 'POST':
        if 'query_pdf_file' in request.FILES:
            query_file = request.FILES['query_pdf_file']
            query_file = base64.b64encode(query_file.read()).decode('utf-8')
            request.session['query_file'] = query_file

            user_query = request.POST.get('query_pdf_query')
            try:
                query_file_content = base64.b64decode(query_file)
                query_file = BytesIO(query_file_content)
                query_file.name = "query_file.pdf"
                result = pdf_query_generator(query_file, user_query)

                response = result['result']
                
            except Exception as e:
                print(e)
                response = "An error occurred while processing your request. Please try again later."

    return render(request, 'query_pdf.html', {'query_file': query_file, 'title': title, 'query': user_query, 'response': response})


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