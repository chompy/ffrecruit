from typing import Optional
from datetime import datetime
from errors import RecruitmentPostValidationException
import re
from langchain_core.documents import Document

class RecruitmentPost:

    VALID_JOBS = ["PLD","WAR","DRK","GNB","WHM","SCH","AST","SGE","MNK","DRG","NIN","SAM","RPR","VIP","BRD","MCH","DNC","BLM","SMN","RDM","PIC","BLU"]
    VALID_INTENTS = ["LFG", "LFM", "FC", "OTHER"]

    def __init__(self):
        self.uid : str = ""
        self.date : Optional[datetime.date] = None
        self.source : str = ""
        self.original_message : str = ""
        self.original_id : str = ""
        self.schedule : str = ""
        self.tags : list[str] = []
        self.jobs : list[str] = []
        self.intent : str = ""
        self.summary : str = ""
        self.discord : list[str] = []
        self.url : str = ""
        self.vector_id : str = ""

    def to_dict(self) -> dict:
        return {
            "uid" : self.uid,
            "date" : self.date.isoformat() if self.date else None,
            "source" : self.source,
            "original_message" : self.original_message,
            "original_id" : self.original_id,
            "schedule" : self.schedule,
            "tags" : self.tags,
            "jobs" : self.jobs,
            "intent" : self.intent,
            "summary" : self.summary,
            "discord" : self.discord,
            "url" : self.url,
            "vector_id" : self.vector_id
        }

    def from_dict(values : dict):
        post = RecruitmentPost()
        post.uid = values.get("uid", "")
        post.date = datetime.fromisoformat(values.get("date", ""))
        post.source = values.get("source", "")
        post.original_message = values.get("original_message", "")
        post.original_id = values.get("original_id", "")
        post.schedule = values.get("schedule", "")
        post.tags = values.get("tags", [])
        post.jobs = values.get("jobs", [])
        post.intent = values.get("intent", "")
        post.summary = values.get("summary", "")
        post.discord = values.get("discord", [])
        post.url = values.get("url", "")
        post.vector_id = values.get("vector_id", "")
        return post

    def validate(self):

        messages = []

        # make regexs
        reDiscord = re.compile("^[a-zA-Z0-9\\.\\_\\-\\#]*$")

        # schedule
        if self.schedule and type(self.schedule) is not str:
            messages.append("'schedule' must be a string")
        # jobs
        for j in self.jobs:
            if j not in RecruitmentPost.VALID_JOBS:
                messages.append("'%s' is not a valid job, it must be one of %s" % (j, ",".join(RecruitmentPost.VALID_JOBS)))
        # intent
        if not self.intent or self.intent not in RecruitmentPost.VALID_INTENTS:
            messages.append("'%s' is not a valid intent, it must be one of %s" % (self.intent, ",".join(RecruitmentPost.VALID_INTENTS)))
        # summary
        if not self.summary or type(self.summary) is not str:
            messages.append("'summary' must be a non empty string")
        # discord
        for d in self.discord:
            if not reDiscord.match(d):
                messages.append("'%s' is not a valid Discord username, please omit it")

        if messages:
            raise RecruitmentPostValidationException("I found one or more errors, please correct them and try again: %s" % (" ; ".join(messages)))

    def storage_key(self) -> str:
        return "%s-%s" % (self.source, self.uid)

    def inject_into_prompt(self, prompt : str) -> str:
        for k, v in self.to_dict().items():
            if type(v) is str: prompt = prompt.replace("{%s}" % k, v)
        return prompt

    def to_string(self):
        return "DATE:\n%s\n\nINTENT:\n%s\n\nSUMMARY:\n%s\n\nJOBS:\n%s\n\nTAGS:\n%s\n\nSCHEDULE:\n%s\n\nDISCORD:\n%s\n\nPERMALINK:\n%s" % (
            self.date.isoformat() if self.date else "n/a", self.intent, self.summary, ",".join(self.jobs), ",".join(self.tags),
            self.schedule if self.schedule else "n/a", self.discord if self.discord else "n/a", self.url if self.url else "n/a"
        )

    def print_to_console(self):
        print(self.to_string())

    def to_vector_document(self) -> Document:
        content = ""
        if self.date:
            content += "DATE:\n%s\n\n" % self.date.isoformat()
        if self.intent:
            content += "INTENT:\n%s\n\n" % self.intent
        if self.summary:
            content += "SUMMARY:\n%s\n\n" % self.summary
        if self.jobs:
            content += "JOBS:\n%s\n\n" % (",".join(self.jobs))
        if self.tags:
            content += "TAGS:\n%s\n\n" % (",".join(self.tags))
        if self.schedule:
            content += "SCHEDULE:\n%s\n\n" % self.schedule
        if self.discord:
            content += "DISCORD:\n%s\n\n" % self.discord

        return Document(
            page_content=content,
            metadata={
                "key" : self.storage_key()
            }
        )

    def update_from_bot_response(self, resp : str):
        
        mode = 0
        current_key = ""
        current_value = ""
        out = {}

        for pos in len(resp):
            char = resp[pos]
            # build key
            if mode == 0:
                if char == ":":
                    mode = 1
                    continue
                current_key += char

            # build content
            elif mode == 1:
                if char == "\n":
                    next_line = resp[i+1:].splitlines()[0].strip()
                    if next_line.endswith(":") and next_line.upper() == next_line:
                        out[current_key.strip().lower()] = current_value.strip()
                        mode = 0
                        continue
                current_value += char

        print(out)

