import os
import shutil
import uvicorn
import logging
import uuid

from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from config.config import get_google_api_key
from core.rag_pipeline import load_split_embed_store, create_rag_chain

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
persist_dir = os.path.join(os.path.dirname(__file__), 'db', 'chroma')
temp_dir = "./temp"

def reset_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

reset_dir(temp_dir)

# Set API key
get_google_api_key()

@lru_cache()
def get_llm():
    return ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0)

@app.post("/upload/")
async def upload(file: UploadFile, query: str = Form(...)):
    logger.info(f"Received file: {file.filename}")

    if not file.filename.endswith((".txt", ".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    session_id = str(uuid.uuid4())
    file_path = os.path.join(temp_dir, f"{session_id}_{file.filename}")

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"Saved file to {file_path}")

        llm = get_llm()
        vector_store = load_split_embed_store(file_path, persist_dir, session_id=session_id)
        rag_chain = create_rag_chain(llm, vector_store, session_id=session_id)

        result = rag_chain.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}}
        )

        answer = result.get("answer", "No answer returned.")
        logger.info(f"Query result: {answer}")

        return JSONResponse(content={
            "answer": answer,
            "session_id": session_id
        })

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
