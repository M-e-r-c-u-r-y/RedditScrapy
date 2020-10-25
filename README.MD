# RedditScrapy

RedditScrapy is a Python library for extracting post data from reddit.
It uses `praw 7.1.0`.

## Configuration

Configure the `.ini` file as per the instructions in [praw ini file configuration](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html).

The `--input_path` / `-ip (default: "./input/")` folder must contain the following:

- The `--input_file_name` / `-ifn` is the input csv file which holds the subreddit names to crawl. It can be multi lined entries(for human readability) instead of a single line csv. Default name is `(default: subreddits_to_crawl.csv)`
- `db.sql` file with table definitions. Used when `--save_type` / `-svt` is `dbwi`.
- `arguments.yml` file with the details for what columns to save from the fetched submissions/posts, what columns to convert links of, etc(check the yml file for more info).

The `--output_path` / `-op (default: "./output/")` folder is where the output csv files are saved to if `--save_type` / `-svt (default: csv)` is csv.

`[COMMA] and [NEWLINE]` are used to denote `,` and `\n` respectively so as to not interfere with saving as csv.

To use POSTGRESQL DB to save the data instead of csv file, set environment variable `ASYNCPG_DSN="postgres://user:password@host:port/database?option=value"`

## Usage

Use "python3 run.py -h" for more information

Example to get 5 hot posts in each subreddit and their comments

`python3 run.py --submissions_count 5` or

`python3 run.py -sc 5`

Example to get 5 new posts in each subreddit but not their comments

`python3 run.py --submissions_count 5 --no-comments --submissions_type new` or

`python3 run.py -sc 5 -nc -st new`

Example to get 5 hot posts in each subreddit and upto 5 [MoreComments](https://praw.readthedocs.io/en/latest/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.replace_more) in the comments

`python3 run.py --submissions_count 5 --comments_count 5` or

`python3 run.py -sc 5 -cc 5`

Example to get 5 hot posts in each subreddit and all their comments with MoreComments set to `None`

`python3 run.py --submissions_count 5 --comments_count None` or

`python3 run.py -sc 5 -cc None`

Example to get 5 hot posts in each subreddit and all their comments with MoreComments set to `None` and save to `db`

`python3 run.py --submissions_count 5 --comments_count None --save_type db` or

`python3 run.py -sc 5 -cc None -svt db`

Example to get 5 hot posts in each subreddit and all their comments with MoreComments set to `None` and save to `db` with initialization. i.e., creat the tables as per the sql commands provided in the `db.sql` file

`python3 run.py --submissions_count 5 --comments_count None --save_type dbwi` or

`python3 run.py -sc 5 -cc None -svt dbwi`

## Supported options and defaults

Supported options for `--submissions_count` / `-sc` are:

`integer: (default: 10)`

Supported options for `--submissions_type` / `-st` are:

`string: controversial, hot, new, random_rising, rising, top (default: hot)`

Supported options for `--time_filter` / `-tf` are:

`string: all, day, hour, month, week, year (default: day)`

Supported options for `--comments_count` / `-cc` are:

`integer: (default: 32)`

`string: None`

Use `None` to get all comments as per the details of MoreComments in PRAW api

Supported options for `--output_path` / `-op` are:

`string: (default: "./output/")`

Supported options for `--input_path` / `-ip` are:

`string: (default: "./input/")`

Supported options for `--input_file_name` / `-ifn` are:

`string: (default: "subreddits_to_crawl.csv")`

Supported options for `--save_type` / `-svt` are:

`string: csv, db, dbwi (default: csv)`

Use `--comments` / `-c` or `--no-comments` / `-nc` to fetch or not fetch the accompanying comments for the submission posts

## Sample output

python3 run.py -sc 1000 -cc None -svt dbwi

---

Reddit Read only mode: True

---

Attempting to create tables with the following statements

---

CREATE TABLE IF NOT EXISTS "comments" (
"id" SERIAL NOT NULL PRIMARY KEY,
"permalink" VARCHAR(300) NOT NULL,
"author" VARCHAR(50) NOT NULL,
"score" INT NOT NULL,
"body" VARCHAR(10000) NOT NULL,
"parent_id" VARCHAR(300) NOT NULL,
"submission" VARCHAR(300) NOT NULL,
"created_utc" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
"fetched_utc" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "posts" (
"id" SERIAL NOT NULL PRIMARY KEY,
"permalink" VARCHAR(300) NOT NULL,
"author" VARCHAR(50) NOT NULL,
"score" INT NOT NULL,
"selftext" VARCHAR(40000) NOT NULL,
"title" VARCHAR(300) NOT NULL,
"created_utc" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
"fetched_utc" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

---

CREATE TABLE

---

We will crawl the following subreddits:
['datascience', 'learnpython', 'python']

---

The data we'll pull from submissions is:
['author', 'created_utc', 'permalink', 'score', 'selftext', 'title']

---

Fetching submissions Finished in 0.09349419999853126 seconds
Cleansing submissions Finished in 39.10098529999959 seconds
The data we'll pull from comments is:
['author', 'body', 'created_utc', 'parent_id', 'permalink', 'score',
'submission']

---

Fetching comments Finished in 29.419100099999923 seconds
Cleansing comments Finished in 0.2968255000014324 seconds

---

COPY 23092 executed on comments

---

COPY 2135 executed on posts
Finished in fetching and processing all posts

---

Crawled and Processed 25227 entries in 71.65045810000083 seconds

---

Data is saved into the db

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
