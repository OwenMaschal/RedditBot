import praw
import requests
import re
import pathlib
import logging
import urllib.request
import configparser
from datetime import timedelta
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.cfg')

image_num = int(config.get('DEFAULTS', 'image_num'))
output_location = config.get('DEFAULTS','output_location')
bot_name = config.get('DEFAULTS','bot')
subreddit_name = config.get('DEFAULTS','subreddit')
time_period = config.get('DEFAULTS','time')
log_location = config.get('DEFAULTS', 'log_location')

# Check if the url has an extension
# (Example: https://imgur.com/fa33.jpg matches)
regex = re.compile('^.*\.[a-z]{3}$')

def setup_logging():
    logger = logging.getLogger('prawcore')
    hdlr = logging.FileHandler(log_location)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def download_image(submission):
    if not submission.is_self: # Ignore self posts
        try:
            # This line grabs the image from the url
            urllib.request.urlretrieve(submission.url,
                output_location + submission.id + '.jpg')
        except Exception as e:
            logger.error('%s at URL: %s', str(e), submission.url)

def main():
    print('Started.')
    logger = setup_logging()
    start = datetime.now()
    logger.debug('Starting...')

    # Setup logging and establish bot connection with Reddit
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit(subreddit_name)

    # Create an image folder if it doesn't already exist
    pathlib.Path(output_location).mkdir(parents=True, exist_ok=True)
    print('Getting images... please wait...')

    # Get 'images_to_get' submissions and download the image from each
    for submission in subreddit.top(time_period, limit=image_num):
        download_image(submission)

    end = datetime.now()
    logger.debug('Completed. Time taken: %s', str(end - start))
    print('Completed! The images are stored at \'' + output_location + '\'')

main()
input('Press ENTER to exit')
