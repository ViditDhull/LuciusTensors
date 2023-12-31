from utils.api_key import api_key
import google.generativeai as genai

genai.configure(api_key = api_key)

def optimize_code(user_code):
    prompt = f"Optimize the given code while preserving its original functionality:\n\n{user_code}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text