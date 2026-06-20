import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv()
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

FAISS_PATH = "data/faiss_index"

chat_histories = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

def save_preference(preference: str):
    docs = [Document(page_content=preference)]
    if os.path.exists(FAISS_PATH):
        db = FAISS.load_local(FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
        db.add_documents(docs)
    else:
        db = FAISS.from_documents(docs, embedding_model)
    
    db.save_local(FAISS_PATH)

def get_relevant_preferences(query: str)-> str:
    if not os.path.exists(FAISS_PATH):
        return ""
    
    db = FAISS.load_local(FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    results = db.similarity_search(query, k=3)
    
    if not results:
        return ""
    
    return "\n".join([doc.page_content for doc in results])

