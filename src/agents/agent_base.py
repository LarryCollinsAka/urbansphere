import yaml
import os

class AgentBase:
    def __init__(self, yaml_path):
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
        self.name = config.get("agent_name", "Agent")
        self.purpose = config.get("purpose", "")
        self.personality_traits = config.get("personality_traits", [])

    def introduce(self):
        traits = ', '.join(self.personality_traits)
        return f"Hi, I'm {self.name}. My purpose: {self.purpose} My personality: {traits}."