# main.py

import csv
import json
import re
import os
import pandas as pd
from prompts import sentence_extraction_prompt, field_extraction_prompt
from utils import load_config, call_openai_api

# Configuration
openai_config = load_config()
model = openai_config['gpt_models']['model_gpt4o']
input_file = r"C:\Users\HariharaM12\Downloads\medicaldata.csv"
sentence_output_file = 'extracted_sentences.json'
structured_output_file = 'structured_data.json'
sentence_results = []
structured_results = []

def clean_json_response(response: str):
    """Clean JSON response from OpenAI API"""
    if not response or not isinstance(response, str):
        return ""
    cleaned = re.sub(r'```(?:json)?\n?|\n?```', '', response).strip()
    cleaned = cleaned.replace('\n', ' ')
    return cleaned

# Read input data
df = pd.read_csv(input_file, encoding='utf-8')

for index, row in df.iterrows():
    title = row.get('title', "")
    text = row.get('text', "")
    print(f"\n[Step 1] Analyzing Text: {title[:60]}...")

    if not text:
        continue

    # Prompt 1: Extract relevant sentences
    prompt1 = sentence_extraction_prompt(title, text)
    extracted_sentences_json = call_openai_api(prompt1, model)
    print("[🔍 Raw API Response Snippet]", extracted_sentences_json[:300])

    if not extracted_sentences_json:
        continue

    cleaned_response = clean_json_response(extracted_sentences_json)
    try:
        extracted_sentences = json.loads(cleaned_response)
    except json.JSONDecodeError:
        print("[⚠️ JSON Error] Sentence extraction failed")
        continue

    sentence_results.append(extracted_sentences)

    # Combine all sentences for prompt 2
    combined_text = ". ".join(
        extracted_sentences.get('aml_diagnosis_sentences', []) +
        extracted_sentences.get('precedent_disease_sentences', []) +
        extracted_sentences.get('performance_status_sentences', []) +
        extracted_sentences.get('mutational_status_sentences', [])
    )

    # Prompt 2: Structured extraction
    prompt2 = field_extraction_prompt(combined_text)
    structured_data_json = call_openai_api(prompt2, model)

    if not structured_data_json:
        continue

    cleaned_structured_data_json = clean_json_response(structured_data_json)
    try:
        structured_data = json.loads(cleaned_structured_data_json)
    except json.JSONDecodeError:
        print("[⚠️ JSON Error] Structured data parsing failed")
        continue

    structured_data["document_title"] = title
    structured_results.append(structured_data)

# Save outputs
with open(sentence_output_file, 'w', encoding='utf-8') as f:
    json.dump(sentence_results, f, indent=4)

with open(structured_output_file, 'w', encoding='utf-8') as f:
    json.dump(structured_results, f, indent=4)

print("\n✅ Data saved to output files")
print(f"\n📝 Sentence results saved to: {sentence_output_file} ({len(sentence_results)} records)")
print(f"📝 Structured results saved to: {structured_output_file} ({len(structured_results)} records)")
