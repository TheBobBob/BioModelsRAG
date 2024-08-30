import ollama
from typing import List
import chromadb

def createDocuments(final_items: List[str], collection: chromadb.Collection) -> List[str]:
    """Generates summaries of the BioModel chunks and adds them to the Chroma database collection

    Args:
        final_items (List[str]): The segmented BioModel database.
        collection (chromadb.Collection): The Chroma database collection.

    Returns:
        List[str]: The documents that are passed to the Chroma database are in string form.
    """
    
    documents = []
    for item in final_items:
        print(item) #option for reporting or not 
        prompt = f"""Please summarize this segment of Antimony: {item}. The summaries must be clear and concise. 
        For Display Names, provide the value for each variable. Expand mathematical functions into words. 
        Cross reference all parts of the provided context. 
        Explain well without errors and in an easily understandable way. Write in a list format."""
        documents5 = ollama.generate(model="llama3", prompt=prompt)
        documents2 = documents5["response"]
        documents.append(documents2) 

    # Add documents to the collection
    collection.add(
        documents=documents,
        ids=[f"id{i}" for i in range(len(documents))]
    )
    
    return documents
    
    

#unit test
#documents = []
#assert(isinstance(documents, list))
#print("ok!")


