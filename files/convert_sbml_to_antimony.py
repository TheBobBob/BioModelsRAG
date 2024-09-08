import tellurium as te

def convert_sbml_to_antimony(sbml_file_path: str, antimony_file_path: str) -> None:
    """Converts SBML format biomodels to Antimony format.

    Args:
        sbml_file_path (str): The file path to the SBML format model.
        antimony_file_path (str): The file path where the Antimony format model will be saved.
    """
    try:
        # Load the SBML model using Tellurium
        model = te.loadSBMLModel(sbml_file_path)
        
        # Convert to Antimony format
        antimony_str = model.getCurrentAntimony()
        
        # Write Antimony format to file
        with open(antimony_file_path, 'w') as file:
            file.write(antimony_str)
        
        print(f"Successfully converted SBML to Antimony: {antimony_file_path}")
    
    except Exception as e:
        print(f"Error converting SBML to Antimony from {sbml_file_path} to {antimony_file_path}: {e}")
