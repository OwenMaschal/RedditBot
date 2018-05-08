import praw
import requests
import shutil
import re
import pathlib
import logging

images_to_get = 10              # Number of images you want to download
output_location = './img/'      # Image output location. Default: ./img/
bot_name = 'bot1'               # Name of your bot definted in praw.ini
subreddit_name = 'wallpapers'   # Name of subreddit to extract images from


def request_imgur_image(file_url):
    regex2 = re.compile('^https://imgur.com/a/([a-zA-Z0-9]*)$')
    m = regex2.match(file_url)
    if m: # Imgur Album Link
        print('This is an album! This has not been implemented yet :(.')
    else: # Imgur image link
        request_image(file_url + '.jpg')

def request_image(file_url):
    req = requests.get(file_url, stream=True, timeout=10.0)
    regex_name = re.compile('.*/([a-zA-Z0-9]+(\.[a-zA-Z0-9]{3})?)$')
    id = regex_name.match(file_url).group(1)
    if req.status_code == requests.codes.ok:
        with open(output_location + id, 'wb') as out_file:
            shutil.copyfileobj(req.raw, out_file)
    else:
        req.raise_for_status()

def setup_praw_logging():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def main():
    setup_praw_logging();
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit(subreddit_name)

    regex = re.compile('^https://imgur.com/')
    pathlib.Path(output_location).mkdir(parents=True, exist_ok=True)

    for submission in subreddit.top('day', limit=images_to_get):
        if not submission.is_self: # Ignore self posts
            if regex.match(submission.url): # Is an Imgur link
                request_imgur_image(submission.url)
            else: # Direct image link (i.reddit)
                request_image(submission.url)

main()
