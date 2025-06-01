# prompts.py

def function_calling_prompt(title: str, text: str) -> str:
    """Prompt for structured data extraction with function calling"""
    return f"""
You are an expert medical NLP assistant. Extract structured clinical data for an AML cancer patient.

Document Title: {title}

Clinical Text:
\"\"\"
{text}
\"\"\"

Extract the following in JSON format:
1. AML Diagnosis Date — mm/dd/yyyy
2. Precedent Diseases — name, date, evidence
3. Performance Status — ECOG & KPS scores, dates, and evidence
4. Mutational Status for NPM1, RUNX1, TP53, FLT3, ASXL1 — status, date, evidence

Be accurate and extract only if clearly mentioned. Otherwise, mark fields as "Not mentioned".
"""
