import os
import requests
import tellurium as te
import tempfile
import ollama
from langchain_text_splitters import CharacterTextSplitter
import time

# Constants and global variables
GITHUB_OWNER = "TheBobBob"
GITHUB_REPO_CACHE = "BiomodelsCache"
BIOMODELS_JSON_DB_PATH = "src/cached_biomodels.json"
LOCAL_DOWNLOAD_DIR = tempfile.mkdtemp()  
cached_data = None
conversation_history = []  # Store previous conversation history
persistent_db = None  # Keep the database persistent

class BioModelCacheRetrieval:
    def __init__(self, search_str, github_owner="TheBobBob", github_repo_cache="BiomodelsCache"):
        self.search_str = search_str
        self.github_owner = github_owner
        self.github_repo_cache = github_repo_cache
    
    def search_models(self):
        """Searches the cache for specific BioModels with keywords.

        Returns:
            dict: A dictionary of models matching the search query.
        """
        
        BIOMODELS_JSON_DB_PATH = "src/cached_biomodels.json"
        cached_data = None
        
        url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo_cache}/contents/{BIOMODELS_JSON_DB_PATH}"
        headers = {"Accept": "application/vnd.github+json"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "download_url" in data:
                file_url = data["download_url"]
                json_response = requests.get(file_url)
                cached_data = json_response.json()
        else:
            print(f"Failed to retrieve data from GitHub. Status code: {response.status_code}")
            return {}

        query_text = self.search_str.strip().lower()
        models = {}

        if cached_data:
            for model_id, model_data in cached_data.items():
                if 'name' in model_data:
                    name = model_data['name'].lower()
                    url = model_data['url']
                    id = model_data['model_id']
                    title = model_data['title']
                    authors = model_data['authors']
                    model_info = ' '.join([str(v).lower() for v in model_data.values()])

                    if query_text in model_info and model_id not in models:
                        models[model_id] = {
                            'ID': model_id,
                            'name': name,
                            'url': url,
                            'id': id,
                            'title': title,
                            'authors': authors,
                        }
        return models

    @staticmethod
    def download_model_files(model_url, model_id):
        LOCAL_DOWNLOAD_DIR = tempfile.mkdtemp()
        """Downloads the file in SBML format given the model URL.

        Args:
            model_url (str): The url used for download
            model_id (str): The model ID used to complete the download URL.

        Returns:
            str: The file path of the downloaded model if successful, or None if the download had failed.
        """
        model_url = f"https://raw.githubusercontent.com/TheBobBob/BiomodelsStore/main/biomodels/{model_id}/{model_id}_url.xml"
        try:
            response = requests.get(model_url)
            if response.status_code == 200:
                os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)
                file_path = os.path.join(LOCAL_DOWNLOAD_DIR, f"{model_id}.xml")
                
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                
                print(f"Model {model_id} downloaded successfully: {file_path}")
                return file_path
            else:
                print(f"Failed to download the model from {model_url}. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error downloading model {model_id} from {model_url}: {e}")
            return None

def convert_sbml_to_antimony(sbml_file_path, antimony_file_path):
    """Convert the SBML model to Antimony format and save to a file."""
    try:
        r = te.loadSBMLModel(sbml_file_path)
        antimony_str = r.getCurrentAntimony()
        
        with open(antimony_file_path, 'w') as file:
            file.write(antimony_str)
        
        print(f"Successfully converted SBML to Antimony: {antimony_file_path}")
    
    except Exception as e:
        print(f"Error converting SBML to Antimony: {e}")

def split_biomodels(antimony_file_path):
    text_splitter = CharacterTextSplitter(
        separator="  // ",
        chunk_size=100000000000000000000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )
    
    final_items = []
    directory_path = os.path.dirname(os.path.abspath(antimony_file_path))
    if not os.path.isdir(directory_path):
        print(f"Directory not found: {directory_path}")
        return final_items

    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
                # Use text_splitter to split content into documents
                items = text_splitter.create_documents([file_content])
                for item in items:
                    # Directly append item assuming it is a string
                    final_items.append(item)
                # Stop after processing the first biomodel
                break
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return final_items

def create_vector_db(final_items):
    global persistent_db  # Use the persistent database
    if persistent_db:
        print("Database already initialized.")
        return persistent_db
    
    from chromadb.utils import embedding_functions
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection_name = 'BioModelsRAG'
    import chromadb
    client = chromadb.Client()
    db = client.get_or_create_collection(name=collection_name, embedding_function=embedding_function)

    
    documents_to_add = []
    ids_to_add = []
    
    for item in final_items:
        item2 = str(item)
        item_id = f"id_{item2[:45].replace(' ', '_')}"
    
        existing_documents = db.get(ids=[item_id])
    
        if not existing_documents:  # If the ID does not exist
            # Generate the LLM prompt and output
            prompt = f"""
            Summarize the following segment of Antimony in a clear and concise manner:
            1. Provide a detailed summary using a limited number of words
            2. Maintain all original values and include any mathematical expressions or values in full.
            3. Ensure that all variable names and their values are clearly presented.
            4. Write the summary in paragraph format, putting an emphasis on clarity and completeness.
        
            Here is the antimony segment to summarize: {item}
            """
    
            output = ollama.generate(
                model = 'llama3', prompt = prompt
            )
    
            # Extract the generated summary text
            final_result = output['documents']
    
            # Add the result to documents and its corresponding ID to the lists
            documents_to_add.append(final_result)
            ids_to_add.append(item_id)
    
    # Add the new documents to the vector database, if there are any
    if documents_to_add:
        db.upsert(
            documents=documents_to_add,
            ids=ids_to_add
        )
    
    return db

def generate_response(db, query_text):
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
    
    
    # Create the prompt for the ollama model with conversation history
    prompt_template = f"""
    
    Use the following context to answer the following question:
    {best_recommendation}
    
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

def main():
    global persistent_db
    search_str = input("Enter search query: ")
    biomodelscacheretrieval = BioModelCacheRetrieval(search_str)
    models = biomodelscacheretrieval.search_models()
    if models:
        all_final_items = []
        
        for model_id, model_data in models.items():
            print(f"Processing model: {model_data['name']}")
            
            # Download and process each model
            model_url = model_data['url']
            model_file_path = biomodelscacheretrieval.download_model_files(model_url, model_id)
            
            if model_file_path:
                antimony_file_path = model_file_path.replace('.xml', '.txt')
                convert_sbml_to_antimony(model_file_path, antimony_file_path)
                
                final_items = split_biomodels(antimony_file_path)
                all_final_items.extend(final_items)
        
        if all_final_items:
            persistent_db = create_vector_db(all_final_items)
            query_text = input("Enter your question about the model(s): ")
            response = generate_response(persistent_db, query_text)
            print("Final response:", response)
        else:
            print("No models were processed successfully.")
    else:
        print("No models found matching your search query.")

if __name__ == "__main__":
    main()
