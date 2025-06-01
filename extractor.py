# extractor.py (clean version using utils structure)

import os
import json
import pandas as pd
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionFunctionCallOptionParam
)

from prompts import function_calling_prompt
from functions import schema
from utils import get_openai_client, get_model

client = get_openai_client()
MODEL = get_model()
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

    for row_num in range(len(df)):
        row = df.iloc[row_num]
        title = row.get("title", "")
        text = row.get("text", "")

        print(f"[Processing] Row {row_num}: {title[:40]}...")

        if not text:
            continue

        prompt = function_calling_prompt(title, text)

        messages: list[ChatCompletionUserMessageParam] = [
            {"role": "user", "content": prompt}
        ]

        function_call: ChatCompletionFunctionCallOptionParam = {"name": "extract_clinical_data"}

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                functions=[schema],
                function_call=function_call,
            )

            arguments = response.choices[0].message.function_call.arguments
            parsed = clean_response(arguments)

            if parsed:
                results.append(parsed)
                flat_rows.append({
                    "document_title": parsed.get("document_title", ""),
                    "aml_diagnosis_date": parsed.get("aml_diagnosis_date", {}).get("value", ""),
                    "ecog_score": parsed.get("performance_status", {}).get("ecog_score", {}).get("value", "")
                })
            else:
                print(f"[Warning] Invalid JSON for row {row_num}")

        except Exception as e:
            print(f"[Error] Row {row_num}: {str(e)}")
            continue

    output_json_path = os.path.join(OUTPUT_DIR, "structured_output.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    output_csv_path = os.path.join(OUTPUT_DIR, "structured_output.csv")
    pd.DataFrame(flat_rows).to_csv(output_csv_path, index=False)

    print(f"\n✅ Extracted data saved to: {output_json_path} and {output_csv_path}")
