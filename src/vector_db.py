import os
import chromadb
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.config import Config
from src.recruitment_post import RecruitmentPost

class VectorDB:

    PATH = "data/vector"

    def __init__(self, config : Config):
        self.config = config
        #self.embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self.db = chromadb.PersistentClient(VectorDB.PATH)
  
    def add(self, posts : list[RecruitmentPost]):
        col = self.db.get_or_create_collection("ffrecruit")

        docs = []
        ids = []
        meta = []

        for post in posts:
            docs.append(post.to_str())
            meta.append({"source": post.source, "intent": post.intent, "original_id": post.original_id, "storage_key": post.storage_key()})
            ids.append(post.uid)

        if docs: col.upsert(documents=docs, metadatas=meta, ids=ids)

    def query(self, query : str) -> list[str]:
        col = self.db.get_or_create_collection("ffrecruit")
        return col.query(
            query_texts=[query],
            where={"intent": "Looking For Members"},
            n_results=30
        )
        