import re
import pathlib
import urllib.request
import logging

def getImages(subreddit, time_period, image_num, output_location):
    logger = logging.getLogger('prawcore')
    # Check if is an imgur link without a file extenstion
    # (Example: https://imgur.com/fa33.jpg matches)
    is_imgur_no_ext = re.compile('^https?://(www\.)?imgur.com/[a-zA-z0-9]+$')

    # Check if the link is an imgur album.
    is_imgur_album = re.compile('^https?://(www\.)?imgur.com/a/')

    # Create an image folder if it doesn't already exist
    pathlib.Path(output_location).mkdir(parents=True, exist_ok=True)

    # Get 'images_to_get' submissions and download the image from each
    for submission in subreddit.top(time_period, limit=image_num):
        if not submission.is_self: # Ignore self posts
            if is_imgur_album.match(submission.url):
                logger.info("Ignored Imgur Album: %s", submission.url)
            if is_imgur_no_ext.match(submission.url):
                submission.url = submission.url + '.jpg'
            try:
                # This line grabs the image from the url
                urllib.request.urlretrieve(submission.url,
                    output_location + submission.id + '.jpg')
            except Exception as e:
                logger.error('%s at URL: %s', e, submission.url)
