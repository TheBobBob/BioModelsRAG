import unittest
from unittest.mock import patch, MagicMock
from generate_response import generate_response

class TestGenerateResponse(unittest.TestCase):
    
    @patch('ollama.generate')  # Mock the ollama generate function
    def test_generate_response(self, mock_ollama_generate):
        # Create a mock for the db query method
        mock_db = MagicMock()
        mock_db.query.return_value = {
            'documents': ['This is a test context for the query.']
        }
        
        # Mock the response from the ollama model
        mock_ollama_generate.return_value = {
            'response': 'This is a test response from the model.'
        }

        # Simulate the user input for the query
        with patch('builtins.input', return_value="Test query"):
            response = generate_response(mock_db)

        # Assert that the response is as expected
        self.assertEqual(response, 'This is a test response from the model.')

if __name__ == '__main__':
    unittest.main()
