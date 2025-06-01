# extractor.py
import json
import pandas as pd
import os
from dotenv import load_dotenv

from openai import AzureOpenAI
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionFunctionParam,
    FunctionCall
)

from prompts import function_calling_prompt
from functions import schema

load_dotenv()

# Azure OpenAI client setup
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

MODEL = os.getenv("AZURE_OPENAI_MODEL")
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_response(raw: str):
    """Clean and parse JSON string"""
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def extract_data_from_csv(csv_path: str):
    df = pd.read_csv(csv_path)
    results = []

    for index, row in df.iterrows():
        title = row.get("title", "")
        text = row.get("text", "")
        print(f"\n[Processing] Row {index + 1}: {title[:40]}...")

        if not text:
            continue

        prompt = function_calling_prompt(title, text)

        messages: list[ChatCompletionUserMessageParam] = [
            {"role": "user", "content": prompt}
        ]
        functions: list[ChatCompletionFunctionParam] = [schema]
        function_call = FunctionCall(name="extract_clinical_data")

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                functions=functions,
                function_call=function_call,
            )

            function_args = response.choices[0].message.function_call.arguments
            parsed = clean_response(function_args)

            if parsed:
                results.append(parsed)
            else:
                print(f"[Warning] Empty or invalid JSON for row {index + 1}")

        except Exception as e:
            print(f"[Error] Row {index + 1} - {str(e)}")
            continue

    output_path = os.path.join(OUTPUT_DIR, "structured_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Extracted data saved to: {output_path}")
