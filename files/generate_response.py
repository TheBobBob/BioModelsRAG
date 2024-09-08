import ollama
import time

def generate_response(db, query_text: str) -> str:
    """
    Generates a response to a query using a vector database and a conversational model.

    Args:
        db (chromadb.Collection): The vector database collection used to query relevant documents.
        query_text (str): The text of the query for which a response is to be generated.

    Returns:
        str: The generated response from the conversational model, simulating streaming output.
    """
    global conversation_history
    query_results = db.query(
        query_texts=query_text,
        n_results=5,
    )
    
    # Ensure query results are being processed
    if not query_results.get('documents'):
        print("No results found for the query.")
        return "No results found."
    
    # Extract the best recommendations from the query results
    best_recommendation = query_results['documents']
    
    # Add the previous conversation context to the prompt
    conversation_history.append(f"Q: {query_text}\nA: {best_recommendation}")
    full_conversation = "\n".join(conversation_history)
    
    # Create the prompt for the ollama model with conversation history
    prompt_template = f"""
    You are a conversational agent. Here is the ongoing conversation:
    
    {full_conversation}
    
    Now, using the context provided below, answer the following question:
    {query_text}

    If the information is insufficient to answer the question, please state that clearly.
    """
    
    # Simulate streaming response by breaking the output into parts
    response = ollama.generate(model="llama3", prompt=prompt_template)
    final_response = response.get('response', 'No response generated')

    # Simulate streaming output
    for char in final_response:
        print(char, end='', flush=True)
        time.sleep(0.02)  # Simulate streaming delay
    
    return final_response
