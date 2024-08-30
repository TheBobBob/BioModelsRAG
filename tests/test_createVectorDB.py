import unittest
from unittest.mock import patch, MagicMock
import chromadb
from chromadb.utils import embedding_functions
from createVectorDB import createVectorDB  # Replace 'your_module' with the actual name of your module

class TestCreateVectorDB(unittest.TestCase):

    @patch('chromadb.PersistentClient')
    @patch('chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction')
    def test_create_vector_db(self, MockEmbeddingFunction, MockPersistentClient):
        # Create a mock instance of PersistentClient
        mock_client = MagicMock()
        MockPersistentClient.return_value = mock_client

        # Mock create_collection method
        mock_collection = MagicMock()
        mock_client.create_collection.return_value = mock_collection

        # Call the function with test parameters
        collection = createVectorDB(
            collection_name="test_collection",
            chroma_data_path="test_path",
            embed_model="test_model",
            metadata={"test_key": "test_value"}
        )

        # Assertions
        MockPersistentClient.assert_called_once_with(path="test_path")
        MockEmbeddingFunction.assert_called_once_with(model_name="test_model")
        mock_client.create_collection.assert_called_once_with(
            collection_name="test_collection",
            embedding_function=MockEmbeddingFunction.return_value,
            metadata={"test_key": "test_value"}
        )
        self.assertEqual(collection, mock_collection)

    @patch('chromadb.PersistentClient')
    @patch('chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction')
    def test_create_vector_db_with_default_values(self, MockEmbeddingFunction, MockPersistentClient):
        # Create a mock instance of PersistentClient
        mock_client = MagicMock()
        MockPersistentClient.return_value = mock_client

        # Mock create_collection method
        mock_collection = MagicMock()
        mock_client.create_collection.return_value = mock_collection

        # Call the function with default parameters
        collection = createVectorDB(
            collection_name="test_collection"
        )

        # Assertions
        MockPersistentClient.assert_called_once_with(path="CHROMA_EMBEDDINGS_PATH")
        MockEmbeddingFunction.assert_called_once_with(model_name="all-MiniLM-L6-v2")
        mock_client.create_collection.assert_called_once_with(
            collection_name="test_collection",
            embedding_function=MockEmbeddingFunction.return_value,
            metadata={"hnsw:space": "cosine"}
        )
        self.assertEqual(collection, mock_collection)

if __name__ == '__main__':
    unittest.main()
