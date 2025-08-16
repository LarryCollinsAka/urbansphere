import json
import os

def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_sdg_info(sdg_number):
    kb = load_knowledge_base()
    return kb["sdgs"].get(sdg_number, {})
    
def get_best_practices():
    kb = load_knowledge_base()
    return kb["urban_best_practices"]

def get_air_quality_actions():
    kb = load_knowledge_base()
    return kb["air_quality_actions"]

def get_housing_upgrade_tips():
    kb = load_knowledge_base()
    return kb["housing_upgrade_tips"]

def get_civic_feedback_examples():
    kb = load_knowledge_base()
    return kb["civic_feedback_examples"]