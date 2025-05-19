import os
import logging

from utils.file_parser import parse_file
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

logger = logging.getLogger(__name__)

# In-memory message history store keyed by session_id
message_history_store = {}


def get_message_history(session_id: str):
    if session_id not in message_history_store:
        message_history_store[session_id] = InMemoryChatMessageHistory()
    return message_history_store[session_id]


def load_split_embed_store(doc_path: str, base_persist_dir: str, session_id: str):
    persist_directory = os.path.join(base_persist_dir, session_id)
    os.makedirs(persist_directory, exist_ok=True)

    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"File not found: {doc_path}")

    raw_text = parse_file(doc_path)
    documents = [Document(page_content=raw_text, metadata={"source": doc_path})]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    return vector_store


def create_rag_chain(llm, vector_store, session_id: str) -> Runnable:
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that rewrites the user’s question to be fully self-contained and clear, using the previous conversation."),
        MessagesPlaceholder("chat_history"),
        ("user", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_prompt)

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use ONLY the provided context to answer the question. If the answer is not in the context, reply: 'I don't know.'"),
        ("system", "Context:\n{context}"),
        ("user", "{input}"),
    ])

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return RunnableWithMessageHistory(
        rag_chain,
        get_message_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
