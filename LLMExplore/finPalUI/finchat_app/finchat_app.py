import chainlit as cl
import os
from dotenv import load_dotenv
import sys
print(f"Chainlit Version: {cl.__version__}")
##Set the root directory for finPal and  add the finPal root directory to the system path
# This is necessary to ensure that the finPalAgent can be imported correctly
finpal_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

finpal_agent_dir = r"C:\Users\malum\LLMExplore"
if finpal_agent_dir not in sys.path:
    sys.path.insert(0, finpal_agent_dir)

from finPalChatNew import FinPalAgent, llm, tools, SYSTEM_MESSAGE_CONTENT

@cl.on_chat_start
async def start():
    """
    This function is called at the start of a new chat session.
    It initializes the FinPalAgent and stores it in the user session.
    """
    # # Create the custom avatar for your agent
    # await cl.Avatar(
    #     name="FinPal", # This name must match the 'author' in your messages
    #     path="./static/finPalLogo.png" # The path to your image file
    # ).send()
    
    # Create a new instance of the custom agent for each session
    # This ensures each user has their own chat history and state.
    agent_instance = FinPalAgent(
        llm=llm, # Use the already initialized LLM from finPalChatNew
        tools=tools, # Use the tools from finPalChatNew
        system_message_content=SYSTEM_MESSAGE_CONTENT
    )
    # Store the agent instance in the user session for persistence across messages
    cl.user_session.set("agent", agent_instance)
    

    await cl.Message(
        content="Hello! I'm FinPal , your personal financial advisor. How can I help you today?",
        author="FinPal", # Specify the author to use the custom avatar
       
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """
    This function is called every time a user sends a message.
    It retrieves the FinPalAgent from the session and processes the user's query.
    """
    # Retrieve the agent instance for the current session
    agent_instance = cl.user_session.get("agent")  # type: FinPalAgent

    if agent_instance is None:
        await cl.Message(content="FinPal Advisor is not initialized. Please refresh the page.").send()
        return

    try:
        # Use a Chainlit step to show the agent's work in the UI
        async with cl.Step(name="FinPal Agent Processing", type="agent") as step:
            # call the `chat` method of FinPalAgent instance
            # cl.make_async is used to run synchronous functions in an async context,
            # which is necessary for Chainlit's event loop.
            response_content = await cl.make_async(agent_instance.chat)(
                user_query=message.content,
                verbose=True # Set to True to see detailed steps in Chainlit's debug view
            )
            step.output = response_content # Set the final output of the step

        # Send the final response back to the Chainlit UI
        await cl.Message(content=response_content, author="FinPal").send()

    except Exception as e:
        await cl.Message(content=f"FinPal Advisor encountered an error: {e}\nPlease try again or rephrase your query.").send()
        print(f"Error in Chainlit @cl.on_message: {e}")