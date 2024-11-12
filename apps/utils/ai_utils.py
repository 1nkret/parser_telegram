import google.generativeai as genai
import os
import time


def response_ai(text: str, prompt: str) -> str:
    genai.configure(api_key=os.getenv("API_KEY_AI"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    try:
        response = model.generate_content(f"{prompt}\n{text}")
        return response.text
    except ValueError:
        raise "Violation of community rules."


def test_response(arr: list, start_pos: int, test_prompt: str):
    for i in range(start_pos, len(arr)):
        print(f"{arr[i]} - category: {response_ai(arr[i], test_prompt)}")
        time.sleep(2)

