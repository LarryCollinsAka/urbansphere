from src.agents.agent_base import AgentBase
from src.models.watsonx_service import WatsonxService
from src.models.db_models import Task, db

class Qumy(AgentBase):
    def __init__(self, watsonx_client: WatsonxService):
        super().__init__(watsonx_client)

    def add_task(self, sender_id: str, message_body: str, intent: str) -> Task:
        new_task = Task(
            sender_id=sender_id,
            message_body=message_body,
            intent=intent
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def get_task(self, task_id: int) -> Task:
        return Task.query.get(task_id)

    def update_task_status(self, task_id: int, new_status: str):
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            db.session.commit()
            return True
        return False