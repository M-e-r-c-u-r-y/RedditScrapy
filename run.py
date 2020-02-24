import praw
from pprint import pprint
from args import args
from tqdm import tqdm
import pandas as pd
import utils
import os.path
import csv
import itertools
import concurrent.futures
# https://www.reddit.com/r/redditdev/comments/7muatr/praw_rate_limit_headers/drww09u
# No rate limits for reading the data

headers = "RedditScrapyApp"
reddit = praw.Reddit('bot1', user_agent=headers)
print(f"Read only mode: {reddit.read_only}")

input_file_name = args.input_path + args.input_file_name

with open(input_file_name, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
subreddits_to_crawl = list(itertools.chain.from_iterable(data))

print(f"We will crawl {', '.join(subreddits_to_crawl)} subreddits")

output_path = args.output_path
if not os.path.isdir(output_path):
    os.mkdir(output_path)

submissions_file_name = output_path + args.output_file_names[0]
comments_file_name = output_path + args.output_file_names[1]
submission_columns = args.submission_columns
cleanse_submission_columns = args.cleanse_submission_columns

print(f"The data we'll pull from submissions is {submission_columns}")

submissions_count = args.submissions_count
comments = args.comments
with concurrent.futures.ThreadPoolExecutor() as executor:
  readObjs = executor.map(utils.fetch_submissions, subreddits_to_crawl, [reddit] * len(subreddits_to_crawl), [submissions_count] * len(subreddits_to_crawl))

submissions_df_dict, submissions_to_crawl = utils.cleanse_submissions(cleanse_submission_columns, comments, readObjs, submission_columns)

if comments:
  comments_count = args.comments_count
  comment_columns = args.comment_columns
  link_comments_columns = args.link_comments_columns
  cleanse_comments_columns = args.cleanse_comments_columns

  print(f"The data we'll pull from comments is {comment_columns}")

  with concurrent.futures.ThreadPoolExecutor() as executor:
    submission_comments = executor.map(utils.fetch_comments, submissions_to_crawl, [reddit] * len(submissions_to_crawl), [comments_count] * len(submissions_to_crawl))

  comments_df_dict = utils.cleanse_comments(cleanse_comments_columns, submission_comments, comment_columns, link_comments_columns)

  res = pd.DataFrame.from_dict(comments_df_dict)
  res.to_csv(comments_file_name,index=False, index_label='permalink')

res = pd.DataFrame.from_dict(submissions_df_dict)
res.to_csv(submissions_file_name,index=False, index_label='permalink')

print(f'Finished in fetching and processing all posts')