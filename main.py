import downloadimages
import praw
import requests
import log
import configparser
from datetime import timedelta
from datetime import datetime

def main():
    print('Started.')
    config = configparser.ConfigParser()
    config.read('config.cfg')

    image_num = int(config.get('DEFAULTS', 'image_num'))
    output_location = config.get('DEFAULTS','output_location')
    bot_name = config.get('DEFAULTS','bot')
    subreddit_na    me = config.get('DEFAULTS','subreddit')
    time_period = config.get('DEFAULTS','time')
    log_location = config.get('DEFAULTS', 'log_location')

    logger = log.setup_logging(log_location)
    start = datetime.now()
    logger.debug('Starting...')

    # Setup logging and establish bot connection with Reddit
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit(subreddit_name)

    print('Getting images... please wait...')
    downloadimages.getImages(subreddit, time_period, image_num, output_location)


    end = datetime.now()
    logger.debug('Completed. Time taken: %s', str(end - start))
    print('Completed! The images are stored at \'' + output_location + '\'')

main()
input('Press ENTER to exit')
