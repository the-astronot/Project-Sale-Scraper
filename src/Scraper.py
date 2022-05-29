"""
@author: jormungandr1105
@desc:
@created: 05/27/2022

"""
import json
import os.path as path
import praw


data_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"data")


class Scraper:
	def __init__(self, config, reddit):
		self.ready = False
		self.reddit = reddit
		if path.exists(path.join(data_path,config)):
			f = open(path.join(data_path,config))
			obj = f.read()
			json.load(obj)
			self.ready = True

	def getXPosts(self, x, sub):
		posts = self.reddit.subreddit(sub).new(limit=x)
		for post in posts:
			assess_post(post,sub)

	def assess_post(self, post, sub):
		pass


# Testing
if __name__ == '__main__':
	class_test = Scraper()
