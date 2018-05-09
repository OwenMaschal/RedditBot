import praw
import requests
import re
import pathlib
import logging
import urllib.request
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

image_num = int(config.get('DEFAULTS', 'image_num'))
output_location = config.get('DEFAULTS','output_location')
bot_name = config.get('DEFAULTS','bot')
subreddit_name = config.get('DEFAULTS','subreddit')
time_period = config.get('DEFAULTS','time')

# Check if the url has an extension
# (Example: https://imgur.com/fa33.jpg matches)
regex = re.compile('^.*\.[a-z]{3}$')

def setup_praw_logging():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def download_image(submission):
    if not submission.is_self: # Ignore self posts
        try:
            # This line grabs the image from the url
            urllib.request.urlretrieve(submission.url,
                output_location + submission.id + '.jpg')
        except Exception as e:
            print(str(e) + ' at URL: ' + submission.url)

def main():
    # Setup logging and establish bot connection with Reddit
    setup_praw_logging();
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit(subreddit_name)

    # Create an image folder if it doesn't already exist
    pathlib.Path(output_location).mkdir(parents=True, exist_ok=True)

    # Get 'images_to_get' submissions and download the image from each
    for submission in subreddit.top(time_period, limit=image_num):
        download_image(submission)

main()
