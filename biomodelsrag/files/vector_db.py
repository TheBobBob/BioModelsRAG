import os
from pathlib import Path
from os import PathLike

import ollama
import chromadb
from chromadb.utils import embedding_functions


COLLECTION_NAME = "BioModelsRAG"
CHROMA_DIR = "chroma"


def get_chroma_path(database_path: PathLike) -> Path:
    """Return the path used by Chroma inside a BioModel database."""

    return Path(database_path) / CHROMA_DIR


def create_vector_db(
    final_items: list[str],
    output_path: PathLike,
) -> chromadb.Collection:
    """
    Create a persistent vector database for Antimony segments.

    The database is stored under:

        output_path/
            chroma/

    Args:
        final_items: Antimony text segments.
        output_path: Root directory for the BioModel database.

    Returns:
        Chroma collection.
    """

    output_path = Path(output_path)
    chroma_path = get_chroma_path(output_path)

    # Create directories if they don't exist
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    chroma_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    client = chromadb.PersistentClient(
        path=str(chroma_path)
    )

    embedding_function = (
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    documents = []

    for item in final_items:

        prompt = f"""
Summarize the following segment of Antimony in a clear
and concise manner.

1. Provide a detailed summary using a limited number of words.
2. Maintain all original values and include mathematical
   expressions or values in full.
3. Ensure that all variable names and their values are
   clearly presented.
4. Write the summary in paragraph format, emphasizing
   clarity and completeness.

Here is the Antimony segment:

{item}
"""

        result = ollama.generate(
            model="llama3",
            prompt=prompt,
        )

        documents.append(
            result["response"]
        )

    if documents:
        collection.add(
            documents=documents,
            ids=[
                f"id{i}"
                for i in range(len(documents))
            ],
        )

    return collection


def load_vector_db(
    database_path: PathLike,
) -> chromadb.Collection:
    """
    Load an existing BioModel vector database.
    """

    chroma_path = get_chroma_path(database_path)

    if not chroma_path.exists():
        raise FileNotFoundError(
            f"Vector database not found: {chroma_path}"
        )

    client = chromadb.PersistentClient(
        path=str(chroma_path)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection