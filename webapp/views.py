from django.shortcuts import render
from utils.prompt_to_sql import generate_sql_query
from utils.code_optimize import optimize_code
from utils.query_pdf import pdf_query_generator
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

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
    global in_memory_pdf_buffer

    if request.method == 'POST':
        if 'query_pdf_file' in request.FILES:
            query_file = request.FILES['query_pdf_file']
            buffer = io.BytesIO()
            for chunk in query_file.chunks():
                buffer.write(chunk)

            # Store the in-memory PDF buffer for future use
            in_memory_pdf_buffer = buffer

        else:
            if in_memory_pdf_buffer:
            
                query_file = InMemoryUploadedFile(
                in_memory_pdf_buffer, None, 'example.pdf', 'application/pdf', len(in_memory_pdf_buffer.getvalue()), None
                )
        

        user_query = request.POST.get('query_pdf_query')
        try:
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
def privacy_policy(request):
    return render(request, 'privacy_policy.html')
