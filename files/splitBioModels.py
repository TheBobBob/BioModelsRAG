from langchain_text_splitters import CharacterTextSplitter
import os
from typing import List, Optional

def splitBioModels(directory: str, final_items: Optional[List[str]] = None) -> List[str]:
    """Separates BioModel database based on indentation

    Args:
        directory (str): Relative path to the folder containing the files.
        final_items (Optional[List[str]]): A list to store the split content. If None, a new list will be created.

    Returns: 
        List[str]: A list of text chunks split from the BioModel files.
    """
    text_splitter2 = CharacterTextSplitter(
        separator="  // ",
        chunk_size=1000000000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )

    if final_items is None:
        final_items = []
    final_items = list(final_items)

    directory_path = os.path.abspath(directory)
    if not os.path.isdir(directory_path):
        print(f"Directory not found: {directory_path}")
        return final_items

    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        try:
            with open(file_path, 'r') as f:
                last_part = os.path.basename(file_path)
                file_content = f.read()
                items = text_splitter2.create_documents([file_content])
                for item in items:
                    item.metadata = last_part
                final_items.extend(items)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return final_items




