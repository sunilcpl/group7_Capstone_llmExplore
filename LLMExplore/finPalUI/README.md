# FinPal - Financial Advisory Chatbot

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
