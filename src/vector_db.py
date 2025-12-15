"""
Creates vector database from park data.
"""


from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_vector_db(data_path="data/ca_state_parks.json", persist_path="faiss_index"):
    """ Creates a FAISS vector database given a JSON file. """

    jq_schema = """
    .[] | {
        text: (
            (.["Park Name"] | tostring) + " — " +
            "Park Hours: " + ((.["Park Hours"] // "") | tostring) + " " +
            "Contact Information: " + ((.["Contact Information"] // "") | tostring) + " " +
            "Dogs Allowed: " + ((.["Are dogs Allowed?"] // "") | tostring) + " " +
            ((.Description // "") | tostring) + " "
        ),
        metadata: {
            title: .["Park Name"],
            url: .URL,
            jurisdiction: .Jurisdiction
        }
    }
    """

    def get_metadata(record, metadata):
      metadata["title"] = record["metadata"]["title"]
      metadata["url"] = record["metadata"]["url"]

      return metadata


    loader = JSONLoader(file_path=data_path, jq_schema=jq_schema, content_key="text", metadata_func=get_metadata)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=30)
    doc_chunks = text_splitter.split_documents(docs)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(doc_chunks, embedding_model)
    db.save_local(persist_path)

    return db


def load_vector_db(persist_path="faiss_index"):
    """ Loads a FAISS vector database from a path. """
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(persist_path, embedding_model, allow_dangerous_deserialization=True)
