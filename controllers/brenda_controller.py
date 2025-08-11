from controllers.sanita_controller import sanita_orchestrator
from services.watsonx_llm import call_llm
import globals as app_globals

def brenda_orchestrator(user_message, conversation_history):
    """
    This is the main orchestrator for the Brenda agent.
    It routes the user's message to the appropriate sub-agent based on intent.
    """
    conversation_history.append({"role": "user", "agent": "processing...", "user": user_message, "response": ""})

    # Simple intent recognition based on keywords. This can be replaced by an LLM in the future.
    if any(keyword in user_message.lower() for keyword in ["waste", "trash", "garbage", "sanitation"]):
        # The user's intent is about waste. Delegate to the Sanita agent.
        brenda_response = sanita_orchestrator(user_message)
        
    else:
        # No specific intent recognized, use Brenda's default response.
        # This will be replaced with an LLM call later in development.
        brenda_response = "Hello, this is Brenda. I'm currently the only agent online. How can I help you today?"

    # Update the last conversation entry with the Brenda response and final agent name
    conversation_history[-1]["response"] = brenda_response
    conversation_history[-1]["agent"] = "brenda"
    conversation_history[-1]["user"] = user_message

    return brenda_response, conversation_history
