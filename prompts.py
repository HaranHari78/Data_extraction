def sentence_extraction_prompt(title, text):
    return f"""
    You are analyzing a clinical document for an AML cancer patient.
    Extract all sentences that contain potential evidence for the following categories:
    1. AML Diagnosis Date
    2. Precedent Disease (with the date of mention)
    3. Performance Status at Baseline:
        - ECOG score (0-4)
        - Karnofsky score (KPS)
        - With associated dates
    4. Mutational Status (with gene name + value + date if available):
        - NPM1, RUNX1, TP53, FLT3, ASXL1

    Document Title: {title}
    Document Text:
    {text}

    Return a JSON like:
    {{
        "document_title": "{title}",
        "aml_diagnosis_sentences": [],
        "precedent_disease_sentences": [],
        "performance_status_sentences": [],
        "mutational_status_sentences": []
    }}
    """


def field_extraction_prompt(text: str):
    return f"""
You are a medical language model trained to extract structured clinical data from patient notes.

From the clinical note below, extract **mutation status** information for the following genes:
- NPM1, TP53, FLT3, ASXL1

Look specifically for phrases indicating:
- Whether the gene is **mutated**, **wild type**, **not mutated**, **positive**, or **negative**
- Also capture **date of test** if mentioned
- Always include the **exact sentence** as evidence

📌 Important:
- If a gene is only mentioned but **no status** is given (like mutated or wild type), leave "status" as empty string but still return the sentence.
- Be strict: only classify a gene as mutated/wild type if it’s clearly stated.

Return output in the following JSON format:

{{
  "mutational_status": {{
    "NPM1": {{"status": "", "date": "", "evidence": ""}},
    "TP53": {{"status": "", "date": "", "evidence": ""}},
    "FLT3": {{"status": "", "date": "", "evidence": ""}},
    "ASXL1": {{"status": "", "date": "", "evidence": ""}}
  }}
}}

Clinical Note:
\"\"\"{text}\"\"\"
"""

