import ollama
persistent_db = None  # Keep the database persistent
import chromadb

def create_vector_db(final_items: list[str]) -> chromadb.Collection:
    """
    Creates or retrieves a persistent vector database for storing summaries of Antimony segments.

    Args:
        final_items (list[str]): A list of Antimony format text segments to be summarized and stored in the database.

    Returns:
        chromadb.Collection: The vector database collection containing the summarized documents.
    """
    global persistent_db  # Use the persistent database
    if persistent_db:
        print("Database already initialized.")
        return persistent_db
    
    import chromadb
    client = chromadb.Client()
    from chromadb.utils import embedding_functions
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection_name = "BioModelsRAG"
    db = client.get_or_create_collection(name=collection_name, embedding_function = embedding_function)

    documents = []
    
    for item in final_items:
        prompt = f"""
        Summarize the following segment of Antimony in a clear and concise manner:
        1. Provide a detailed summary using a limited number of words
        2. Maintain all original values and include any mathematical expressions or values in full. 
        3. Ensure that all variable names and their values are clearly presented. 
        4. Write the summary in paragraph format, putting an emphasis on clarity and completeness. 
        
        Here is the antimony segment to summarize: {item}
        """
        documents5 = ollama.generate(model="llama3", prompt=prompt)
        documents2 = documents5['response']
        documents.append(documents2)
    
    if final_items:
        db.add(
            documents=documents,  # Ensure these are strings
            ids=[f"id{i}" for i in range(len(final_items))]
        )
    
    persistent_db = db
    return db