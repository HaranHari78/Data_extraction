# extractor.py (using config.ini)

import os
import json
import pandas as pd
import configparser
from openai import AzureOpenAI
import httpx

from prompts import function_calling_prompt
from functions import schema

# Load config.ini

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

config = load_config()

client = AzureOpenAI(
    api_key=config["azure_openai"]["api_key"],
    api_version=config["azure_openai"]["api_version"],
    azure_endpoint=config["azure_openai"]["endpoint"],
    http_client=httpx.Client(verify=False)  # Optional SSL bypass
)

MODEL = config["gpt_models"]["model_gpt4o"]
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_response(raw: str):
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None

def extract_data_from_csv(csv_path: str):
    df = pd.read_csv(csv_path)
    results = []

    for idx, row in df.iterrows():
        title = row.get("title", "")
        text = row.get("text", "")
        row_num = int(idx) + 1

        print(f"\n[Processing] Row {row_num}: {title[:40]}...")

        if not text:
            continue

        prompt = function_calling_prompt(title, text)

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                functions=[schema],
                function_call={"name": "extract_clinical_data"},
            )

            arguments = response.choices[0].message.function_call.arguments
            parsed = clean_response(arguments)

            if parsed:
                results.append(parsed)
            else:
                print(f"[⚠️ Warning] Invalid JSON for row {row_num}")

        except Exception as e:
            print(f"[❌ Error] Row {row_num}: {str(e)}")
            continue

    output_path = os.path.join(OUTPUT_DIR, "structured_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Extracted data saved to: {output_path}")
