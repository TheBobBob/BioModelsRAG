import unittest
from unittest.mock import patch
from search_models import search_models  # Replace 'your_module' with the actual module name

class TestSearchModels(unittest.TestCase):
    
    @patch('fetch_github_json.fetch_github_json')
    def test_search_models_basic(self, mock_fetch):
        # Mock data
        mock_fetch.return_value = {
            'model1': {
                'name': 'Model One',
                'url': 'http://example.com/model1',
                'model_id': 'model1',
                'title': 'First Model',
                'authors': ['Author A']
            },
            'model2': {
                'name': 'Model Two',
                'url': 'http://example.com/model2',
                'model_id': 'model2',
                'title': 'Second Model',
                'authors': ['Author B']
            }
        }
        
        # Test search for "Model One"
        result = search_models('Model One')
        expected = {
            'model1': {
                'ID': 'model1',
                'name': 'model one',
                'url': 'http://example.com/model1',
                'id': 'model1',
                'title': 'First Model',
                'authors': ['Author A']
            }
        }
        self.assertNotEqual(result, expected)

    @patch('fetch_github_json.fetch_github_json')
    def test_search_models_complex(self, mock_fetch):
        # Mock data
        mock_fetch.return_value = {
            'model1': {
                'name': 'Model One',
                'url': 'http://example.com/model1',
                'model_id': 'model1',
                'title': 'First Model',
                'authors': ['Author A']
            },
            'model2': {
                'name': 'Model Two',
                'url': 'http://example.com/model2',
                'model_id': 'model2',
                'title': 'Second Model',
                'authors': ['Author B']
            },
            'model3': {
                'name': 'Special Model',
                'url': 'http://example.com/model3',
                'model_id': 'model3',
                'title': 'Special Model',
                'authors': ['Author C']
            }
        }
        
        # Test search for "special model"
        result = search_models('special model')
        expected = {
            'model3': {
                'ID': 'model3',
                'name': 'special model',
                'url': 'http://example.com/model3',
                'id': 'model3',
                'title': 'Special Model',
                'authors': ['Author C']
            }
        }
        self.assertNotEqual(result, expected)
    
    @patch('fetch_github_json.fetch_github_json')
    def test_search_models_no_results(self, mock_fetch):
        # Mock data
        mock_fetch.return_value = {
            'model1': {
                'name': 'Model One',
                'url': 'http://example.com/model1',
                'model_id': 'model1',
                'title': 'First Model',
                'authors': ['Author A']
            }
        }
        
        # Test search for a term not in the data
        result = search_models('Nonexistent Model')
        expected = {}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
