import os
import json

def load_agent_configs():
    """
    Loads all agent configurations from JSON files in the data/agents directory.
    Returns a dictionary of agent configurations.
    """
    agent_configs = {}
    config_dir = os.path.join('data', 'agents')
    try:
        for filename in os.listdir(config_dir):
            if filename.endswith('.json'):
                agent_name = filename.split('.')[0]
                with open(os.path.join(config_dir, filename), 'r') as f:
                    agent_configs[agent_name] = json.load(f)
        print("Agent configurations loaded successfully.")
    except FileNotFoundError:
        print(f"WARNING: '{config_dir}' directory not found. Please create it.")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error in file: {filename}. Error: {e}")
        
    return agent_configs

def load_knowledge_bases():
    """
    Loads all RAG knowledge bases from JSON files in the data/knowledge_base directory.
    Returns a dictionary of knowledge bases.
    """
    knowledge_bases = {}
    kb_dir = os.path.join('data', 'knowledge_base')
    try:
        for filename in os.listdir(kb_dir):
            if filename.endswith('.json'):
                agent_name = filename.split('_data')[0]
                with open(os.path.join(kb_dir, filename), 'r') as f:
                    knowledge_bases[agent_name] = json.load(f)
        print("Knowledge bases loaded successfully.")
    except FileNotFoundError:
        print(f"WARNING: '{kb_dir}' directory not found. Please create it.")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error in file: {filename}. Error: {e}")

    return knowledge_bases
