# utils.py

import configparser

import httpx
from openai import AzureOpenAI

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def call_openai_api(prompt: str, model: str):
    custom_http_client = httpx.Client(verify=False)
    config = load_config()
    try:
        client = AzureOpenAI(
            api_key=config['azure_openai']['api_key'],
            api_version=config['azure_openai']['api_version'],
            azure_endpoint=config['azure_openai']['endpoint'],
            http_client=custom_http_client

        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API error: {e}")
        return ""
