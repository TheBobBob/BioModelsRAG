import unittest
from unittest.mock import patch, MagicMock
from download_model_file import download_model_file

class TestDownloadModelFile(unittest.TestCase):
    @patch('requests.get')
    def test_successful_download(self, mock_get):
        # Mock the HTTP response
        model_id = 'BIOMD0000000001'
        model_url = f"https://raw.githubusercontent.com/konankisa/BiomodelsStore/main/biomodels/{model_id}/{model_id}_url.xml"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<xml>Data</xml>"
        mock_get.return_value = mock_response
        
        # Call the function
        file_path = download_model_file(model_url, model_id)
        
        # Assert the returned path is correct (this will vary depending on your LOCAL_DOWNLOAD_DIR setup)
        self.assertIsNotNone(file_path)
        self.assertTrue(file_path.endswith(f"{model_id}.xml"))

    @patch('requests.get')
    def test_failed_download(self, mock_get):
        # Mock the HTTP response for a failed request
        model_id = 'BIOMD0000000002'
        model_url = f"https://raw.githubusercontent.com/konankisa/BiomodelsStore/main/biomodels/{model_id}/{model_id}_url.xml"
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Call the function
        file_path = download_model_file(model_url, model_id)
        
        # Assert the function handles the error correctly
        self.assertIsNone(file_path)

    @patch('requests.get')
    def test_exception_handling(self, mock_get):
        # Simulate an exception during the HTTP request
        model_id = 'BIOMD0000000003'
        model_url = f"https://raw.githubusercontent.com/konankisa/BiomodelsStore/main/biomodels/{model_id}/{model_id}_url.xml"
        
        mock_get.side_effect = Exception("Network error")
        
        # Call the function
        file_path = download_model_file(model_url, model_id)
        
        # Assert the function handles exceptions correctly
        self.assertIsNone(file_path)

if __name__ == '__main__':
    unittest.main()
