async def is_malicious(query: str) -> bool:
    # Disallow write operations
    blacklist = ["insert", "update", "delete", "drop", "alter", "truncate"]
    return any(word in query.lower() for word in blacklist)


async def secure_db_query_prompt(agent, user_query, user_id, max_retries=3):
    # if is_malicious(user_query):
    #     return {"message": Chatbot_Constants.OUT_OF_DOMAIN_RESPONSE}

    # System prompt to enforce rules
    system_prompt = f"""
    SYSTEM:
    - You are a SQL generator. 
    - Only output valid SQL queries as plain text.
    - Every query must include: WHERE userId = {user_id}.
    - Only use SELECT queries.
    - Never remove or create tables.
    - Must remember you will only query data for userId = {user_id}. Don't do any write operations. 
    - Do not explain anything. Output only the SQL statement.
    """
    final_prompt = f"{system_prompt}\nUser request: {user_query}"
    return agent.invoke(final_prompt)
