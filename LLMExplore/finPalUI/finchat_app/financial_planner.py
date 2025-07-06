# app/financial_planner.py
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai  # Import OpenAI package for the API
import os

# Retrieve OpenAI API key from environment variable

openai_api_key = ""

#os.getenv("OPENAI_API_KEY")  # Ensure the key is retrieved securely

# Initialize OpenAI API
openai.api_key = openai_api_key  # Set OpenAI API key for the openai package

# Initialize LangChain with OpenAI
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Define a prompt template
template = "You are a financial advisor. The user is asking for financial planning advice: {question}"
prompt = PromptTemplate(input_variables=["question"], template=template)

# Create the LangChain LLM chain (deprecated, but still functional)
chain = LLMChain(llm=llm, prompt=prompt)

def get_financial_advice_from_openai(question: str):
    """Use OpenAI GPT to generate financial advice based on the user's question."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful financial advisor."},
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.7
    )

    print("OpenAI response:")
    print(response)
    print("OpenAI response text:")

    return response.choices[0].message.content.strip()

def generate_financial_plan(question: str):
    """Generate financial advice from LangChain and OpenAI GPT."""
    print(f"Generating financial plan for question: {question}")
    # Generate advice using LangChain (using LLMChain temporarily)
    langchain_advice = chain.run(question)  # LLMChain generated advice

    print(f"LangChain advice: {langchain_advice}")
    # Generate advice using OpenAI GPT directly
    #openai_advice = get_financial_advice_from_openai(question)  # OpenAI GPT advice

   # print(f"OpenAI advice: {openai_advice}")
    return langchain_advice
