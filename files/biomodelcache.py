import requests
import os
import tempfile

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
