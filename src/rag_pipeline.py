"""
This module provides querying functions.
"""

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def two_step_query(query: str, llm, retriever):
  """ Perform a two-step RAG chain. """

  # 1. Retrieve documents
  rag_docs = retriever.get_relevant_documents(query)
  rag_context = "\n\n".join([d.page_content for d in rag_docs])

  # 2. Create prompt
  prompt = PromptTemplate.from_template("""
  You are a helpful virtual assistant for California parks and outdoors. 
  Use the provided context from park data to answer the question.
  If information is missing, respond with the best estimate or say "I'm not sure."

  Context:
  {context}


  Question:
  {question}

  Answer:

  
  """)

  rag_chain = LLMChain(llm=llm, prompt=prompt)
  answer = rag_chain.run({
      "context": rag_context,
      "question": query
  })

  return answer
