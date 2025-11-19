"""
This module provides querying functions.
"""

import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import weather_fn
from weather_fn import get_weather


def build_rag_chain(llm, retriever):
  """ Build a two-step RAG chain. """

  # 1. Retrieve documents
  def retrieve_and_format(query):
    # 1.1. Get documents context
    rag_docs = retriever.invoke(query)
    rag_context = "\n\n".join([d.page_content for d in rag_docs])
    rag_sources = "\n\n".join([f"{d.metadata["title"]} information from {d.metadata["url"]}" for d in rag_docs])

    # 1.2. Check if query requires weather information
    keywords = ["weather", "temperature", "day", "rain", "sunny", "snow"]
    if any(word in query.lower() for word in keywords):

      # 1.3. Get location (if available)
      location = rag_docs[0].metadata.get("title") if rag_docs else None
      if not location:
        rag_context += "\n\n No location found. Could not get weather data."
      
      # 1.4. Get weather information (if available)
      match = re.search(r"(\d+)[ -]?day", query)
      days = int(match.group(1)) if match else 0
      weather_info = get_weather(location, days)
      if not weather_info:
        rag_context += "\n\n No weather information found. Something went wrong with fetching weather data."

      rag_context += f"\n\n Weather information: {weather_info}\n"

    inputs = {
        "context": rag_context,
        "question": query,
        "sources": rag_sources,
    }

    return inputs

  # 2. Create prompt
  prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful California Parks & Trails assistant."
         "Answer concisely and cite the relevant parks information in your answer.",
         ),

        ("human",
         """Use the following context and sources from park data to answer questions.
            If information is missing, respond with the best estimate or say "I'm not sure."
            Format the sources (if available) as footnotes in the end of the answer.

            Context:
            {context}

            Sources:
            {sources}

            Question:
            {question}

            Your answer:

          """
        )
    ])

  # 3. Build chain
  rag_chain = (
    RunnableLambda(retrieve_and_format)
    | prompt
    | llm
    | StrOutputParser()
  )

  return rag_chain