# download_model.py

from huggingface_hub import hf_hub_download
import os

# --- Using the alternative financial model: us4/fin-llama3.1-8b ---
model_name = "us4/fin-llama3.1-8b"
model_file = "model-q4_k_m.gguf" # Confirmed to exist on the model page for Q4_K_M

model_path = None # Initialize model_path to None

try:
    print(f"Attempting to download model: {model_name} with file: {model_file}")
    model_path = hf_hub_download(repo_id=model_name, filename=model_file)
    print(f"Model downloaded successfully to: {model_path}")

    # Only write to file if download was successful
    if model_path: # Check if model_path was successfully assigned
        with open("downloaded_model_path.txt", "w") as f:
            f.write(model_path)
        print("Model path also saved to downloaded_model_path.txt")

except Exception as e:
    print(f"Error downloading model: {e}")
    print("Please double-check the model name and filename on Hugging Face Hub.")
    print(f"Attempted URL: https://huggingface.co/{model_name}/resolve/main/{model_file}")