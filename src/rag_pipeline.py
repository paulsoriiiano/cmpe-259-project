"""
This module provides querying functions.
"""


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def build_rag_chain(llm, retriever):
  """ Build a two-step RAG chain. """

  # 1. Retrieve documents
  def retrieve_and_format(query):
    rag_docs = retriever.invoke(query)
    rag_context = "\n\n".join([d.page_content for d in rag_docs])
    rag_sources = "\n\n".join([f"{d.metadata["title"]} information from {d.metadata["url"]}" for d in rag_docs])

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
         "Answer concisely and cite the relevant parks in your answer.",
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