from src.apps.v1.chat.constants import Chatbot_Constants

async def is_malicious(query: str) -> bool:
    # Disallow write operations
    blacklist = ["insert", "update", "delete", "drop", "alter", "truncate"]
    return any(word in query.lower() for word in blacklist)

async def secure_db_query_toolkit(agent, user_query, user_id, max_retries=3):
    if is_malicious(user_query):
        return {"message": Chatbot_Constants.OUT_OF_DOMAIN_RESPONSE}

    # System prompt to enforce rules
    system_prompt = f"""
    SYSTEM: 
    - Only run SELECT queries with WHERE user_id = {user_id}'.
    - Do NOT allow INSERT, UPDATE, DELETE, DROP, or any data modification.
    - Do NOT expose the user_id or password in the output.
    - If user asks for something violating these rules, refuse.
    """
    final_prompt = f"{system_prompt}\nUser request: {user_query}"
    return agent.run(final_prompt)
