from src.agents.agent_base import AgentBase
from src.models.watsonx_service import WatsonxService
from src.agents.qumy import Qumy

class Sanita(AgentBase):
    def __init__(self, watsonx_client: WatsonxService, qumy_client: Qumy):
        super().__init__(watsonx_client)
        self.qumy_client = qumy_client

    def process_sanitation_issue(self, task_id: int) -> str:
        task = self.qumy_client.get_task(task_id)
        if not task:
            return "Sorry, I could not find that task in the queue."

        prompt = (
            f"You are Sanita, a helpful AI agent for the city's sanitation department. "
            f"A citizen has reported a sanitation issue. Your job is to draft a polite, "
            f"professional confirmation message, stating that the issue has been received "
            f"and a team has been dispatched. Do not mention a specific task ID.\n\n"
            f"Citizen's report: '{task.message_body}'\n\n"
            f"Drafted response: "
        )

        try:
            response_text = self.watsonx_client.get_completion(prompt, temperature=0.7, max_tokens=150)
            self.qumy_client.update_task_status(task_id, 'In Progress')
            return response_text
        except Exception as e:
            print(f"Error in Sanita's processing: {e}")
            self.qumy_client.update_task_status(task_id, 'Error')
            return "Sorry, I am unable to process that request at this time."