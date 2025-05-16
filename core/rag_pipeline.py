import os

from utils.file_parser import  parse_file
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def extract_text_from_documents(documents):
    """
    Extract and join text from list of Document objects.
    """
    return "\n\n".join([doc.page_content for doc in documents])


def load_split_embed_store(doc_path: str, persist_directory: str, llm):
    # If vector store directory exists, load it
    if os.path.exists(persist_directory):
        vector_store = Chroma(persist_directory=persist_directory,
                              embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                              )
        print("Loaded existing vector store from disk.")
    else:
        print("Persistent directory does not exist. Initializing vector store...")

        # Check if document file exists
        if not os.path.exists(doc_path):
            raise FileNotFoundError(f"The file {doc_path} does not exist. Please check the path.")

        # Load document
        raw_text = parse_file(doc_path)
        documents = [Document(page_content=raw_text, metadata={"source": doc_path})]

        # Split document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)

        # Create embeddings
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Create vector store and persist
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=persist_directory
        )
        vector_store.persist()
        print("Vector store created and persisted.")

    return vector_store


def create_rag_chain(llm, vector_store):
    """Create a retrieval-augmented generation (RAG) chain for QA."""

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an assistant that rewrites the user’s question to be fully self-contained and clear, using the previous conversation."),
        MessagesPlaceholder("chat_history"),
        ("user", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_prompt)

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant. Use ONLY the provided context to answer the question. If the answer is not in the context, reply: 'I don't know.' Keep your answer brief and to the point."),
        ("system", "Context:\n{context}"),
        ("user", "{input}"),
    ])

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return rag_chain

