import os
import chromadb
from dotenv import load_dotenv
from models.models import create_embeddings

# Load environment variables once when the module is imported
load_dotenv()

def retrieve_documents(query, model, k=5):
    """
    Retrieves the top-k most similar documents from the specified Chroma collection based on the query,
    using OpenAI embeddings and a persistent Chroma client.
    
    Args:
        query (str): The query string to search for.
        k (int): Number of top similar documents to retrieve.
        collection_name (str, optional): Name of the collection to query. Defaults to "simple_rag" if not provided.
        
    Returns:
        dict: A dictionary containing retrieved documents and their metadata.
    """

    # Use the DB_PATH from environment or default to .chroma
    db_path = os.getenv("DB_PATH") or ".chroma"
    
    collection_name = "simple_rag"

    # Initialize a persistent Chroma client
    try:
        client = chromadb.PersistentClient(path=db_path)
    except TypeError as e:
        raise RuntimeError(f"Error initializing Chroma client: {e}")

    # Access the specified collection or create it if it doesn't exist
    collection = client.get_or_create_collection(name=collection_name)

    query_embedding = create_embeddings([query], model=model)
    query_embedding = [query_embedding[0]]

    # Query the collection for similar documents
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas"]
    )

    print(results)

    return results
