from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(
    title="Book RAG Llama2",
    version="1.0.0"
)


app.include_router(
    api_router,
)


@app.get("/")
def health_check():

    return {
        "status": "running"
    }