# Import necessary modules
# Import from the new globals module
import globals as app_globals

# Brenda's Core Orchestration Logic
def brenda_orchestrator(user_message, conversation_history):
    """
    Simulates Brenda's NLU and routing logic.
    In the future, this will call an LLM to determine intent and route the message.
    """
    # This is the central hub. It uses an LLM for NLU and routes to agents.
    if "waste" in user_message.lower():
        intent = "sanita_waste_report"
        entities = {"topic": "waste", "location": "unspecified"}
        agent_name = "sanita"
    elif "queue" in user_message.lower():
        intent = "qumy_queue_status"
        entities = {"topic": "queue", "service": "unspecified"}
        agent_name = "qumy"
    else:
        intent = "fallback_unclear"
        entities = {}
        agent_name = "brenda" # Respond directly

    updated_history = conversation_history + [{'user': user_message, 'agent': 'processing...'}]

    agent_response = "I'm sorry, I couldn't understand that."
    
    # We can access agent configs from our global state
    if agent_name == "sanita":
        agent_config = app_globals.agent_configs.get("sanita", {})
        # This is where we would call the Sanita agent
        agent_response = f"Sanita here! I received your message about {entities.get('topic', 'waste')}. I'll use our knowledge base to help you."
    elif agent_name == "qumy":
        agent_config = app_globals.agent_configs.get("qumy", {})
        # This is where we would call the Qumy agent
        agent_response = f"Qumy at your service! I've logged your request about {entities.get('topic', 'a queue')}. I can find the wait time for you."
    else:
        # Fallback response from Brenda herself
        agent_config = app_globals.agent_configs.get("brenda", {})
        agent_response = "Hello, this is Brenda. I'm currently the only agent online. How can I help you today?"
        
    updated_history[-1]['agent'] = agent_response

    return agent_response, updated_history
