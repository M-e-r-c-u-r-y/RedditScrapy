import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--submissions_count",
    type=int,
    default=10,
    help="The number of submissions to crawl in the subreddits",
)
parser.add_argument(
    "--submissions_type",
    type=str,
    default="hot",
    help="The submissions type to crawl in the subreddits",
)
parser.add_argument(
    "--time_filter",
    type=str,
    default="day",
    help="The submissions type to crawl in the subreddits",
)
parser.add_argument(
    "--comments_count",
    type=str,
    default="32",
    help="The number of MoreComments to crawl in the comments section",
)
parser.add_argument(
    "--output_path",
    type=str,
    default="./output/",
    help="Output path for the processed files",
)
parser.add_argument(
    "--input_path",
    type=str,
    default="./input/",
    help="Input path for the subreddits_to_crawl file",
)
parser.add_argument(
    "--input_file_name",
    type=str,
    default="subreddits_to_crawl.csv",
    help="File containing csv of subreddits to crawl",
)

feature_parser = parser.add_mutually_exclusive_group(required=False)
feature_parser.add_argument(
    "--comments",
    dest="comments",
    action="store_true",
    help="Flag to switch on the crawling of comments",
)
feature_parser.add_argument(
    "--no-comments",
    dest="comments",
    action="store_false",
    help="Flag to switch off the crawling of comments",
)
parser.set_defaults(comments=True)

args = parser.parse_args()

if args.comments_count == "None":
    args.comments_count = None
else:
    try:
        args.comments_count = int(args.comments_count)
    except ValueError:
        print("Please pass a number or None")
        raise

args.__dict__["submission_columns"] = [
    "permalink",
    "url",
    "author",
    "created_utc",
    "subreddit_name_prefixed",
    "media",
    "media_only",
    "is_video",
    "is_original_content",
    "whitelist_status",
    "parent_whitelist_status",
    "over_18",
    "likes",
    "num_reports",
    "total_awards_received",
    "is_robot_indexable",
    "title",
    "selftext",
    "ups",
    "downs",
    "score",
]

args.__dict__["cleanse_submission_columns"] = ["selftext", "title"]

args.__dict__["comment_columns"] = [
    "permalink",
    "author",
    "created_utc",
    "subreddit_name_prefixed",
    "likes",
    "num_reports",
    "total_awards_received",
    "ups",
    "downs",
    "score",
    "body",
    "parent_id",
    "submission",
]

args.__dict__["link_comments_columns"] = ["permalink", "parent_id", "submission"]

args.__dict__["cleanse_comments_columns"] = ["body"]

args.__dict__["output_file_names"] = ["submissions_", "comments_"]

