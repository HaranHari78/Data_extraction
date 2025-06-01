schema = {
    "name": "extract_clinical_data",
    "description": "Extract clinical data fields from an AML patient's note.",
    "parameters": {
        "type": "object",
        "properties": {
            "document_title": {"type": "string"},
            "aml_diagnosis_date": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "evidence": {"type": "string"}
                }
            },
            "precedent_disease": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "disease": {"type": "string"},
                        "date": {"type": "string"},
                        "evidence": {"type": "string"}
                    }
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
                        }
                    },
                    "ecog_score": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "date": {"type": "string"},
                            "evidence": {"type": "string"}
                        }
                    }
                }
            },
            "mutational_status": {
                "type": "object",
                "properties": {
                    "NPM1": {"$ref": "#/definitions/mutation"},
                    "RUNX1": {"$ref": "#/definitions/mutation"},
                    "TP53": {"$ref": "#/definitions/mutation"},
                    "FLT3": {"$ref": "#/definitions/mutation"},
                    "ASXL1": {"$ref": "#/definitions/mutation"}
                }
            }
        },
        "required": ["document_title"]
    },
    "definitions": {
        "mutation": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "date": {"type": "string"},
                "evidence": {"type": "string"}
            }
        }
    }
}
