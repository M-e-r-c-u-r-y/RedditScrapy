import argparse, textwrap

parser = argparse.ArgumentParser(
    description=textwrap.dedent(
        """\
        A python script to fetch submissions and comments using PRAW API
        """
    ),
    usage='Use "python3 %(prog)s -h" for more information',
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "-sc",
    "--submissions_count",
    type=int,
    default=10,
    help="The number of submissions to crawl in the subreddits",
)
parser.add_argument(
    "-st",
    "--submissions_type",
    type=str,
    default="hot",
    help="The submissions type to crawl in the subreddits",
)
parser.add_argument(
    "-tf",
    "--time_filter",
    type=str,
    default="day",
    help="The submissions type to crawl in the subreddits",
)
parser.add_argument(
    "-cc",
    "--comments_count",
    type=str,
    default="32",
    help="The number of MoreComments to crawl in the comments section",
)
parser.add_argument(
    "-op",
    "--output_path",
    type=str,
    default="./output/",
    help="Output path for the processed files",
)
parser.add_argument(
    "-ip",
    "--input_path",
    type=str,
    default="./input/",
    help="Input path for the subreddits_to_crawl file",
)
parser.add_argument(
    "-ifn",
    "--input_file_name",
    type=str,
    default="subreddits_to_crawl.csv",
    help="File containing csv of subreddits to crawl",
)

parser.add_argument(
    "-svt",
    "--save_type",
    type=str,
    default="csv",
    help=textwrap.dedent(
        """\
        Save mode, can be csv, db, dbwi. Defaults to csv.
        csv  - csv file
        db   - db mode with no initialization(tables are expected to exist)
        dbwi - db mode with initialization, tables are created as per the statements in `db_tables["init"] arg variable`"""
    ),
)

feature_parser = parser.add_mutually_exclusive_group(required=False)
feature_parser.add_argument(
    "-c",
    "--comments",
    dest="comments",
    action="store_true",
    help="Flag to switch on the crawling of comments",
)
feature_parser.add_argument(
    "-nc",
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
        print("Please pass a number or None for the --comments_count (-cc) option")
        raise
