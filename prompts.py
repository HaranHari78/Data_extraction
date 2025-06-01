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

def field_extraction_prompt(text):
    return f"""
    Extract the following fields from this clinical note:

    """{text}"""

    Fields to extract:
    1. AML Diagnosis Date – mm/dd/yyyy format
    2. Precedent Disease — a list of objects, each with:
        - disease name
        - associated date
        - evidence
    3. Performance Status:
        - ECOG and KPS scores with values, dates, and evidence
    4. Mutational Status (genes: NPM1, RUNX1, TP53, FLT3, ASXL1):
        - each with status, date, and evidence

    Return only valid JSON in this format:
    {{
        "document_title": "",
        "aml_diagnosis_date": {{"value": "", "evidence": ""}},
        "precedent_disease": [{{"disease": "", "date": "", "evidence": ""}}],
        "performance_status": {{
            "kps_score": {{"value": "", "date": "", "evidence": ""}},
            "ecog_score": {{"value": "", "date": "", "evidence": ""}}
        }},
        "mutational_status": {{
            "NPM1": {{"status": "", "date": "", "evidence": ""}},
            "RUNX1": {{"status": "", "date": "", "evidence": ""}},
            "TP53": {{"status": "", "date": "", "evidence": ""}},
            "FLT3": {{"status": "", "date": "", "evidence": ""}},
            "ASXL1": {{"status": "", "date": "", "evidence": ""}}
        }}
    }}
    """
