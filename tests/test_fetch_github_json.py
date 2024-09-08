import unittest
from unittest.mock import patch, Mock
import requests

from fetch_github_json import fetch_github_json, GITHUB_OWNER, GITHUB_REPO_CACHE, BIOMODELS_JSON_DB_PATH

class TestFetchGitHubJson(unittest.TestCase):
    @patch('fetch_github_json.requests.get')
    def test_fetch_github_json_no_download_url(self, mock_get):
        # Setup mock response with no download_url
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        # Call the function and check for ValueError
        with self.assertRaises(ValueError):
            fetch_github_json()

    @patch('fetch_github_json.requests.get')
    def test_fetch_github_json_request_failure(self, mock_get):
        # Setup mock response with failure status code
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Call the function and check for ValueError
        with self.assertRaises(ValueError):
            fetch_github_json()

if __name__ == '__main__':
    unittest.main()
