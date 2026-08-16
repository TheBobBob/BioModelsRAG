import unittest
from vector_db import create_vector_db, load_vector_db, get_chroma_path  # Replace with the actual import path
import os 
import chromadb 

final_items = ['''// Compartments and Species:
  compartment comp1;
  species BLL in comp1, IL in comp1, AL in comp1, A in comp1, BL in comp1;
  species B in comp1, DLL in comp1, D in comp1, ILL in comp1, DL in comp1;
  species I in comp1, ALL in comp1;''', '''// Created by libAntimony v2.13.0
model *BIOMD0000000001()''']

class Testing(unittest.TestCase):
    def create_vector_db(self, final_items):
        data = create_vector_db(final_items)
        self.assertTrue(isinstance(data, str))
        self.assertTrue(len(data) > 0)

    def test_load_vector_db(tmp_path):
        database_path = tmp_path / "test_db"
        chroma_path = database_path / "chroma"

        client = chromadb.PersistentClient(
            path=str(chroma_path)
        )

        collection = client.get_or_create_collection(
            name="BioModelsRAG"
        )

        collection.add(
            documents=["ATP is converted to ADP during this reaction."],
            ids=["test_id"],
        )

        loaded_collection = load_vector_db(
            database_path
        )

        assert loaded_collection.name == "BioModelsRAG"
        results = loaded_collection.get(
            ids=["test_id"]
        )

        assert results["documents"] == [
            "ATP is converted to ADP during this reaction."
        ]
        
    def get_chroma_path(self, database_path): 
        assert get_chroma_path(database_path) == os.path.join(database_path, "chroma")

if __name__ == '__main__':
    unittest.main()
