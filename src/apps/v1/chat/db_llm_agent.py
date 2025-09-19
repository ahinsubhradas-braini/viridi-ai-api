from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

from src.core.config import settings


async def db_llm_agent():
    try:
        # Connect to MySQL Database
        VIRIDI_APPLICATION_DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"

        print("VIRIDI_APPLICATION_DATABASE_URL", VIRIDI_APPLICATION_DATABASE_URL)

        db = SQLDatabase.from_uri(VIRIDI_APPLICATION_DATABASE_URL)
    except Exception as dbConnError:
        print("dbConnError ===>", dbConnError)
    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        api_key=settings.gemini_api_key,  # Gemini API key here
        model="gemini-1.5-flash",  # Gemini model
        temperature=0,
        base_url="https://generativelanguage.googleapis.com/v1beta/models",
    )

    # Toolkit
    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm,
        include_tables=["users", "userinvoices", "products"],
        view_support=False,
        max_string_length=500,
    )

    # Agent
    agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

    return agent
