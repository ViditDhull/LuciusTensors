import openai
from utils.api_key import api_key

openai.api_key = api_key

def generate_sql_query(nl_prompt):
    prompt = f"Generate an SQL query to the prompt: {nl_prompt}"
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 200
    )
    
    sql_query = response.choices[0].text.strip()
    return sql_query