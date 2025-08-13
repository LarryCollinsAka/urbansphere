from .agent_base import AgentBase
import os

class SanitaAgent(AgentBase):
    def __init__(self):
        yaml_path = os.path.join(os.path.dirname(__file__), "agent_config/sanita.yml")
        super().__init__(yaml_path)

    # Add Sanita-specific logic here