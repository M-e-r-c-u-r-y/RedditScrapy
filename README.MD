# ScrapeReddit

ScrapeReddit is a Python library for extracting post data from reddit.
It uses ``praw 6.5.1``.

## Configuration

Configure the ``.ini`` file as per the instructions in [praw ini file configuration](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html).

``./input/`` folder must contain ``subreddits_to_crawl.csv`` file which holds the subreddit names to crawl. I've made it such that it can be multi lined so that you can choose to make multi line entries instead of a single line.

``./output/`` folder is where the output csv files are saved to.

``[COMMA] and [NEWLINE]`` are used to denote `,` and `\n` respectively so as to not interfere with saving as csv.

## Usage

Example to get 5 hot posts in each subreddit and their comments

```run.py --submissions_count=5```

Example to get 5 hot posts in each subreddit but not their comments

```run.py --submissions_count=5 --no-comments```

Example to get 5 hot posts in each subreddit and upto 5 [MoreComments](https://praw.readthedocs.io/en/latest/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest.replace_more) in the comments

```run.py --submissions_count=5 --comments_count=5```

Example to get 5 hot posts in each subreddit but all their comments with MoreComments set to ``None``

```run.py --submissions_count=5 --comments_count=None```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)