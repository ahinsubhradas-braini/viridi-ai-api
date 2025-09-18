# # Import python core libary dependices
# import asyncio

# # Imports fastapi dependices
# from fastapi import APIRouter,Request
# from fastapi.responses import StreamingResponse

# # Imports from project or 3rd party libary dependices
# from src.apps.v1.chat.schemas.chatbot_request import SessionRequest
# from src.common.logger import logger
# from src.apps.v1.chat.service import ChatService
# from src.common.response.stream_response_helper import Stream_response_helper
# from src.common.security.reate_limiter import limit_request
# from src.apps.v1.chat.intent_model import predict_intent
# from src.apps.v1.chat.constants import Chatbot_Constants

# router = APIRouter()

# @router.get("/sessions")
# async def get_sessions(request: Request):
#     logger.info("FastAPI app started successfully")
#     return {"message": "Sessions data"}

# @router.post("/session")
# @limit_request("1/minute")
# async def session(request:Request,session_data: SessionRequest):
#     # Calling with thread pool executor to avoid blocking the main event loop
#     check_prediction_intent = await asyncio.to_thread(predict_intent, session_data.user_query, 0.5)

#     if(check_prediction_intent['score'] < 0.5 or check_prediction_intent['intent'] == 'out_of_domain'):
#         return {"message": Chatbot_Constants.OUT_OF_DOMAIN_RESPONSE}
#     elif check_prediction_intent['intent'] == 'greetings':
#      return {"message": f"Hello {session_data.user_name} I am viridi ai, how can I help you ?"}
#     else:
#         # Call the chatbot service to do the query and send the response as stream
#         query_response = await ChatService.get_query_result(session_data.user_query, session_data.user_id)

#         print("query_response",query_response)

#         async def event_generator():
#             async for event in Stream_response_helper.fake_sse():
#                 yield event

#         return StreamingResponse(event_generator(), media_type="text/event-stream")
