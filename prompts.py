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
    You are analyzing a clinical note for an AML cancer patient.

    Extract the following fields according to the provided function schema:
    - AML Diagnosis Date
    - Precedent Disease with name, date, and evidence
    - Performance Status (ECOG and KPS scores with dates and evidence)
    - Mutational Status (NPM1, RUNX1, TP53, FLT3, ASXL1 — each with status, date, and evidence)

    Clinical Note:
    """{text}"""
    """
