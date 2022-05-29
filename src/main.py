"""
@author: jormungandr1105
@desc: main launcher for sale scraper
@created: 05/27/2022
"""
import os
import os.path as path
import praw
from dotenv import load_dotenv


def startup():
	env_file = path.join(path.dirname(path.dirname(path.abspath(__file__))),"data/.env")
	load_dotenv(env_file)
	reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('SECRET'), user_agent=os.getenv('USER_AGENT'))
	hot_posts = reddit.subreddit('homelabsales').new(limit=10)
	for post in hot_posts:
		#print(post.title, post.selftext, post.url)
		print(post.title)

if __name__ == '__main__':
	startup()
