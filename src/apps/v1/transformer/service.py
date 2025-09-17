# Import python core libary dependices
import requests
import json
import os

# Imports from project or 3rd party libary dependices
from src.apps.v1.transformer.transformer_agent import TransformerAgent
from src.core.config import settings

def transform_data(api_data_url: dict,api_provider_name:str):
    """
    Transform 3rd party api response data
    """
    return {"data":""}
    # Fetch json data from the provided api_data_url
    input_schema = fetch_data_from_url(api_data_url)
    # Fetch json output from directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(current_dir,"output", "output_schema.json")
    output_schema = get_output_schema_from_directory(json_path)
    
    # Calling transformer class
    transformer = TransformerAgent(
        api_key=settings.open_router_key,
        base_url=settings.open_router_url,
        model=settings.open_router_model,
        timeout=settings.llm_timeout
    )
    # # Calling transformer method to transform data
    get_transformer_response = transformer.generate_transformer(
        input_schema= input_schema,
        output_schema= output_schema,
        api_provider_name = api_provider_name
    )

    return get_transformer_response

def fetch_data_from_url(url: str):
    """
    Fetch json data from node.js server object url
    """
    response = requests.get(url).json()
    return response
    
def get_output_schema_from_directory(json_path: str):
    """
    Read the json path from output and 
    """
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    return data