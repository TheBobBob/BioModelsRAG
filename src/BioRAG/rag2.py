# -*- coding: utf-8 -*-
"""RAG2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fskQmtugai5co1I64Hv3iAcKQKUKHAzU
"""

import re
#pip install langchain_community
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

#attempt at character based splitter, using the line indexes would not work because each chunk has to be assigned to a document

#for loop here for each and every one, and then concatenate it to the end
#takes a super long time because of how many files there are too split, so may consider just pulling out a few to test on, but we will see that tomorrow
text_splitter2 = CharacterTextSplitter(
    separator = "  // ",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

final_items = []
import os
directory = r"/content/drive/MyDrive/biomodels (2)" #can do all but for the purposes of this, will do a mix of different biomodels across the spectrum (around 30 max!)
files = os.listdir(directory)

for file in files:
    file_path = os.path.join(directory, file)
    with open(file_path, 'r') as f:
        file_content = f.read()
        items = text_splitter2.create_documents([file_content])
        final_items.extend(items)

type(items)

#pip install chromadb
#pip install sentence_transformers
import chromadb
from chromadb.utils import embedding_functions

#establishing chroma db
CHROMA_DATA_PATH = r"/content/CHROMA Embeddings"
COLLECTION_NAME = "BIOMODELS"
EMBED_MODEL = "all-MiniLM-L6-v2"
client = chromadb.PersistentClient(path = CHROMA_DATA_PATH)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)

collection = client.create_collection(
    name = "BIOMODELSww",
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"},
)

from google.colab import drive
drive.mount('/content/drive')

import google.generativeai as genai
import os

os.environ["API_KEY"] = "AIzaSyBIZakoaE9S0QhbzOw2msHRwczRAl14zmQ"

genai.configure(api_key=os.environ["API_KEY"])

model1 = genai.GenerativeModel('gemini-1.5-flash')

i=0

documents = []

for item in final_items:
    print(item)
    prompt = f'Please summarize this segment of Antimony format code:{item}. The summaries must be clear and concise. For Display Names, provide the value for each variable.  Do not expand mathematical functions into words.'
    documents2 = model1.generate_content(prompt)
    documents3 = documents2.text
    documents.append(documents3) #issue is that each variable is not being defined properly.

collection.add(
    documents = documents,
    ids=[f"id{i}" for i in range(len(documents))] #doesnt work because the entire thing is still one whole document
)

print(documents[7])
type(documents)

query_results = collection.query(
    query_texts = ["Give the model that has ATP in it. What is the metadata for this model? "],
    n_results=5,
)

print(query_results)
best_recommendation = query_results["documents"]

query_texts = "Give the model that has ATP in it. What is the metadata for this model? "

prompt_template = prompt_template = f"""Use the following pieces of context to answer the question at the end. If you don't know the answer, say so.

This is the first piece of context necessary: {best_recommendation}

Cross-reference all pieces of context to define variables and other unknown entities. Calculate mathematical values based on provided matching variables.

Question: {query_texts}

"""
response = model1.generate_content(prompt_template)
print(response.text)

type(response)

print(best_recommendation)