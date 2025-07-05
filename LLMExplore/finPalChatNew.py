import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langchain_mistralai import ChatMistralAI
from typing import List, Dict, Union, Any, Tuple

# --- 0. Pre-Steps ---
load_dotenv()
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY environment variable not set. Please create a .env file with your Mistral API key.")

# --- 1. Define your Custom Tools ---
@tool
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

@tool
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
tool_map = {tool.name: tool for tool in tools} # Create a map for easy lookup
# print(f"Tools defined: {[t.name for t in tools]}") # Commented out for cleaner general use

# --- 2. Initialize the Mistral LLM via API ---
llm = ChatMistralAI(model="mistral-small-latest", temperature=0).bind_tools(tools)
# print("LLM initialized with tools bound directly.") # Commented out for cleaner general use

# Define the system message for the agent (global constant for easy import)
SYSTEM_MESSAGE_CONTENT = (
    "You are a helpful financial assistant named FinPal Advisor. Your main task is to assist users with financial calculations using available tools, and answer general financial questions. "
    "When a calculation is requested and you have the necessary information, use the appropriate tool. "
    "If a query requires multiple steps (e.g., currency conversion then investment calculation), process them sequentially using the correct tools. "
    "If you need more information to perform a calculation, ask clarifying questions. "
    "If the query is a general financial question, answer it directly. "
    "Always provide a clear, concise, and helpful final answer to the user's original question."
)

