import os
import argparse
import json
from src.config import Config
from src.errors import InvalidArgumentException
from src.fetchers.reddit import RedditFetcher
from src.fetchers.discord_paste import DiscordPasteFetcher
from src.recruitment_post import RecruitmentPost

config = Config()

AVAILABLE_FETCHERS = [RedditFetcher, DiscordPasteFetcher]
STORE_PATH = "data/input"
PARSED_PATH = "data/output"

parser = argparse.ArgumentParser(description='Fetch recruitment post from given source.')
parser.add_argument("source", type=str)
args = parser.parse_args()

source_config = config.get_source_by_key(args.source)
if not source_config:
    raise InvalidArgumentException("source '%s' not found" % args.source)

if not source_config.get("fetcher"):
    raise InvalidArgumentException("could not find fetcher for '%s' not found" % args.source)

def _check_parsed_post(fetched_post : RecruitmentPost):
    parse_path_to = os.path.join(PARSED_PATH, fetched_post.storage_key() + ".json")
    if os.path.exists(parse_path_to):
        delete_parsed = False
        with open(parse_path_to, "r", encoding="utf-8") as f:
            parsed_post = RecruitmentPost.from_dict(json.load(f))
            if parsed_post.date < fetched_post.date:
                delete_parsed = True
        if delete_parsed:
            os.remove(parse_path_to)
            print("\tUPDATE DETECTED.")

for fetcher_class in AVAILABLE_FETCHERS:
    if source_config.get("fetcher") == fetcher_class.name():
        fetcher = fetcher_class(config, args.source)
        print("> Using '%s' fetcher." % fetcher_class.name())
        for post in fetcher.fetch():
            print("  - %s" % post.uid)
            _check_parsed_post(post)
            path_to = os.path.join(STORE_PATH, post.storage_key() + ".json")
            with open(path_to, "w", encoding="utf-8") as f:
                json.dump(post.to_dict(), f)        

