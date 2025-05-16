import os
import shutil
import uvicorn
import logging

from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse

from config.config import get_google_api_key
from functools import lru_cache
from core.rag_pipeline import load_split_embed_store, create_rag_chain
from langchain_google_genai import ChatGoogleGenerativeAI

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
persist_dir = os.path.join(os.path.dirname(__file__), 'db', 'chroma')
temp_dir = "./temp"

# Ensure clean temp directory
def reset_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


get_google_api_key()

@lru_cache()
def get_llm():
    return ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0)


@app.post("/upload/")
async def upload(file: UploadFile, query: str = Form(...)):
    logger.info(f"Received file: {file.filename}")

    reset_dir(temp_dir)
    reset_dir(persist_dir)

    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    logger.info(f"Saved file to {file_path}")

    llm = get_llm()
    vector_store = load_split_embed_store(file_path, persist_dir, llm)
    rag_chain = create_rag_chain(llm, vector_store)

    result = rag_chain.invoke({"input": query})
    # logger.info(f"Query result: {result['answer']}")
    return JSONResponse(content={"answer": result["answer"]})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
