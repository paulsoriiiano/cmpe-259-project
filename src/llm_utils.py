"""
Loads different API-based LLMs for the project.
"""

from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

def load_model(api_token, size="small"):
    if size == "small":
        llm = ChatMistralAI(
          model = "mistral-tiny-2312",
          api_key = api_token,
          temperature = 0.7,
          max_tokens = 256
        )
    elif size == "large":
        llm = ChatOpenAI(
          model = "meta-llama/Llama-3.3-70B-Instruct:groq",
          api_key = api_token,
          base_url = "https://router.huggingface.co/v1",
          temperature = 0.7,
          max_tokens = 256
        )
    else:
        print("I am not aware of this model.")
        return

    return llm