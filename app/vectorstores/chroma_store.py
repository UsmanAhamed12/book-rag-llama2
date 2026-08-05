from app.db.chroma import get_chroma_client
from app.models.chunk import Chunk


class ChromaVectorStore:

    def __init__(
        self,
        collection_name: str = "book_chunks",
    ) -> None:

        client = get_chroma_client()

        self.collection = client.get_or_create_collection(
            name=collection_name
        )


    def add(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:


        self.collection.add(

            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],


            documents=[
                chunk.text
                for chunk in chunks
            ],


            embeddings=embeddings,


            metadatas=[

                {
                    "document_id": chunk.document_id,

                    "chunk_index": chunk.chunk_index,

                    "source": chunk.metadata.source,

                    "page_number": chunk.metadata.page_number,

                    "start_char": chunk.metadata.start_char,

                    "end_char": chunk.metadata.end_char,

                }

                for chunk in chunks
            ],
        )