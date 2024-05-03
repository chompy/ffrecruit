from src.fetchers.base import BaseFetcher
from src.recruitment_post import RecruitmentPost
from datetime import datetime
import parsedatetime as pdt
import hashlib

class DiscordPasteFetcher(BaseFetcher):

    SPLIT_STRING = " — "
    INPUT_FILE = "discord-paste.txt"

    def name():
        return "discord-paste"

    def _reset(self):
        self.last_line : str = ""
        self.current_message_date : datetime.date = None
        self.current_message : str = ""
        self.current_post_id : str = ""

    def _make_post(self) -> RecruitmentPost:
        post = RecruitmentPost()
        post.uid = BaseFetcher._hash_string(self.current_post_id)
        post.original_message = "\n".join(self.current_message.splitlines()[0:-1])
        post.date = self.current_message_date
        post.source = DiscordPasteFetcher.name()
        post.contact = "Via '%s' as '%s'" % (self.source.get("name", "n/a"), self.current_post_id)
        self.current_post_id = ""
        self.current_message = ""
        self.current_message_date = None
        return post

    def _fetch_input(self) -> str:
        with open(DiscordPasteFetcher.INPUT_FILE, "r", encoding="utf-8") as f:
            return f.read()

    def fetch(self) -> list[RecruitmentPost]:

        data = self._fetch_input()


        self._reset()
        out = []

        cal = pdt.Calendar()
        now = datetime.now()

        for line in data.splitlines():
            # when split string is found then the previous message was the username
            # the remaining lines are the message
            if DiscordPasteFetcher.SPLIT_STRING in line:
                if self.current_post_id and self.current_message: out.append(self._make_post())
                self.current_post_id = self.last_line.strip()
                self.current_message = ""
                continue

            self.last_line = line

            # first line of message is time
            if self.current_post_id and not self.current_message_date:
                self.current_message_date = cal.parseDT(line.strip(), now)[0]
                continue

            self.current_message += "%s\n" % line
        
        if self.current_post_id and self.current_message: out.append(self._make_post())    

        return out