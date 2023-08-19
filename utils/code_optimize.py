import openai
from utils.api_key import api_key

openai.api_key = api_key

def optimize_code(user_code):
    prompt = f"Optimize the given code while preserving its original functionality:\n\n{user_code}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    
    optimized_code = response.choices[0].text.strip()
    return optimized_code