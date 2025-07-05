import os
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent #create_tool_calling_agent
from langchain_core.messages import SystemMessage
# Import LlamaCpp for GGUF models
from langchain_community.llms import LlamaCpp
# For streaming output (optional but good for user experience)
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import hub # For pulling a standard ReAct prompt
from pydantic import BaseModel, Field



# --- START: IMPORTANT MODEL PATH UPDATE ---
# Replace this with the actual path to your downloaded GGUF model
# Example: GGUF_MODEL_PATH = "C:\\Users\\malum\\.cache\\huggingface\\hub\\models--us4--fin-llama3.1-8b\\snapshots\\a2f8b1a3d0e9b9d3e8e7c1f8b1d9e2c4b5f6a7d8\\model-q4_k_m.gguf"
# You can copy the path from the 'downloaded_model_path.txt' file you created.
GGUF_MODEL_PATH = "C:\\Users\\malum\\.cache\\huggingface\\hub\\models--us4--fin-llama3.1-8b\\snapshots\\64eb8dc463e78b59e8fa643498b24879fbf85894\\model-q4_k_m.gguf" # <--- **UPDATE THIS LINE**
# Replace <YOUR_SNAPSHOT_HASH> with the actual hash from your downloaded_model_path.txt

if not os.path.exists(GGUF_MODEL_PATH):
    raise FileNotFoundError(
        f"GGUF model not found at specified path: {GGUF_MODEL_PATH}\n"
        "Please update GGUF_MODEL_PATH in finPalLLamaChat.py with the correct path "
        "from your downloaded_model_path.txt file."
    )
# --- END: IMPORTANT MODEL PATH UPDATE ---


# --- Define Tools (as per your previous setup) ---

# --- NEW: Pydantic model for sip_calculator arguments ---
class SIPCalculatorInput(BaseModel):
    monthly_investment: float = Field(description="The amount invested every month, e.g., 5000.")
    annual_interest_rate: float = Field(description="The expected annual rate of return as a decimal, e.g., 0.12 for 12%.")
    years: int = Field(description="The investment tenure in years, e.g., 10.")

@tool(args_schema=SIPCalculatorInput)
def sip_calculator(monthly_investment: float, annual_interest_rate: float, years: int) -> float:
    """
    Calculates the future value of a Systematic Investment Plan (SIP).

    Args:
        monthly_investment (float): The amount invested every month (e.g., 5000).
        annual_interest_rate (float): The expected annual rate of return as a decimal (e.g., 0.12 for 12%).
        years (int): The investment tenure in years (e.g., 10).

    Returns:
        float: The estimated future value of the investment.
    """
    # print(f"\n--- DEBUG: Executing sip_calculator with: monthly_investment={monthly_investment}, annual_interest_rate={annual_interest_rate}, years={years} ---") # Commented out for cleaner test runs
    monthly_rate = annual_interest_rate / 12
    months = years * 12
    if monthly_rate == 0:
        return monthly_investment * months
    future_value = monthly_investment * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
    return future_value

# --- NEW: Pydantic model for currency_converter arguments ---
class CurrencyConverterInput(BaseModel):
    amount: float = Field(description="The amount of money to convert.")
    from_currency: str = Field(description="The currency to convert from (e.g., 'USD', 'INR').")
    to_currency: str = Field(description="The currency to convert to (e.g., 'INR', 'USD').")

