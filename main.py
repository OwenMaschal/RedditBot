import praw

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('UMD')

#for submission in subreddit.hot(limit=10):