# --- 3. Custom FinPal Agent Class ---
class FinPalAgent:
    def __init__(self, llm: ChatMistralAI, tools: List[Any], system_message_content: str):
        self.llm = llm
        self.tool_map = {tool.name: tool for tool in tools}
        self.system_message_content = system_message_content
        # Initialize conversation history with the system message (for interactive chat)
        self.chat_history: List[BaseMessage] = [SystemMessage(content=self.system_message_content)]
        # print("FinPalAgent initialized. Ready for chat.") # Commented out for cleaner general use

    def _run_single_step(self, current_messages: List[BaseMessage], verbose: bool) -> Tuple[str, bool]: # Removed max_steps from signature here
        """
        Executes a single turn of the agent's thought process.
        Returns (response_content, is_final_answer).
        """
        llm_response = self.llm.invoke(current_messages)

        if verbose:
            print(f"\n--- LLM's Raw Response: ---")
            print(llm_response)

        if llm_response.tool_calls:
            if verbose:
                print("\n--- LLM requested tool call(s)! Executing tool(s)... ---")
            
            current_messages.append(llm_response) 

            for tool_call_dict in llm_response.tool_calls:
                tool_name = tool_call_dict['name']
                tool_args = tool_call_dict['args']
                tool_call_id = tool_call_dict['id']
                
                if tool_name in self.tool_map:
                    try:
                        tool_output = self.tool_map[tool_name].invoke(tool_args)
                        if verbose:
                            print(f"Tool '{tool_name}' executed. Output: {tool_output}")
                        current_messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call_id))
                    except Exception as e:
                        error_msg = f"Error executing tool '{tool_name}' with args {tool_args}: {e}"
                        if verbose:
                            print(f"ERROR: {error_msg}")
                        current_messages.append(ToolMessage(content=f"ERROR: {error_msg}", tool_call_id=tool_call_id))
                        return f"An error occurred while using a tool: {e}", True # Treat tool error as final
                else:
                    error_msg = f"LLM requested unknown tool: {tool_name}"
                    if verbose:
                        print(f"ERROR: {error_msg}")
                    current_messages.append(AIMessage(content=f"ERROR: {error_msg}"))
                    return error_msg, True # Treat unknown tool as final

            if llm_response.content:
                if verbose:
                    print("\n--- LLM returned content along with tool calls. This might be a final answer. ---")
                return llm_response.content, True
            
            return "", False

        elif llm_response.content:
            if verbose:
                print("\n--- LLM provided direct answer (no tool call). ---")
            current_messages.append(llm_response)
            return llm_response.content, True

        else:
            if verbose:
                print("\n--- LLM response was empty or unhandled. Breaking loop. ---")
            return "The LLM did not provide a clear response.", True

    def chat(self, user_query: str, max_steps_per_turn: int = 5, verbose: bool = False) -> str: # Default verbose to False for general chat
        """
        Processes a single user query in a multi-turn chat.
        Maintains continuous chat_history.
        """
        if verbose:
            print(f"\n--- User: {user_query} ---")

        self.chat_history.append(HumanMessage(content=user_query))
        
        response_content = "An internal error occurred."
        final_answer_received = False

        for step in range(max_steps_per_turn):
            if verbose:
                print(f"\n--- Agent Internal Step {step + 1} ---")
                print(f"Current full chat history ({len(self.chat_history)} messages):")
                for msg in self.chat_history[-min(len(self.chat_history), 8):]:
                    print(f"  {type(msg).__name__}: {msg.content[:100]}..." + 
                          (f" (Tool Calls: {msg.tool_calls})" if hasattr(msg, 'tool_calls') and msg.tool_calls else ""))

            try:
                response_content, final_answer_received = self._run_single_step(
                    self.chat_history, verbose
                )
                
                if final_answer_received:
                    break

            except Exception as e:
                if verbose:
                    print(f"\nAn unexpected error occurred in FinPalAgent.chat: {e}")
                response_content = f"An unexpected internal error occurred: {e}"
                final_answer_received = True
                break

        if not final_answer_received:
            response_content = f"Agent reached maximum internal steps ({max_steps_per_turn}) for this turn without a final answer. Please rephrase or try again."
            if not isinstance(self.chat_history[-1], AIMessage):
                 self.chat_history.append(AIMessage(content=response_content))
        elif final_answer_received and not isinstance(self.chat_history[-1], AIMessage):
            self.chat_history.append(AIMessage(content=response_content))

        if verbose:
            print(f"\n--- FinPal Agent Final Response for this turn: ---")
            print(response_content)
        
        return response_content

    def run_for_testing(self, user_query: str, max_steps: int = 5, verbose: bool = False) -> str:
        """
        Runs the agent for a single query, resetting its internal history for each call.
        This is suitable for batch testing where each query is independent.

        Args:
            user_query (str): The user's input query.
            max_steps (int): Maximum internal agent steps for THIS user query.
            verbose (bool): If True, prints detailed debugging information during execution.

        Returns:
            str: The final response from the agent.
        """
        if verbose:
            print(f"\n--- Starting FinPalAgent.run_for_testing for Query: {user_query} ---")

        # Create a fresh, temporary conversation history for this query
        temp_query_history: List[BaseMessage] = [SystemMessage(content=self.system_message_content)]
        temp_query_history.append(HumanMessage(content=user_query))
        
        final_response_content = "The agent could not generate a clear response for this test query."
        final_answer_received = False

        for step in range(max_steps):
            if verbose:
                print(f"\n--- Test Run Internal Step {step + 1} ---")
                print(f"Current temp query history ({len(temp_query_history)} messages):")
                for msg in temp_query_history[-min(len(temp_query_history), 8):]:
                    print(f"  {type(msg).__name__}: {msg.content[:100]}..." + 
                          (f" (Tool Calls: {msg.tool_calls})" if hasattr(msg, 'tool_calls') and msg.tool_calls else ""))

            try:
                response_content, final_answer_received = self._run_single_step(
                    temp_query_history, verbose
                )
                
                if final_answer_received:
                    final_response_content = response_content
                    break

            except Exception as e:
                if verbose:
                    print(f"\nAn unexpected error occurred in FinPalAgent.run_for_testing: {e}")
                final_response_content = f"An unexpected internal error occurred during testing: {e}"
                final_answer_received = True
                break

        if not final_answer_received:
            final_response_content = (f"Agent reached maximum steps ({max_steps}) without a final answer "
                                      f"for test query: '{user_query[:50]}...'. "
                                      f"Last message in history: {temp_query_history[-1].content[:100]}...")
        
        if verbose:
            print(f"\n--- FinPalAgent.run_for_testing finished for query: {user_query} ---")
        
        return final_response_content


if __name__ == "__main__":
    # This block ensures that when finPal_agent.py is run as the main script,
    # it defaults to the interactive chat experience.
    print("\n--- Welcome to FinPal, your personal financial advisor! ---")
    print("Type 'quit' or 'exit' to end the chat.")

    # Create an agent instance specific to this execution
    interactive_agent = FinPalAgent(llm=llm, tools=tools, system_message_content=SYSTEM_MESSAGE_CONTENT)

    while True:
        user_input = input("\nMe: ")
        if user_input.lower() in ['quit', 'exit']:
            print("FinPal Advisor: Goodbye!")
            break
        
        agent_response = interactive_agent.chat(user_input, verbose=False) # Use chat for interactive mode
        print(f"FinPal Advisor: {agent_response}")