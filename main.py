import datetime, praw

print('Authenticating...')
reddit = praw.Reddit('bot1')
print('Authentication successful!')

subreddit = reddit.subreddit('pythonforengineers')
with open('out.txt', 'a') as f:
    f.write(str(datetime.datetime.now()) + '\n')
    for submission in subreddit.top('day', limit=10):
        f.write('https://www.reddit.com/' + submission.permalink + '\n')
    f.write('\n')# Add a line between commits
