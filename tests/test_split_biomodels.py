import unittest
import tempfile
import os
from split_biomodels import split_biomodels  # Replace with the actual import path

class TestSplitBiomodels(unittest.TestCase):

    def test_split_biomodels(self):
        # Create a temporary Antimony file with dummy content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.antimony') as temp_file:
            antimony_file_path = temp_file.name
            # Write dummy Antimony content
            temp_file.write(b"model M1 { ... } // model M2 { ... }")

        try:
            # Call the split_biomodels function
            final_items = split_biomodels(antimony_file_path)

            # Check the results
            self.assertGreater(len(final_items), 0, "The final_items should not be empty")
            # You can add more specific checks based on your expected output
            
        finally:
            # Cleanup temporary file
            os.remove(antimony_file_path)

if __name__ == '__main__':
    unittest.main()
