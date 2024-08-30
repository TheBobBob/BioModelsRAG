import chromadb
from chromadb.utils import embedding_functions
from typing import Optional, Dict

def createVectorDB(
    collection_name: Optional[str],
    chroma_data_path: Optional[str] = None,
    embed_model: Optional[str] = "all-MiniLM-L6-v2",
    metadata: Optional[Dict[str, str]] = None
) -> chromadb.Collection:
    """Creates the vector database to store embeddings.

    Args:
        collection_name (str): The name of the collection.
        chroma_data_path (Optional[str]): Path for chroma embeddings.
        embed_model (Optional[str]): Model name for embeddings.
        metadata (Optional[Dict[str, str]]): Metadata for the collection.

    Returns:
        chromadb.Collection: The created collection object.
    """
    if chroma_data_path is None:
        chroma_data_path = r"CHROMA_EMBEDDINGS_PATH"  # Default path if not provided

    client = chromadb.PersistentClient(path=chroma_data_path)

    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=embed_model
    )

    # Use provided metadata or default to empty dictionary
    if metadata is None:
        metadata = {"hnsw:space": "cosine"}

    collection = client.create_collection(
        collection_name=collection_name,
        embedding_function=embedding_func,
        metadata=metadata,
    )
    
    return collection

#unsure how to create unittest

#collection = createVectorDB(
    #COLLECTION_NAME="123456789",
    #C#HROMA_DATA_PATH=r"C:\Users\navan\Downloads\BioModelsRAG\CHROMA_EMBEDDINGS_PATH",
    #EMBED_MODEL="all-MiniLM-L6-v2",
    #metadata={"hnsw:space": "cosine"}
