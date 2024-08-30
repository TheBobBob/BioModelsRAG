import unittest
from unittest.mock import patch, MagicMock
from typing import Dict
import ollama

from generateResponse import generateResponse
from createVectorDB import createVectorDB


class Testing(unittest.TestCase):
    @patch('ollama.generate')
    @patch('chromadb.Collection')
    def test_split(self, MockCollection, mock_generate):
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            'documents':['Doc1', 'Doc2', 'Doc3']
        }
        MockCollection.return_value = mock_collection 
        mock_generate.return_value = {'response': 'This is the generated response based on the context.'}
        data = generateResponse(query_text="What protein interacts with ach2?", collection=mock_collection)
        self.assertTrue(isinstance(data, str))
        self.assertTrue(len(data)>0)

if __name__ == '__main__':
    unittest.main()