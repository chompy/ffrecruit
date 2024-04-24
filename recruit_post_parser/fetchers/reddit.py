from fetchers.base import BaseFetcher
from recruitment_post import RecruitmentPost
import praw
import datetime

class RedditFetcher(BaseFetcher):

    def name():
        return "reddit"

    def fetch(self) -> list[RecruitmentPost]:

        reddit = praw.Reddit(
            client_id = self.config.reddit.get("client_id", ""),
            client_secret = self.config.reddit.get("client_secret", ""),
            user_agent = self.config.reddit.get("user_agent", "")
        )
        reddit.read_only = True
        subr = reddit.subreddit(self.source.get("external_id", ""))

        out = []
        for reddit_post in subr.new(limit=5):
            post = RecruitmentPost()
            post.source = RedditFetcher.name()
            post.uid = BaseFetcher._hash_string(reddit_post.id)
            post.original_id = reddit_post.id
            post.original_message = reddit_post.title + "\n\n" + reddit_post.selftext
            post.date = datetime.datetime.fromtimestamp(reddit_post.created_utc)
            post.url = "https://reddit.com%s" % reddit_post.permalink
            out.append(post)
        
        return out