# extractor.py (using config.ini with full typing and no warnings)

import os
import json
import pandas as pd
import configparser
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionUserMessageParam
import httpx
import logging

from prompts import function_calling_prompt
from functions import schema

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load config.ini

def load_config():
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    return parser

cfg = load_config()

client = AzureOpenAI(
    api_key=cfg["azure_openai"]["api_key"],
    api_version=cfg["azure_openai"]["api_version"],
    azure_endpoint=cfg["azure_openai"]["endpoint"],
    http_client=httpx.Client(verify=False)
)

MODEL = cfg["gpt_models"]["model_gpt4o"]
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
    flat_rows = []

    for idx, row in df.iterrows():
        title = row.get("title", "")
        text = row.get("text", "")
        row_num = int(idx) + 1

        logging.info(f"[Processing] Row {row_num}: {title[:40]}...")

        if not text:
            continue

        prompt = function_calling_prompt(title, text)

        messages: list[ChatCompletionUserMessageParam] = [
            {"role": "user", "content": prompt}
        ]

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                functions=[schema],
                function_call={"name": "extract_clinical_data"},
            )

            arguments = response.choices[0].message.function_call.arguments
            parsed = clean_response(arguments)

            if parsed:
                results.append(parsed)
                flat_rows.append({"document_title": parsed.get("document_title", ""),
                                  "aml_diagnosis_date": parsed.get("aml_diagnosis_date", {}).get("value", ""),
                                  "ecog_score": parsed.get("performance_status", {}).get("ecog_score", {}).get("value", "")})
            else:
                logging.warning(f"[Warning] Invalid JSON for row {row_num}")

        except Exception as e:
            logging.error(f"[Error] Row {row_num}: {str(e)}")
            continue

    output_json_path = os.path.join(OUTPUT_DIR, "structured_output.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    output_csv_path = os.path.join(OUTPUT_DIR, "structured_output.csv")
    pd.DataFrame(flat_rows).to_csv(output_csv_path, index=False)

    logging.info(f"✅ Extracted data saved to: {output_json_path} and {output_csv_path}")
