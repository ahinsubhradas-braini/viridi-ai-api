# Imports fastapi dependices
from fastapi import HTTPException

# Imports from project or 3rd party libary dependices
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from src.core.config import settings

async def db_llm_agent():
    try:
        # Connect to MySQL Database
        db = SQLDatabase.from_uri(settings.VIRIDI_APPLICATION_DATABASE_URL)

        # LLM
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)

        # Toolkit
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # Agent
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True
        )

        return agent
    except Exception as e:
        print(f"Error initializing db_llm_agent: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")    