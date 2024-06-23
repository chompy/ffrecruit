import os
import json
from src.config import Config
from src.recruitment_post import RecruitmentPost
from src.vector_db import VectorDB

INPUT_DIR = "data/output"

config = Config()

# LOAD POSTS
posts = []
for finfo in os.scandir(INPUT_DIR):
    with open(os.path.join(INPUT_DIR, finfo.name), "r", encoding="utf-8") as f:
        posts.append(RecruitmentPost.from_dict(json.load(f)))

print("> Processing %d posts." % len(posts))

# ADD TO VECTOR DB
vdb = VectorDB(config)
vdb.add(posts)

print("  DONE.")