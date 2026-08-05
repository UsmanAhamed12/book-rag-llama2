from app.db.chroma import get_chroma_client

client = get_chroma_client()

collection = client.get_collection("book_chunks")

result = collection.get(limit=5)

for metadata in result["metadatas"]:
    print(metadata)