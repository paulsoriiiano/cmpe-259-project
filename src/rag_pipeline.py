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

    rag_docs = retriever.get_relevant_documents(query)
    rag_context = "\n\n".join([d.page_content for d in rag_docs])
    rag_sources = "\n\n".join([f"{d.metadata["title"]} information from {d.metadata["url"]}" for d in rag_docs])

    inputs = {
        "context": rag_context,
        "sources": rag_sources,
        "question": RunnablePassthrough()
    }

    return inputs

  # 2. Create prompt
  prompt = ChatPromptTemplate.from_template("""
  You are a helpful virtual assistant for California parks and outdoors. 
  Use the provided context from park data to answer the question.
  If information is missing, respond with the best estimate or say "I'm not sure."
  Always cite your sources, whenever possible.

  Context:
  {context}


  Question:
  {question}

                                        
  Answer:
                                        

  Sources:
  {sources}                                      
  """)

  # 3. Build chahin
  rag_chain = (
    RunnableLambda(retrieve_and_format)
    | prompt
    | llm
    | StrOutputParser()
  )

  return rag_chain