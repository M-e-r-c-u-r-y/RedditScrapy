import re

def cleanse_text(columns=None, df_dict=None):
  """In-place modification of the dictonary passed to the function"""
  if columns is not None and df_dict is not None:
    for col in columns:
      data = []
      for el in df_dict[col]:
        temp = re.sub(r'\s{2,}',' ', el.replace(",","[COMMA]")
        .replace("\n", "[NEWLINE]")
        .replace("&#x200B;", " "))
        temp = re.sub(r'\[NEWLINE\]', ' ',temp)
        temp = re.sub(r'\s{2,}',r'[NEWLINE]',temp)
        data.append(temp)
      df_dict[col] = data
  else:
    print("Data passed is not suitable for this function")
  return None


def fetch_submissions(subreddit, reddit, submissions_count):
  return reddit.subreddit(subreddit).hot(limit=submissions_count)

def fetch_comments(submissionObj, reddit, comments_count):
  submission = reddit.submission(id=submissionObj.id)
  submission.comments.replace_more(limit=comments_count)
  return submission.comments.list()

def cleanse_submissions(cleanse_submission_columns, comments, readObjs, submission_columns):
  submissions_df_dict = {col:[] for col in submission_columns}
  submissions_to_crawl = [submission for readObj in readObjs for submission in readObj]
  for submission in submissions_to_crawl:
    for col in submission_columns:
      submissions_df_dict[col].append(getattr(submission,col))
  if comments == False:
    submissions_to_crawl = None
  data = []
  for link in submissions_df_dict['permalink']:
    data.append(f"{'https://www.reddit.com' + link}")
  submissions_df_dict['permalink'] = data
  cleanse_text(cleanse_submission_columns, submissions_df_dict)
  return submissions_df_dict, submissions_to_crawl

def cleanse_comments(cleanse_comments_columns, submission_comments, comment_columns, link_comments_columns):
  comments_df_dict = {col:[] for col in comment_columns}
  for comment in submission_comments:
    for top_level_comment in comment:
      for col in comment_columns:
        comments_df_dict[col].append(getattr(top_level_comment,col))
  for col in link_comments_columns:
    data = []
    if col == 'permalink':
      for el in comments_df_dict[col]:
        data.append(f"{'https://www.reddit.com' + el}")
    elif col == 'parent_id':
      for i,el in enumerate(comments_df_dict[col]):
        if el.split("_")[1] != comments_df_dict['submission'][i]:
          data.append(f"{'/'.join(comments_df_dict['permalink'][i].split('/')[:-2])+ '/' + el.split('_')[1]}")
        else:
          data.append(f"{'/'.join(comments_df_dict['permalink'][i].split('/')[:-2])}")
    elif col == 'submission':
      for i,el in enumerate(comments_df_dict[col]):
        data.append(f"{'/'.join(comments_df_dict['permalink'][i].split('/')[:-2])}")
    comments_df_dict[col] = data

  cleanse_text(cleanse_comments_columns, comments_df_dict)
  return comments_df_dict