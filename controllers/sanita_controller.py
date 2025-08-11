from datetime import datetime

# In the future, we will have a real-time data store for waste reports.
# For now, we'll use a simple in-memory list as a placeholder.
sanita_reports = []

def sanita_orchestrator(user_message):
    """
    This is the main orchestrator for the Sanita agent.
    It processes a user's message related to waste reports and generates a response.
    """
    # 1. Process the incoming message. In the future, this is where we'd use a
    #    Language Model (LLM) to extract details like location and severity.
    print(f"Sanita received a message: {user_message}")

    # 2. Simulate saving a waste report.
    report = {
        "user_message": user_message,
        "timestamp": datetime.now().isoformat(),
        "status": "received"
    }
    sanita_reports.append(report)
    print(f"Sanita has received {len(sanita_reports)} reports so far.")

    # 3. Generate a dynamic response.
    response = "Thank you for reporting the waste problem! Sanita has logged your report and our team is on it."

    return response