from parsers.base_parser import BaseParser
from recruitment_post import RecruitmentPost
from datetime import datetime
import parsedatetime as pdt
import hashlib

class DiscordPasteParser(BaseParser):

    NAME = "discord-paste"
    SPLIT_STRING = " — "

    def _reset(self):
        self.last_line : str = ""
        self.current_message_date : datetime.date = None
        self.current_message : str = ""
        self.current_post_id : str = ""

    def _make_post(self) -> RecruitmentPost:
        post = RecruitmentPost()
        h = hashlib.new("sha256")
        h.update(self.current_post_id.encode())
        post.uid = h.hexdigest()
        post.original_message = "\n".join(self.current_message.splitlines()[0:-1])
        post.date = self.current_message_date
        post.source = self.source
        self.current_post_id = ""
        self.current_message = ""
        self.current_message_date = None
        return post

    def parse(self, source : str, data : str) -> list[RecruitmentPost]:

        self.source : str = source
        self._reset()
        out = []

        cal = pdt.Calendar()
        now = datetime.now()

        for line in data.splitlines():
            # when split string is found then the previous message was the username
            # the remaining lines are the message
            if DiscordPasteParser.SPLIT_STRING in line:
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