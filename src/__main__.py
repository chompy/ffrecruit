import argparse
from datetime import datetime
import parsedatetime as pdt
import pickledb

from config import Config
from fetchers.reddit import RedditFetcher
from errors import InvalidArgumentException
from recruitment_post import RecruitmentPost
from bot import Chatbot
from vector_db import VectorDB

AVAILABLE_FETCHERS = [RedditFetcher]

parser = argparse.ArgumentParser(description='Parses recruitment posts copy and pasted from Discord.')
parser.add_argument("source", type=str)

args = parser.parse_args()

# load config
config = Config().load_from_yaml()
source = config.get_source_by_key(args.source)

# verify that provided source is in config
if not source:
    raise InvalidArgumentException("provided 'source' argument is not valid")

# init classes
bot = Chatbot(config)
db = pickledb.load("data/_rp.db", False)
vdb = VectorDB(config)

#keys = vdb.query("")
#p = RecruitmentPost.from_dict(db.get(keys[0]))
#p.print_to_console()
#sys.quit()

# find fetcher
fetcher = None
for fclass in AVAILABLE_FETCHERS:
    if fclass.name() == source.get("fetcher", ""):
        fetcher = fclass(config, args.source)
if not fetcher:
    raise InvalidArgumentException("no fetcher available for given source")

# fetch posts
posts = fetcher.fetch()
updated_posts = []

# process posts
for post in posts:
    print("> %s" % post.uid)

    # check if post already exists and ensure it's been updated before processing
    spost = db.get(post.storage_key())
    if spost:
        spost = RecruitmentPost.from_dict(spost)
        if post.date == spost.date:
            print("\t - Post not modified, skipping.")
            continue
        continue

    # process post
    try:
        bot.process_post(post)
    except Exception as e:
        print("\t - An error occured.")
        #continue
        raise e
        
    post.print_to_console()
    updated_posts.append(post)

# save to vector db
vdb.add(updated_posts)
vdb.dump()

# save to pickle db
for post in updated_posts:
    db.set(post.storage_key(), post.to_dict())
db.dump()
