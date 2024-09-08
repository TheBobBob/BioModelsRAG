import os
import requests
import tempfile

# Create a temporary directory for downloading files
LOCAL_DOWNLOAD_DIR = tempfile.mkdtemp()
def download_model_file(model_url:str, model_id:str) -> str:
    """Downloads the file in SBML format given the model URL.

    Args:
        model_url (str): The url used for download
        model_id (str): The model ID used to complete the download URL.

    Returns:
        str: The file path of the downloaded model if successful, or None if the download had failed.
    """
    model_url = f"https://raw.githubusercontent.com/konankisa/BiomodelsStore/main/biomodels/{model_id}/{model_id}_url.xml"
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