@tool(args_schema=CurrencyConverterInput) 
def currency_converter(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Converts an amount from one currency to another using a simplified exchange rate.
    Note: For a real application, this should use a live API for accurate rates.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from (e.g., "USD", "INR").
        to_currency (str): The currency to convert to (e.g., "INR", "USD").

    Returns:
        float: The converted amount.
    """
    # print(f"\n--- DEBUG: Executing currency_converter with: amount={amount}, from_currency='{from_currency}', to_currency='{to_currency}' ---") # Commented out for cleaner test runs
    exchange_rates = {
        "USD_INR": 83.5, # Example rate
        "INR_USD": 1 / 83.5,
        "EUR_USD": 1.08,
        "USD_EUR": 1 / 1.08,
        "GBP_USD": 1.27, # Example
        "USD_GBP": 1 / 1.27, # Example
        # Add more rates as needed
    }
    
    rate_key = f"{from_currency.upper()}_{to_currency.upper()}"
    rate = exchange_rates.get(rate_key)
    
    if rate is None:
        raise ValueError(f"Exchange rate not available for {from_currency} to {to_currency}")
    
    converted_amount = amount * rate
    return converted_amount

tools = [sip_calculator, currency_converter]


# --- Initialize LlamaCpp LLM ---
print(f"Loading GGUF model from: {GGUF_MODEL_PATH}")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path=GGUF_MODEL_PATH,
    temperature=0.3,  # Adjust as needed (0.0 for deterministic, higher for creativity)
    max_tokens=2048,  # Max tokens in the generated response
    n_ctx=4096,       # Context window size (should be >= max_tokens + prompt length)
    n_batch=512,      # Number of tokens to process in parallel in a batch
    callback_manager=callback_manager,
    verbose=True,     # Enable verbose output from LlamaCpp
    f16_kv=True,      # Use half-precision for key/value cache (reduces memory)
    # n_gpu_layers=0, # Set to > 0 if you have a GPU and llama-cpp-python was built with GPU support
    # For CPU-only, keep n_gpu_layers at 0 or omit it.
    # n_threads=-1,   # Use all available CPU threads (or specify a number)
    # repeat_penalty=1.1, # Adjust for repetition
)
print("LlamaCpp model loaded.")


# --- Define System Message Content for Tool Calling (Crucial) ---
# This message instructs the LLM on its role and how to use tools.
# SYSTEM_MESSAGE_CONTENT = """
# You are a helpful and knowledgeable financial AI assistant called FinPal.
# Your primary goal is to provide accurate financial information and insights based on the tools available to you.
# You can answer questions about stock prices and company news.
# When a user asks for information that can be obtained using your tools, you MUST use the appropriate tool.
# Present the information clearly and concisely.
# If a question cannot be answered by your tools, state that you cannot fulfill the request and offer to assist with something else.
# """

# --- Define System Message Content for ReAct Agent with JSON hint ---
SYSTEM_MESSAGE_CONTENT = """
You are FinPal, a helpful and knowledgeable financial AI assistant.
Your goal is to provide accurate financial information and insights.
You have access to the following tools:

{tools}

To use a tool, you must use the following format:

Thought: you should always think about what to do
Action: tool_name
Action Input: ```json
{{
  "arg1": "value1",
  "arg2": "value2"
}}
Observation: the result of the tool execution
Thought: Based on the observation, I will now... (continue with next thought or provide final answer)
... (this Thought/Action/Action Input/Observation sequence can repeat multiple times as needed) ...
Thought: I have finished my task and now know the final answer
Final Answer: [your answer here]

You must always output your thought process.
If the user asks for information that cannot be directly answered by your tools,
provide a helpful and informative response based on your general financial knowledge.
If the conversation requires a tool, use it. If not, respond conversationally.
"""

# # Create the prompt template
# prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(content=SYSTEM_MESSAGE_CONTENT),
#         ("human", "{input}"),
#         ("placeholder", "{agent_scratchpad}"), # Essential for agent's internal thought process and tool use
#     ]
# )
# Pull a standard ReAct agent prompt from the LangChain Hub
# This prompt is designed to work with create_react_agent
# It will have placeholders for tools, tool_names, and agent_scratchpad
#prompt = hub.pull("hwchase17/react")

tools_string = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
formatted_system_message_content = SYSTEM_MESSAGE_CONTENT.format(tools=tools_string)

# base_prompt_messages = prompt.messages
# final_prompt_messages = [
# SystemMessage(content=formatted_system_message)
# ] + base_prompt_messages[1:] # Keep Human and AgentScratchpad placeholders

# custom_react_prompt = ChatPromptTemplate.from_messages(final_prompt_messages)

prompt = ChatPromptTemplate.from_messages(
[
SystemMessage(content=SYSTEM_MESSAGE_CONTENT), # Use SystemMessage here
("human", "{input}"),
MessagesPlaceholder("agent_scratchpad"),
]
)

prompt = prompt.partial(
tools="\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
tool_names=", ".join([tool.name for tool in tools]),
)
# Create the agent
#agent = create_tool_calling_agent(llm, tools, prompt)
agent = create_react_agent(llm, tools, prompt)

# Create the AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- Main interaction loop ---
def chat_with_finPal():
    print("Welcome to FinPal, your personal financial advisor!")
    print("Type 'quit' or 'exit' to end the chat.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            print("FinPal: Goodbye!")
            break

        try:
            # Invoke the agent with the user's input
            print("\nFinPal (thinking...):")
            response = agent_executor.invoke({"input": user_input, "agent_scratchpad": []})
            #response = agent_executor.invoke({"input": user_input})
            print(f"\nFinPal: {response['output']}")
        except Exception as e:
            print(f"FinPal: An error occurred: {e}")
            print("Please try your query again or rephrase it.")

if __name__ == "__main__":
    chat_with_finPal()