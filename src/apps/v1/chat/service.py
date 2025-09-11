# Imports from project or 3rd party libary dependices
from src.apps.v1.chat.db_llm_agent import db_llm_agent
from src.apps.v1.chat.db_query_prompts import secure_db_query_prompt
class ChatService:
    async def get_query_result(user_query: str, user_id: int):
        # Initialize the database LLM agent
        agent = await db_llm_agent()

        return await secure_db_query_prompt(agent, user_query,user_id, max_retries=3)