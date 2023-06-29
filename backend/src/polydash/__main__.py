import uvicorn
from fastapi import FastAPI
from .routers import node, block
from .db import start_db
from .block_retriever.retriever import start_retriever

# Modules set up
start_db()
start_retriever()

# FastAPI set up
app = FastAPI()
# app.include_router(node.router)
app.include_router(block.router)


@app.get("/")
async def root():
    return {"message": "Nothing here"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)