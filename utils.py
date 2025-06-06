import httpx
import configparser
from openai import AzureOpenAI
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
def call_openai_api(prompt, model):
    custom_http_client = httpx.Client(verify=False)
    openai_config = load_config()
    # AzureOpenAI client using the custom HTTP client
    openai_client = AzureOpenAI(
        api_key=openai_config["azure_openai"]["api_key"],
        api_version=openai_config["azure_openai"]["api_version"],
        azure_endpoint=openai_config["azure_openai"]["endpoint"],
        http_client=custom_http_client
    )
    try:
         response = openai_client.chat.completions.create(
         model=model,messages=[{"role": "user", "content": f"{prompt}"}])
         print(response.choices[0].message.content)
         return response.choices[0].message.content
    except Exception as e:
        print("Error during API call:", e)
        return
