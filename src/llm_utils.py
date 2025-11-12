"""
Loads different API-based LLMs for the project.
"""

from langchain_huggingface import HuggingFaceEndpoint

def load_model(api_token, size="small"):
    if size == "small":
        model_name = "mistralai/Mistral-7B-v0.2"
    elif size == "large":
        model_name = "meta-llama/Llama-2-13b-chat-hf"
    else:
        print("I am not aware of this model.")
        return
    
    # Create API-based LLM 
    llm = HuggingFaceEndpoint(
        repo_id = model_name,
        task = "text-generation",
        temperature = 0.7,
        max_new_tokens = 512,
        repetition_penalty = 1.1,
        huggingfacehub_api_token=api_token
    )

    return llm