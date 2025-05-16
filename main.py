from config.config import get_google_api_key
from core.rag_pipeline import load_split_embed_store, create_rag_chain

from langchain_google_genai import ChatGoogleGenerativeAI

import os


def main():
    get_google_api_key()

    doc_path = "data/pima_diabetes_prediction_project.pdf"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    persist_directory = os.path.join(current_dir, 'db', 'chroma')

    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature = 0)

    # Load, split, embed, and store
    vector_store = load_split_embed_store(doc_path, persist_directory,llm)

    # Create RAG chain
    rag_chain = create_rag_chain(llm, vector_store)

    # Now you can query your rag_chain
    query = "What is the main point of the document?"
    result = rag_chain.invoke({"input": query})

    # print("Answer:", result)
    print("Answer:", result["answer"])


if __name__ == "__main__":
    main()
