import ollama
from typing import List, Optional, Dict

N_RESULTS = 20 #10 sections was derived based on the segments of the BioModel. Based on tests conducted, 10 sections provided the most optimal output.
def generateResponse(query_text: str, collection: Optional[Dict] = None) -> str:
    """Generates a response to a query based on the Chroma database collection.

    Args:
        query_text (str): The query to search for.
        collection (Optional[Dict]): The Chroma collection object to use for querying.

    Returns:
        str: The response generated from the query.
    """
    if collection is None:
        raise ValueError("Collection is not provided")

    # Query the embedding database for similar documents
    query_results = collection.query(
        query_texts=query_text,
        n_results=N_RESULTS,
    )

    # Extract the best recommendations from the query results
    best_recommendation = query_results.get('documents', [])

    # Create the prompt for the ollama model
    prompt_template = f"""Use the following pieces of context to answer the question at the end. If you don't know the answer, say so.

    This is the piece of context necessary: {best_recommendation}

    Cross-reference all pieces of context to define variables and other unknown entities. Calculate mathematical values based on provided matching variables. Remember previous responses if asked a follow-up question.

    Question: {query_text}

    """
    response = ollama.generate(model="llama3", prompt=prompt_template)
    final_response = response.get('response', 'No response generated')
    return final_response

#from createVectorDB import collection
#query = "What protein interacts with ach2?"
#result = generateResponse(query_text=query, collection=collection)
#print("Response:", result)