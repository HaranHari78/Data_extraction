import httpx
import configparser
from openai import AzureOpenAI


def load_config():
    """Load configuration from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def call_openai_api(prompt, model):
    """Call Azure OpenAI API using HTTPX with disabled SSL verification"""
    config = load_config()

    client = AzureOpenAI(
        api_key=config['azure_openai']['api_key'],
        api_version=config['azure_openai']['api_version'],
        azure_endpoint=config['azure_openai']['endpoint'],
        http_client=httpx.Client(verify=False)
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[❌ API Error] {str(e)}")
        return None

