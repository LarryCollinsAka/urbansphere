from .agent_base import AgentBase
import os

import json
from src.agents.agent_base import AgentBase
from src.models.watsonx_service import WatsonxService

class Uby(AgentBase):
    def __init__(self, watsonx_client: WatsonxService):
        super().__init__(watsonx_client)

    def get_bin_location(self, user_location: str) -> str:
        mock_data = {
            "Main St and 1st Ave": "The nearest bin is at Main St and 3rd Ave.",
            "City Center": "The nearest bin is near the City Hall fountain."
        }
        
        # In a real app, you would use user_location to query a GIS database.
        response = mock_data.get(user_location, "I could not find a bin near that location.")
        
        return response

    def provide_informed_advice(self, data: dict) -> str:
        prompt = (
            f"You are Uby, an expert urban data analyst. "
            f"Provide a short, actionable piece of advice based on the following data: {json.dumps(data)}.\n"
            f"Drafted advice:"
        )

        try:
            response_text = self.watsonx_client.get_completion(prompt, temperature=0.5, max_tokens=100)
            return response_text
        except Exception as e:
            print(f"Error in Uby's processing: {e}")
            return "Sorry, I am unable to analyze that data at this time."