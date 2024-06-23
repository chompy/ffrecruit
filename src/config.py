import os
import yaml
from typing import Optional

class Config:
    
    def __init__(self):
        self.sources : list[dict] = []
        self.prompts : dict[str] = {}
        self.openai : dict = {}
        self.huggingface : dict = {}
        self.reddit : dict = {}
        self._load()

    def _load(self):
        path_to = os.path.join("conf/config.yaml")
        with open(path_to, "r") as f:
            data = yaml.safe_load(f)
            self.sources = data.get("sources", [])
            self.prompts = data.get("prompts", {})
            self.openai = data.get("openai", {})
            self.huggingface = data.get("huggingface", {})
            self.reddit = data.get("reddit", {})
        return self

    def get_source_by_key(self, key : str) -> Optional[dict]:
        for s in self.sources:
            if s.get("key") == key: return s
        return None

    def get_sources_by_fetcher(self, fetcher : str) -> list[dict]:
        out = []
        for s in self.sources:
            if s.get("fetcher") == fetcher: out.append(s)
        return out

    def get_system_prompt(self) -> str:
        return self.prompts.get("system", "")

    def get_user_prompt(self) -> str:
        return self.prompts.get("user", "")
