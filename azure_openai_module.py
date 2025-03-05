import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

def get_azure_openai_response(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": messages
    }
    response = requests.post(f"{endpoint}/openai/deployments/gpt-4/chat/completions", headers=headers, json=data)
    return response.json()
