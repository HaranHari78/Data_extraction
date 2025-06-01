# utils.py

import configparser
import httpx
from openai import AzureOpenAI

_client = None
_model = None

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def get_openai_client():
    global _client
    if _client is None:
        config = load_config()
        _client = AzureOpenAI(
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"],
            azure_endpoint=config["azure_openai"]["endpoint"],
            http_client=httpx.Client(verify=False)
        )
    return _client

def get_model():
    global _model
    if _model is None:
        config = load_config()
        _model = config["gpt_models"]["model_gpt4o"]
    return _model
