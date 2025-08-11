"""
This module holds global application state to avoid circular imports.
"""

from data.loader import load_agent_configs, load_knowledge_bases
#from utils.memory import session_store

# Load our data into these global variables at startup
agent_configs = load_agent_configs()
knowledge_bases = load_knowledge_bases()

# The session_store is also a shared global variable