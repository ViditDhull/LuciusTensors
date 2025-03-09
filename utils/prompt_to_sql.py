from utils.api_key import g_api_key
import google.generativeai as genai

genai.configure(api_key = g_api_key)

def generate_sql_query(nlp_prompt):
    try:
        prompt = f"""
        You are an expert SQL query generator. Based on the user's text prompt, 
        generate the most likely SQL query. Provide a very short (1-2 sentence) explanation of the query.
        List all assumptions you made about table names and column names in less than 2-3 lines.
        Assume reasonable names and types for any tables and columns needed.
        The user will use this generated query on their existing database. It's critical
        that you provide well formatted SQL.

        User Prompt: {nlp_prompt}

        SQL Query:
        """
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        return f"Error optimizing code: {str(e)}"