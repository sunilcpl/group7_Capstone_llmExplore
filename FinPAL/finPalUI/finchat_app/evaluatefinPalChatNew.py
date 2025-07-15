import csv
from finPalChatNew import FinPalAgent, llm, tools, SYSTEM_MESSAGE_CONTENT # Import the agent class and its dependencies

# --- 1. Define Test Queries ---
test_queries = [
    "I want to invest ₹5000 monthly in SIP for 15 years with 12% expected returns. What will be my corpus?",
    "What's the difference between a mutual fund and an ETF?",
    "Convert $100 to INR. Then, if I invest that amount monthly for 5 years with 8% expected returns, what will be my corpus?", # Complex query combining tools
    "What is inflation and why is it important for my investments?", # Another general knowledge query
    "How much will $1000 grow to in 10 years at an annual return of 7%?", # Lump sum growth
    "Calculate the SIP value if I put 2000 rupees every month for 10 years at 10.5% annual interest.",
    "How much should I save from my ₹8K/month student income in Bengaluru for essentials?", # Budgeting advice
    "If I invest 10000 INR per month at 15% for 20 years, what's the final amount?",
    "Should I buy Google stock today?", # Out of scope
    "How can I start building an emergency fund?", # General advice
    "Convert 50 GBP to USD and then tell me how much I'd have if I invested that amount for 3 years at 6% annually.", # Multi-step, multi-tool
    "What are the benefits of diversifying my investment portfolio?",
    "What is compounding?", # General knowledge
    "Can you explain what a bond is?", # General knowledge
    "I have 500 USD, convert it to EUR, then calculate its SIP value if I invest that EUR amount monthly for 7 years with 9% annual return.", # More complex multi-tool
    "What is the SIP amount if I want to reach 1,00,000 in 5 years with 10% annual return?", # Inverse SIP (agent might not know this)
]

# --- 2. Instantiate the FinPalAgent ---
# We use the 'llm', 'tools', and 'SYSTEM_MESSAGE_CONTENT' imported from finPal_agent.py
# The agent will create its own chat_history for interactive use, but run_for_testing creates a new one.
finPal_agent = FinPalAgent(llm=llm, tools=tools, system_message_content=SYSTEM_MESSAGE_CONTENT)
print("FinPalAgent instance created for evaluation.")

# --- 3. Define Output CSV File ---
output_csv_file = 'test_results.csv'

print(f"\n--- Starting FinPal Advisor Evaluation and writing results to {output_csv_file} ---")

# --- 4. Run Tests and Write Results to CSV ---
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(['Query ID', 'User Query', 'FinPal Advisor Response'])

    for i, user_input in enumerate(test_queries):
        query_id = i + 1
        print(f"\n--- Running Test Query {query_id}: {user_input} ---")
        
        # Invoke the agent's run_for_testing method
        # Set verbose=True here if you want to see the internal steps during evaluation
        response = finPal_agent.run_for_testing(user_input, verbose=False) 
        
        print(f"--- FinPal Advisor's Final Response for Query {query_id}: ---")
        print(response)

        # Write the results to CSV
        csv_writer.writerow([query_id, user_input, response])

print(f"\n--- All Evaluation Complete. Results saved to {output_csv_file} ---")