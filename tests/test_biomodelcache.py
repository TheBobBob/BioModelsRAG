import unittest
from unittest.mock import patch, MagicMock
from biomodelcache import BioModelCacheRetrieval
import os

class TestBioModelCacheRetrieval(unittest.TestCase):
    
    @patch('requests.get')
    def test_search_models_success(self, mock_get):
        # Mock the response for the GitHub API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "download_url": "http://example.com/cached_biomodels.json"
        }
        mock_get.return_value = mock_response

        # Mock the response for the cached biomodels JSON
        mock_response_json = MagicMock()
        mock_response_json.status_code = 200
        mock_response_json.json.return_value = {
            "model_id_1": {
                "name": "Test Model One",
                "url": "http://example.com/model_1",
                "model_id": "model_id_1",
                "title": "Title One",
                "authors": ["Author A"]
            },
            "model_id_2": {
                "name": "Another Test Model",
                "url": "http://example.com/model_2",
                "model_id": "model_id_2",
                "title": "Title Two",
                "authors": ["Author B"]
            }
        }
        
        mock_get.side_effect = [mock_response, mock_response_json]

        # Create an instance of the BioModelCacheRetrieval class
        search_str = "test model"
        retriever = BioModelCacheRetrieval(search_str)
        
        # Call the search_models method
        models = retriever.search_models()
        
        # Check the results
        self.assertEqual(len(models), 2)
        self.assertIn('model_id_1', models)
        self.assertIn('model_id_2', models)

    @patch('requests.get')
    def test_download_model_files_success(self, mock_get):
        # Mock the response for downloading a model file
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<sbml></sbml>'
        mock_get.return_value = mock_response
        
        model_id = "model_id_1"
        model_url = "http://example.com/model_1_url.xml"
        
        # Call the download_model_files method
        file_path = BioModelCacheRetrieval.download_model_files(model_url, model_id)
        
        # Check if the file path is valid
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))
        
        # Cleanup the created file
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
