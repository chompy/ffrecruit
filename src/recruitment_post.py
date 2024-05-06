from typing import Optional
from datetime import datetime
import re
from src.roles import role_list_to_job_list
from src.intents import intent_to_abbr

class RecruitmentPost:

    def __init__(self):
        self.uid : str = ""
        self.date : Optional[datetime.date] = None
        self.fetcher : str = ""
        self.source : str = ""
        self.original_message : str = ""
        self.original_id : str = ""
        self.schedule : str = ""
        self.tags : list[str] = []
        self.roles : list[str] = []
        self.intent : str = ""
        self.summary : str = ""
        self.contact : str = ""
        self.open_slots : int = 0
        self.url : str = ""

    def clean_up(self):
        self.roles = role_list_to_job_list(self.roles)
        self.intent = intent_to_abbr(self.intent)

    def to_dict(self) -> dict:
        return {
            "uid" : self.uid,
            "date" : self.date.isoformat() if self.date else None,
            "fetcher" : self.fetcher,
            "source" : self.source,
            "original_message" : self.original_message,
            "original_id" : self.original_id,
            "schedule" : self.schedule,
            "tags" : self.tags,
            "roles" : self.roles,
            "intent" : self.intent,
            "summary" : self.summary,
            "contact" : self.contact,
            "open_slots": self.open_slots,
            "url" : self.url
        }

    def from_dict(values : dict):
        post = RecruitmentPost()
        post.uid = values.get("uid", "")
        post.date = datetime.fromisoformat(values.get("date", ""))
        post.fetcher = values.get("fetcher", "")
        post.source = values.get("source", "")
        post.original_message = values.get("original_message", "")
        post.original_id = values.get("original_id", "")
        post.schedule = values.get("schedule", "")
        post.tags = list(set(values.get("tags", [])))
        post.roles = list(set(values.get("roles", [])))
        post.intent = values.get("intent", "")
        post.summary = values.get("summary", "")
        post.contact = values.get("contact", "")
        post.open_slots = values.get("open_slots", 0)
        post.url = values.get("url", "")
        return post

    def storage_key(self) -> str:
        return "%s-%s" % (self.fetcher, self.uid)

    def inject_into_prompt(self, prompt : str) -> str:
        for k, v in self.to_dict().items():
            if type(v) is str: prompt = prompt.replace("{%s}" % k, v)
        return prompt

    def to_str(self) -> str:
        content = ""
        if self.date:
            content += "DATE:\n%s\n\n" % self.date.isoformat()
        if self.intent:
            content += "INTENT:\n%s\n\n" % self.intent
        if self.summary:
            content += "SUMMARY:\n%s\n\n" % self.summary
        if self.roles:
            content += "ROLES:\n%s\n\n" % (",".join(self.roles))
        if self.tags:
            content += "TAGS:\n%s\n\n" % (",".join(self.tags))
        if self.schedule:
            content += "SCHEDULE:\n%s\n\n" % self.schedule
        if self.contact:
            content += "CONTACT:\n%s\n\n" % self.contact
        if self.open_slots:
            content += "OPEN SLOTS:\n%d\n\n" % self.open_slots

        return content

