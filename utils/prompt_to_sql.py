from utils.api_key import api_key
import google.generativeai as genai

genai.configure(api_key = api_key)

def generate_sql_query(nlp_prompt):
    prompt = f"Write a sql query for this prompt and do not inlcude 'sql' or any other text in response {nlp_prompt}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text