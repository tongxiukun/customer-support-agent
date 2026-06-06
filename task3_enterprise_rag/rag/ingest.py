import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

def build_vector_store():
    loader = DirectoryLoader("corpus",glob="*.md")
    raw_docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
    split_chunks = splitter.split_documents(raw_docs)
    for idx,doc in enumerate(split_chunks):
        doc.metadata["chunk_id"] = f"chunk_{idx:03d}"
        doc.metadata["min_role"] = "intern" if idx%4 !=0 else "manager"
    embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(split_chunks,embed)
    db.save_local("faiss_index")
    print(f"向量库构建完成，分片总数：{len(split_chunks)}")

if __name__ == "__main__":
    build_vector_store()