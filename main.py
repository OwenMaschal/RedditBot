import praw
import requests
import re
import pathlib
import logging
import urllib.request

images_to_get = 50              # Number of images you want to download
output_location = './img/'      # Image output location. Default: ./img/
bot_name = 'bot1'               # Name of your bot definted in praw.ini
subreddit_name = 'wallpapers'   # Name of subreddit to extract images from
time_period = 'week'

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
            if not regex.match(submission.url):
                # If the link is missing a file extension, add it
                submission.url = submission.url + '.jpg'
            print(submission.id + ': ' +submission.url)
            urllib.request.urlretrieve(submission.url, output_location + submission.id + '.jpg')
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
    for submission in subreddit.top(time_period, limit=images_to_get):
        download_image(submission)

main()
