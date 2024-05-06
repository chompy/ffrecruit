import time
import os
import datetime
import json
from src.config import Config
from src.recruitment_post import RecruitmentPost

INPUT_PATH = "data/_output"
OUTPUT_PATH = "web/data.json"

config = Config()

# LOAD POSTS
posts = []
for finfo in os.scandir(INPUT_PATH):
    with open(os.path.join(INPUT_PATH, finfo.name), "r", encoding="utf-8") as f:

        data = json.load(f)
        post = RecruitmentPost.from_dict(data)
        post.clean_up()
        posts.append(post.to_dict())

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(posts, f)