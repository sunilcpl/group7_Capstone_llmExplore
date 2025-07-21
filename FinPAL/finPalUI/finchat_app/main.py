from fastapi import FastAPI
from chainlit.utils import mount_chainlit
import uvicorn
#from financial_planner import generate_financial_plan
#from finPalChatNew import FinPalAgent, llm, tools, SYSTEM_MESSAGE_CONTENT,tool_map
app = FastAPI()


# @app.get("/app")
# async def get_financial_plan(message: str):
#     """FastAPI route to get financial planning advice."""
#     print("Callling financial planner with message:", message)
#     try:
#         # Get financial plan from LangChain and FinGPT
#         langchain_advice = generate_financial_plan(message)
#         return {
#             "langchain_advice": langchain_advice,
#         }
#     except Exception as e:
#         return {"error": str(e)}


mount_chainlit(app=app, target="finchat_app.py", path="/chainlit")
# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
