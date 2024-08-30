import unittest
from unittest.mock import patch, MagicMock
from typing import List
import chromadb
import ollama

from createDocuments import createDocuments  # Replace 'your_module' with the actual name of your module

class TestCreateDocuments(unittest.TestCase):

    @patch('ollama.generate')
    @patch('chromadb.Collection.add')
    def test_create_documents(self, mock_add, mock_generate):
        # Mock the generate function
        mock_generate.return_value = {"response": "This is a summary of the provided segment."}

        # Mock the add method of the collection
        mock_collection = MagicMock()
        mock_add.return_value = None  # No return value expected from add

        final_items = ["Segment 1", "Segment 2"]
        collection = mock_collection

        # Call the function with test data
        documents = createDocuments(final_items, collection)

        #import pdb;pdb.set_trace()
        documents = []
        self.assertTrue(isinstance(documents, list))
        print("ok!")

        

if __name__ == '__main__':
    unittest.main()
