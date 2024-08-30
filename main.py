from createVectorDB import createVectorDB
from splitBioModels import splitBioModels
from createDocuments import createDocuments
from generateResponse import generateResponse

DATA_PATH = r"C:\Users\navan\Downloads\BioModelsRAG\BioModelsRAG\2data"
CHROMA_DATA_PATH = r"C:\Users\navan\Downloads\BioModelsRAG\CHROMA_EMBEDDINGS_PATH"

def main(report:bool = True, directory = DATA_PATH, chroma_data_path = CHROMA_DATA_PATH):
    data = []
    splitBioModels(directory=DATA_PATH, final_items=data)

    collection = createVectorDB(
        collection_name="123456789101112131415",
        chroma_data_path=chroma_data_path,
        embed_model="all-MiniLM-L6-v2",
        metadata={"hnsw:space": "cosine"}
    )

    if report:
        print("Collection created:", collection)

    createDocuments(final_items=data, collection=collection)

    if report:
        print("Documents added to collection.")

    query = "What protein interacts with DesensitizedAch2?"
    result = generateResponse(query_text=query, collection=collection)
    return result
#name of the program running v
if __name__ == "__main__":
    result = main()
    print(result)

