from src.recruitment_post import RecruitmentPost
from src.config import Config
import hashlib

class BaseFetcher:

    def __init__(self, config : Config, source_key : str):
        self.config = config
        self.source = self.config.get_source_by_key(source_key)

    def _hash_string(value : str) -> str:
        h = hashlib.new("sha256")
        h.update(value.encode())
        return h.hexdigest()

    def name():
        return ""

    def fetch(self) -> list[RecruitmentPost]:
        return []