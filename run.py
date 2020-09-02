import concurrent.futures
import csv
import itertools
import os.path
import time
from datetime import datetime
from pprint import pprint

import pandas as pd
import praw

# from tqdm import tqdm

import utils
from args import args

# https://www.reddit.com/r/redditdev/comments/7muatr/praw_rate_limit_headers/drww09u
# No rate limits for reading the data
saved_details = {}
t1 = time.perf_counter()
# Day,Month,Year,Hour,Minute,Second
pattern = f"%d-%m-%Y-%H-%M-%S"
fetch_start = datetime.utcnow()
fetch_start_utc = float(int(fetch_start.timestamp()))
fetch_start = fetch_start.strftime(pattern)
headers = "ExampleApp"
reddit = praw.Reddit("bot1", user_agent=headers)
print(f"Reddit Read only mode: {reddit.read_only}")
print("*" * 80)

input_file_name = args.input_path + args.input_file_name

with open(input_file_name, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)
subreddits_to_crawl = list(itertools.chain.from_iterable(data))

print(f"We will crawl the following subreddits:")
pprint(sorted(subreddits_to_crawl), compact=True)
print("*" * 80)
output_path = args.output_path
if not os.path.isdir(output_path):
    os.mkdir(output_path)

fetch_type = args.submissions_type + "_"

submissions_file_name = (
    output_path + args.output_file_names[0] + fetch_type + fetch_start + ".csv"
)
comments_file_name = (
    output_path + args.output_file_names[1] + fetch_type + fetch_start + ".csv"
)
submission_columns = args.submission_columns
cleanse_submission_columns = args.cleanse_submission_columns

print(f"The data we'll pull from submissions is:")
pprint(sorted(submission_columns), compact=True)
print("*" * 80)
submissions_count = args.submissions_count
submissions_type = args.submissions_type
time_filter = args.time_filter
comments = args.comments
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    readObjs = executor.map(
        utils.fetch_submissions,
        subreddits_to_crawl,
        [reddit] * len(subreddits_to_crawl),
        [submissions_count] * len(subreddits_to_crawl),
        [submissions_type] * len(subreddits_to_crawl),
        [time_filter] * len(subreddits_to_crawl),
    )

t2 = time.perf_counter()
print(f"Fetching submissions Finished in {t2-t1} seconds")

submissions_df_dict, submissions_to_crawl = utils.cleanse_submissions(
    cleanse_submission_columns, comments, readObjs, submission_columns
)
t3 = time.perf_counter()
print(f"Cleansing submissions Finished in {t3-t2} seconds")
total_submissions = len(submissions_df_dict["permalink"])
if comments:
    comments_count = args.comments_count
    comment_columns = args.comment_columns
    link_comments_columns = args.link_comments_columns
    cleanse_comments_columns = args.cleanse_comments_columns

    print(f"The data we'll pull from comments is:")
    pprint(sorted(comment_columns), compact=True)
    print("*" * 80)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        submission_comments = executor.map(
            utils.fetch_comments,
            submissions_to_crawl,
            [reddit] * len(submissions_to_crawl),
            [comments_count] * len(submissions_to_crawl),
        )
    t4 = time.perf_counter()
    print(f"Fetching comments Finished in {t4-t3} seconds")
    comments_df_dict = utils.cleanse_comments(
        cleanse_comments_columns,
        submission_comments,
        comment_columns,
        link_comments_columns,
    )
    t5 = time.perf_counter()
    print(f"Cleansing comments Finished in {t5-t4} seconds")
    total_comments = len(comments_df_dict["permalink"])
    res = pd.DataFrame.from_dict(comments_df_dict)
    res["fetched_utc"] = fetch_start_utc
    res.to_csv(comments_file_name, index=False, index_label="permalink")
    saved_details["comments"] = comments_file_name

res = pd.DataFrame.from_dict(submissions_df_dict)
res["fetched_utc"] = fetch_start_utc
res.to_csv(submissions_file_name, index=False, index_label="permalink")
saved_details["submissions"] = submissions_file_name

print(f"Finished in fetching and processing all posts")
print("*" * 80)
t6 = time.perf_counter()

if comments:
    print(
        f"Crawled and Processed {total_submissions + total_comments} entries in {t6-t1} seconds"
    )
else:
    print(f"Crawled and Processed {total_submissions} entries in {t6-t1} seconds")
print("*" * 80)

print("Outputs are saved at the following location:")
pprint(saved_details)
print("*" * 80)
