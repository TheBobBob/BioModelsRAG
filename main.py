import os
import tempfile
from fetch_github_json import fetch_github_json
from search_models import search_models
from download_model_file import download_model_file
from convert_sbml_to_antimony import convert_sbml_to_antimony
from split_biomodels import split_biomodels
from create_vector_db import create_vector_db
from generate_response import generate_response

# Set up a temporary directory for model downloads
LOCAL_DOWNLOAD_DIR = tempfile.mkdtemp()  

def main(search_str: str, query_text: str, download_dir: str = LOCAL_DOWNLOAD_DIR) -> str:
    """
    Main function to execute the workflow of searching for models, downloading,
    converting, splitting, and querying the database.

    Args:
        search_str (str): The search query to find relevant models.
        query_text (str): The query text to generate a response from the vector database.
        download_dir (str): Directory to store downloaded files (default is a temporary directory).

    Returns:
        str: The response generated from the vector database based on the query text.
    """
    # Step 1: Fetch models and search for the query
    models = search_models(search_str)
    
    if models:
        all_final_items = []
        
        # Step 2: Process each model returned by the search
        for model_id, model_data in models.items():
            print(f"Processing model: {model_data['name']}")
            
            model_url = model_data['url']
            model_file_path = download_model_file(model_url, model_id)
            
            if model_file_path:
                # Step 3: Convert the downloaded SBML model to Antimony format
                antimony_file_path = os.path.join(download_dir, f"{model_id}.txt")
                convert_sbml_to_antimony(model_file_path, antimony_file_path)
                
                # Step 4: Split the converted Antimony model
                final_items = split_biomodels(antimony_file_path)
                all_final_items.extend(final_items)
        
        # Step 5: Create the vector database from the split biomodel items
        if all_final_items:
            db = create_vector_db(all_final_items)
            
            # Step 6: Query the database and generate a response
            response = generate_response(db, query_text)
            print(f"Response: {response}")
            return response
        else:
            print("No models were processed successfully.")
            return "No models processed successfully."
    else:
        print("No models found matching your search query.")
        return "No models found."

if __name__ == "__main__":
    search_query = input("Enter search query: ")
    question = input("Enter your question about the model(s): ")
    result = main(search_str=search_query, query_text=question)
    print(result)
