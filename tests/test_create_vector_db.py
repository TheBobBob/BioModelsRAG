import unittest
from create_vector_db import create_vector_db  # Replace with the actual import path

final_items = ['''// Compartments and Species:
  compartment comp1;
  species BLL in comp1, IL in comp1, AL in comp1, A in comp1, BL in comp1;
  species B in comp1, DLL in comp1, D in comp1, ILL in comp1, DL in comp1;
  species I in comp1, ALL in comp1;''', '''// Created by libAntimony v2.13.0
model *BIOMD0000000001()''']

class Testing(unittest.TestCase):
    def create_vector_db(self, final_items):
        data = create_vector_db(final_items)
        #import pdb;pdb.set_trace()
        self.assertTrue(isinstance(data, str))
        self.assertTrue(len(data)>0)
    

if __name__ == '__main__':
    unittest.main()
