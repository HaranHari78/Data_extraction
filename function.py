# functions.py

schema = {
    "name": "extract_clinical_data",
    "description": "Extract structured cancer-related clinical information from unstructured medical text.",
    "parameters": {
        "type": "object",
        "properties": {
            "document_title": {"type": "string"},
            "aml_diagnosis_date": {
                "type": "object",
                "properties": {
                    "value": {"type": "string", "description": "AML diagnosis date in mm/dd/yyyy format"},
                    "evidence": {"type": "string"}
                },
                "required": ["value", "evidence"]
            },
            "precedent_disease": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "disease": {"type": "string"},
                        "date": {"type": "string"},
                        "evidence": {"type": "string"}
                    },
                    "required": ["disease", "date", "evidence"]
                }
            },
            "performance_status": {
                "type": "object",
                "properties": {
                    "kps_score": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "date": {"type": "string"},
                            "evidence": {"type": "string"}
                        },
                        "required": ["value", "date", "evidence"]
                    },
                    "ecog_score": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "date": {"type": "string"},
                            "evidence": {"type": "string"}
                        },
                        "required": ["value", "date", "evidence"]
                    }
                },
                "required": ["kps_score", "ecog_score"]
            },
            "mutational_status": {
                "type": "object",
                "properties": {
                    gene: {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "date": {"type": "string"},
                            "evidence": {"type": "string"}
                        },
                        "required": ["status", "date", "evidence"]
                    } for gene in ["NPM1", "RUNX1", "TP53", "FLT3", "ASXL1"]
                },
                "required": ["NPM1", "RUNX1", "TP53", "FLT3", "ASXL1"]
            }
        },
        "required": ["document_title", "aml_diagnosis_date", "precedent_disease", "performance_status", "mutational_status"]
    }
}
