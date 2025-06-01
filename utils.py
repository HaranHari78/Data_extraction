import httpx
import configparser
from openai import AzureOpenAI


def load_config():
    """Load configuration from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def call_openai_api(prompt, model):
    """Call Azure OpenAI API with httpx client (SSL verify disabled)"""
    custom_http_client = httpx.Client(verify=False)
    config = load_config()

    client = AzureOpenAI(
        api_key=config['azure_openai']['api_key'],
        api_version=config['azure_openai']['api_version'],
        azure_endpoint=config['azure_openai']['endpoint'],
        http_client=custom_http_client,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        print("[🔁 API Response Preview]", content[:150])
        return content
    except Exception as e:
        print(f"[❌ API Error] {str(e)}")
        return None
