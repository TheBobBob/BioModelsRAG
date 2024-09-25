from biomodelcache import BioModelCacheRetrieval
from convert_sbml_to_antimony import convert_sbml_to_antimony
from split_biomodels import split_biomodels
from create_vector_db import create_vector_db
from generate_response import generate_response
import os
import tempfile

LOCAL_DOWNLOAD_DIR = tempfile.mkdtemp()  

def main():
    retriever = BioModelCacheRetrieval(search_str)
    models = retriever.search_models()
    
    if models:
        all_final_items = []
        
        for model_id, model_data in models.items():
            print(f"Processing model: {model_data['name']}")
            
            model_url = model_data['url']
            model_file_path = retriever.download_model_files(model_url, model_id)
            
            if model_file_path:
                antimony_file_path = os.path.join(LOCAL_DOWNLOAD_DIR, f"{model_id}.txt")
                convert_sbml_to_antimony(model_file_path, antimony_file_path)
                
                final_items = split_biomodels(antimony_file_path)
                all_final_items.extend(final_items)
        
        if all_final_items:
            db = create_vector_db(all_final_items)
            
            query_text = input("Enter your question about the model(s): ")
            response = generate_response(db, query_text)
            print(f"Response: {response}")
        else:
            return ValueError("No models were processed successfully.")
    else:
        return ValueError("No models found matching your search query.")

if __name__ == "__main__":
    search_str = input("Enter search query: ")
    main(search_str)