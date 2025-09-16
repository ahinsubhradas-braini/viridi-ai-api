# from langchain_community.utilities import SQLDatabase
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from langchain.agents import create_sql_agent
# from src.core.config import settings
# from langchain_google_genai import ChatGoogleGenerativeAI

# async def db_llm_agent():
#     # Connect to MySQL Database
#     VIRIDI_APPLICATION_DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"
#     db = SQLDatabase.from_uri(VIRIDI_APPLICATION_DATABASE_URL)

#     # Gemini LLM
#     llm = ChatGoogleGenerativeAI(
#         api_key=settings.gemini_api_key,       # Gemini API key here
#         model="gemini-1.5-flash",         # Gemini model
#         temperature=0,
#         base_url = "https://generativelanguage.googleapis.com/v1beta/models"
#     )
    
#     # Toolkit
#     toolkit = SQLDatabaseToolkit(db=db, llm=llm)

#     # Agent
#     agent = create_sql_agent(
#         llm=llm,
#         toolkit=toolkit,
#         verbose=True
#     )

#     return agent
