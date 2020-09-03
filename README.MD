# RedditScrapy

RedditScrapy is a Python library for extracting post data from reddit.
It uses ``praw 6.5.1``.

## Configuration

Configure the ``.ini`` file as per the instructions in [praw ini file configuration](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html).

``./input/`` folder must contain ``subreddits_to_crawl.csv`` file which holds the subreddit names to crawl. I've made it such that it can be multi lined so that you can choose to make multi line entries instead of a single line.

``./output/`` folder is where the output csv files are saved to.

``[COMMA] and [NEWLINE]`` are used to denote `,` and `\n` respectively so as to not interfere with saving as csv.

## Usage

Example to get 5 hot posts in each subreddit and their comments

```run.py --submissions_count=5```

Example to get 5 new posts in each subreddit but not their comments

```run.py --submissions_count=5 --no-comments --submissions_type="new"```

Example to get 5 hot posts in each subreddit and upto 5 [MoreComments](https://praw.readthedocs.io/en/latest/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.replace_more) in the comments

```run.py --submissions_count=5 --comments_count=5```

Example to get 5 hot posts in each subreddit but all their comments with MoreComments set to ``None``

```run.py --submissions_count=5 --comments_count=None```

## Supported options and defaults

Supported options for ``--submissions_count`` are:

```integer: (default: 10)```

Supported options for ``--submissions_type`` are:

```string: controversial, hot, new, random_rising, rising, top (default: hot)```

Supported options for ``--time_filter`` are:

```string: all, day, hour, month, week, year (default: day)```

Supported options for ``--comments_count`` are:

```integer: (default: 32)```

```string: None```

Use ``None`` to get all comments as per the details of MoreComments in PRAW api

Supported options for ``--output_path`` are:

```string: (default: "./output/")```

Supported options for ``--input_path`` are:

```string: (default: "./input/")```

Supported options for ``--input_file_name`` are:

```string: (default: "subreddits_to_crawl.csv")```

Use ``--comments`` or ``--no-comments`` to fetch or not fetch the accompanying comments for the submission posts

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)