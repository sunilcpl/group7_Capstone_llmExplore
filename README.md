# Frontend Module FinPalUI

## Project Overview

FinPal is an AI-powered financial advisory chatbot built using Mistral AI and LangChain. FinPalUI is the frontend module that provides a modern and interactive interface for users to interact with the financial advisory system.

## Key Components

### 1. Interactive Chat Interface
- Modern Chainlit-based chat interface
- Real-time financial advice and calculations
- Systematic Investment Plan (SIP) calculator
- Currency converter

### 2. Technical Stack
- Python for backend services
- Chainlit for frontend interface
- TOML for configuration management
- FastAPI (via Chainlit)
- WebSocket for real-time communication

## Chainlit Lifecycle Hooks

Chainlit provides several lifecycle hooks that allow you to customize the application behavior at different stages. This project currently implements the following hooks:

### Implemented Hooks

#### 1. On Start
✅ Implemented
```python
@cl.on_start
async def initialize():
    # Initialize FinPalAgent
    agent_instance = FinPalAgent(
        llm=llm,
        tools=tools,
        system_message_content=SYSTEM_MESSAGE_CONTENT
    )
    cl.user_session.set("agent", agent_instance)
    
    # Send welcome message
    await cl.Message(
        content="Hello! I'm FinPal, your personal financial advisor. How can I help you today?"
    ).send()

 #### 2. On Message
✅ Implemented
```python
@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and process queries"""
    # Retrieve agent from session
    agent_instance = cl.user_session.get("agent")
    
    if agent_instance is None:
        await cl.Message(content="FinPal Advisor is not initialized. Please refresh the page.").send()
        return
    
    try:
        # Process user query with Chainlit step
        async with cl.Step(name="FinPal Agent Processing", type="agent") as step:
            response_content = await cl.make_async(agent_instance.chat)(
                user_query=message.content,
                verbose=True
            )
            step.output = response_content
```    

On Settings
❌ Not Implemented

# Not currently implemented
# @cl.on_settings
# async def settings_changed(settings: dict):
#     pass

On Stop
❌ Not Implemented
# Not currently implemented
# @cl.on_stop
# async def stop():
#     pass
## Implementation Notes
1. Session Management
- Uses cl.user_session to store the FinPalAgent instance
- Maintains agent state across messages
- Includes error handling for uninitialized agent

2. Message Processing
- Implements Chainlit's step system for better UI feedback
- Uses cl.make_async for synchronous agent calls
- Includes verbose mode for detailed processing steps

3. State Management
- Stores agent instance in user session
- Maintains conversation context
- Handles initialization errors gracefully

4. Custom Logo
- Loads a custom logo from the `public` directory
- Uses Chainlit's built-in support for static assets
- Logo is displayed in the chat interface header
- Maintains consistent branding across the application

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Mistral API key (for using Mistral AI model)

### Installation

1. Navigate to the finPalUI directory
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
### Development

#### Project Structure
finPalUI/
├── finchat_app/
│   ├── .chainlit/      # Chainlit configuration
│   ├── .files/         # Static files
│   ├── __pycache__/    # Python cache
│   ├── public/         # Public assets (including logo)
│   ├── chainlit.md     # Chainlit documentation
│   ├── config.toml     # Application configuration
│   ├── financial_planner.py  # Financial analysis module
│   ├── finchat_app.py  # Main application file
│   └── main.py         # Main entry point
└── requirements.txt    # Project dependencies

- Mistral API key (for using Mistral AI model)

### Installation
1. Navigate to the finPalUI directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Development
To start the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --reload-dir .
```

The application will be available through Chainlit interface

# Backend Module  FinPal - Financial Advisory Chatbot 

FinPal is an AI-powered financial advisory chatbot built using Mistral AI and LangChain. It provides personalized financial advice and calculations for users.

## Key Components

### 1. Interactive Chatbot (`finPalChatNew.py`)

The main chatbot implementation that provides financial advice and calculations. It includes:
- Systematic Investment Plan (SIP) calculator
- Currency converter
- Interactive chat interface

### 2. Evaluation Script (`evaluatefinPalChatNew.py`)

A script that tests the chatbot's performance with various financial queries. It includes test cases for:
- SIP calculations
- Currency conversions
- General financial knowledge
- Multi-step calculations

### 3. Prerequisites

- Python 3.8 or higher
- Mistral API key (for using Mistral AI model)
- Git (for cloning the repository)

### 4. Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/finpal.git
   cd finpal
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Mistral API key:
     ```
     MISTRAL_API_KEY=your_api_key_here
     ```

4. Run the chatbot:
   ```bash
   python finPalChatNew.py
   ```

## WIP Modules

### LlamaCpp Implementation

We are currently working on an alternative implementation using LlamaCpp:

- `finPalLLamaChat.py`: Alternative implementation using local LlamaCpp models
- `evaluatefinPalLlamaChat.py`: Evaluation script for the LlamaCpp implementation

This implementation is still in progress and currently not recommended for use. It will provide a local-only solution without cloud dependencies once complete.

### Setup Instructions for LlamaCpp Modules

1. **Prerequisites**:
   - Python 3.8 or higher
   - CUDA-compatible GPU (recommended for better performance)
   - LlamaCpp model files (GGUF format)

2. **Model Setup**:
   - Download a GGUF model file from the Hugging Face model hub or other sources
   - Place the model file in a dedicated directory (e.g., `models/`)
   - Update the `GGUF_MODEL_PATH` in `finPalLLamaChat.py` with your model path:
   ```python
   GGUF_MODEL_PATH = "/path/to/your/model.gguf"
   ```

3. **Optional Configuration**:
   - You can configure model parameters in `finPalLLamaChat.py`:
     - Temperature (default: 0.7)
     - Top_p (default: 0.95)
     - Top_k (default: 40)
     - Number of threads (default: 4)

4. **Running the WIP Implementation**:
   ```bash
   python finPalLLamaChat.py
   ```

   Note: This implementation is still under development and may have:
   - Performance issues
   - Limited functionality compared to the Mistral AI version
   - Potential stability problems

## Setup Requirements
{{ ... }}

## Usage
{{ ... }}

## Features
{{ ... }}

## Project Structure
{{ ... }}

## Contributing
{{ ... }}

## License
{{ ... }}

## Acknowledgments
{{ ... }}

