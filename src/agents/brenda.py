# src/agents/brenda.py

from src.agents.agent_base import AgentBase
from src.models.watsonx_service import WatsonxService
import json
import os

class Brenda(AgentBase):
    def __init__(self, watsonx_client: WatsonxService):
        yaml_path = os.path.join(os.path.dirname(__file__), "agent_config/brenda.yml")
        super().__init__(yaml_path)
        self.watsonx_client = watsonx_client

    def orchestrate_message(self, message: str) -> dict:
        """
        Processes a message using structured reasoning and returns a function call with arguments.
        """
        prompt = (
            f"You are Brenda, an AI orchestrator for a city management system. "
            f"Your role is to identify the user's request and determine the correct tool to call. "
            f"Your reasoning should be placed inside <think></think> tags and the final JSON response inside <response></response> tags.\n\n"
            f"You can call the following tools:\n\n"
            f"1. **add_task**: To report a new city issue. Arguments: `issue` (string), `location` (string, optional).\n"
            f"2. **get_task_status**: To check the status of a reported issue. Arguments: `ticket_id` (integer).\n"
            f"3. **greet**: To respond to a greeting. Arguments: `greeting` (string).\n"
            f"4. **get_bin_location**: To find the location of the nearest trash or recycling bin. Arguments: `user_location` (string).\n"
            f"5. **unknown**: To indicate the request cannot be fulfilled. Arguments: `reason` (string).\n\n"
            f"User message: 'The trash bin at the corner of Main St and 1st Ave is overflowing.'\n"
            f"<think>The user is reporting an issue. The best tool is `add_task`. I need to extract the issue and location as arguments.</think>\n"
            f"<response>{{\"tool\": \"add_task\", \"arguments\": {{\"issue\": \"overflowing trash bin\", \"location\": \"Main St and 1st Ave\"}}}}</response>\n"
            f"User message: 'What's the status of my report?'\n"
            f"<think>The user is asking for an update on a report. This corresponds to the `get_task_status` tool. No ticket ID is provided, so the argument will be null.</think>\n"
            f"<response>{{\"tool\": \"get_task_status\", \"arguments\": {{\"ticket_id\": null}}}}</response>\n"
            f"User message: 'Where is the nearest recycling bin?'\n"
            f"<think>The user wants to find a bin. This maps directly to the `get_bin_location` tool. I need to find the user's current location from the context, but since it's not explicitly in the message, the argument is null.</think>\n"
            f"<response>{{\"tool\": \"get_bin_location\", \"arguments\": {{\"user_location\": null}}}}</response>\n"
            f"User message: '{message}'\n"
            f"<think>"
        )

        try:
            response_text = self.watsonx_client.get_completion(prompt)
            
            # Extract the JSON object from within the <response> tags
            response_start = response_text.find('<response>')
            response_end = response_text.find('</response>')
            
            if response_start != -1 and response_end != -1:
                json_string = response_text[response_start + len('<response>'):response_end]
                function_call = json.loads(json_string)
                return function_call
            else:
                # If the model doesn't follow the structured format, we fall back to a safe default
                return {"tool": "unknown", "arguments": {"reason": "failed to parse structured response"}}

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from watsonx.ai: {e}")
            return {"tool": "unknown", "arguments": {"reason": "failed to parse JSON from model"}}
        except Exception as e:
            print(f"Error in Brenda's orchestration: {e}")
            return {"tool": "unknown", "arguments": {"reason": "internal error in orchestration"}}