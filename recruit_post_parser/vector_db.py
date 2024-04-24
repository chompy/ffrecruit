import os
from faiss import IndexFlatL2
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config import Config
from recruitment_post import RecruitmentPost

class VectorDB:

    PATH = "data/vector"
    INDEX_NAME = "index"

    def __init__(self, config : Config):
        self.config = config
        self.embeddings = OpenAIEmbeddings(api_key=self.config.openai.get("api_key"), base_url=self.config.openai.get("base_url"))
        faiss = FAISS(
            embedding_function=self.embeddings,
            index=IndexFlatL2(1536),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        if not os.path.exists(VectorDB.PATH):
            faiss.save_local(folder_path=VectorDB.PATH, index_name=VectorDB.INDEX_NAME)
        self.vdb = FAISS.load_local(folder_path=VectorDB.PATH, embeddings=self.embeddings, index_name=VectorDB.INDEX_NAME, allow_dangerous_deserialization=True)

    def _delete_existing_posts(self, posts : list[RecruitmentPost]):
        delete_ids = []
        for post in posts:
            if post.vector_id: delete_ids.append(post.vector_id)
        if delete_ids: self.vdb.delete(delete_ids)
  
    def add(self, posts : list[RecruitmentPost]):
        self._delete_existing_posts(posts)
        docs = []
        for post in posts: docs.append(post.to_vector_document())
        if docs:
            vector_ids = self.vdb.add_documents(docs)
            for i in range(len(vector_ids)):
                posts[i].vector_id = vector_ids[i]

    def dump(self):
        self.vdb.save_local(VectorDB.PATH)

    def query(self, query : str) -> list[str]:
        docs = self.vdb.similarity_search(query)
        print(docs)
        out = []
        for d in docs: out.append(d.metadata.get("key"))
        return out