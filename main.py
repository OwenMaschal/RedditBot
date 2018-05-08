import praw
import requests
import shutil
import re
import json
import pathlib
import logging

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
        with open('./img/' + id,'wb') as out_file:
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
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('wallpapers')

    regex = re.compile('^https://imgur.com/')
    pathlib.Path('./img/').mkdir(parents=True, exist_ok=True)
    for submission in subreddit.top('day', limit=10):
        if regex.match(submission.url): # Is an Imgur link
            request_imgur_image(submission.url)
        else: # Direct image link (i.reddit)
            request_image(submission.url)

main()
