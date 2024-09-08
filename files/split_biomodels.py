from langchain_text_splitters import CharacterTextSplitter
import os

def split_biomodels(antimony_file_path: str) -> list[str]:
    """Splits the content of an Antimony format model into smaller chunks using a Character Text Splitter.

    Args:
        antimony_file_path (str): A path to the Antimony format model file.

    Returns:
        list[str]: A list of text chunks obtained by splitting the model content.
    """
    text_splitter = CharacterTextSplitter(
        separator="  // ",
        chunk_size=1000,  # Adjust this size according to your needs
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )
    
    final_items = []
    directory_path = os.path.dirname(os.path.abspath(antimony_file_path))
    
    if not os.path.isfile(antimony_file_path):
        print(f"File not found: {antimony_file_path}")
        return final_items

    try:
        with open(antimony_file_path, 'r') as f:
            file_content = f.read()
            # Use text_splitter to split content into documents
            items = text_splitter.create_documents([file_content])
            for item in items:
                # Append each item to final_items
                final_items.append(item)
    
    except Exception as e:
        print(f"Error reading file {antimony_file_path}: {e}")

    return final_items
