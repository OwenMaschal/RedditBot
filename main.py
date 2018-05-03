import praw, requests, shutil, re, json, pathlib

def request_imgur_image(file_url):
    regex2 = re.compile('^https://imgur.com/a/([a-zA-Z0-9]*)$')
    m = regex2.match(file_url)
    if m:
        #print('This is an album! We are going to ignore these for now.')
    else: # This is a single image
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

def main():
    #print('Authenticating...')
    reddit = praw.Reddit('bot1')
    #print('Authentication successful!')
    subreddit = reddit.subreddit('wallpapers')
    regex = re.compile('^https://imgur.com/')
    pathlib.Path('./img/').mkdir(parents=True, exist_ok=True)
    for submission in subreddit.top('day', limit=10):
        #print(submission.url)
        if regex.match(submission.url):
            request_imgur_image(submission.url)
        else: # Direct image link
           request_image(submission.url)

main()
