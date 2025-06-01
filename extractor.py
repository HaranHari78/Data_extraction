import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
import httpx  # ✅ import httpx for SSL bypass

from prompts import function_calling_prompt
from functions import schema

load_dotenv()

# ✅ Disable SSL certificate verification (for testing only)
custom_http_client = httpx.Client(verify=False)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    http_client=custom_http_client  # ✅ inject httpx client
)

MODEL = os.getenv("AZURE_OPENAI_MODEL")
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

            message = response.choices[0].message
            arguments = message.function_call.arguments
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
