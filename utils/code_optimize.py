from utils.api_key import g_api_key
import google.generativeai as genai

genai.configure(api_key = g_api_key)

def optimize_code(user_code):
    try:
        prompt = f"""
                You are an expert code optimizer. Optimize the following code for readability, efficiency, and best practices, 
                while strictly preserving its original functionality. Explain the changes you made in a very short comment before presenting the optimized code.
                
                Code to optimize:\n\n{user_code}

                Optimized Code:
            """
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        return f"Error optimizing code: {str(e)}"