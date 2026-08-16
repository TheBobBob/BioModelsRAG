import unittest
from unittest.mock import patch, MagicMock
from generate_response import generate_response

class TestGenerateResponse(unittest.TestCase):
    
    @patch('ollama.generate')
    def test_generate_response_ollama(self, mock_ollama_generate):
        mock_db = MagicMock()
        mock_db.query.return_value = {
            'documents': ['This is a test context for the query.']
        }
        
        mock_ollama_generate.return_value = {
            'response': 'This is a test response from the model.'
        }

        with patch('builtins.input', return_value="Test query"):
            response = generate_response(mock_db)

        self.assertEqual(response, 'This is a test response from the model.')

    @patch('groq.generate')
    def test_generate_response_groq(self, mock_groq_generate):
        mock_db = MagicMock()
        mock_db.query.return_value = {
            'documents': ['This is a test context for the query.']
        }

        mock_groq_generate.return_value = {
            'response': 'test response'
        }

        
        with patch('builtins.input', return_value="Test query"):
            response = generate_response(mock_db)

        self.assertEqual(response, 'test response')
        
                
if __name__ == '__main__':
    unittest.main()
