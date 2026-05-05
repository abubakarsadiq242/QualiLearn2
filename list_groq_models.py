import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/models"
headers = {
    'Authorization': f'Bearer {api_key}'
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        models = response.json().get('data', [])
        for m in models:
            print(f"Model: {m['id']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
