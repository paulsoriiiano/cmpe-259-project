"""
Loads different LLMs for the project.
"""

from langchain import HuggingFacePipeline
from transformers import pipeline

def load_model(size="small"):
    if size == "small":
        model_name = "mistralai/Mistral-7B-v0.1"
    elif size == "large":
        model_name = "meta-llama/Llama-2-13b-chat-hf"
    else:
        print("I am not aware of this model.")
        return
    
    pipe = pipeline("text-generation", model=model_name, max_new_tokens=512)
    return HuggingFacePipeline(pipeline=pipe)