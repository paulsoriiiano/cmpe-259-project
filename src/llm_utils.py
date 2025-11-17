"""
Loads different API-based LLMs for the project.
"""


from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI


def load_model(api_token, size="small"):
    """ Loads a Chat model using specific Chats. """
    
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


def load_chat_model(size="small"):
    """ Loads a Chat model using HuggingFaceEndpoint and ChatHuggingFace. """

    if size == "small":
        llm = HuggingFaceEndpoint(
          repo_id = "mistralai/Mistral-7B-Instruct-v0.2",
          task = "text-generation",
          max_new_tokens = 512,
          temperature = 0.7,
          repetition_penalty = 1.03,
          provider = "auto"
        )
    elif size == "large":
        llm = HuggingFaceEndpoint(
          repo_id = "meta-llama/Llama-3.3-70B-Instruct",
          task = "text-generation",
          max_new_tokens = 512,
          temperature = 0.7,
          repetition_penalty = 1.03,
          provider = "hyperbolic"
        )
    else:
        print("I am not aware of this model.")
        return

    return ChatHuggingFace(llm=llm)