"""
@author: jormungandr1105
@desc: scrapes reddit threads for keywords
@created: 05/27/2022
"""
import json
import time
import os.path as path
import praw
import datetime
from DiscordBot import DiscordBot


data_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"data")


class Scraper:
	def __init__(self, config, reddit):
		self.ready = False
		self.past_posts = {}
		self.reddit = reddit
		self.ready = self.load_keywords(config)
		if not self.ready:
			print("Missing file: \"{}\"".format(config))

	def load_keywords(self,config):
		if path.exists(path.join(data_path,config)):
			f = open(path.join(data_path,config))
			self.conf = json.load(f)
			f.close()
			return True
		return False

	def seen_before(self, post):
		if post.id in self.past_posts:
			return True
		return False

	def purge_old_posts(self):
		for post in self.past_posts:
			# If post is more than 12 hours old, ditch it
			if time.time() - self.past_posts[post] > 43200:
				self.past_posts.pop(post)

	def getXPosts(self, x, sub, bot):
		if self.ready:
			posts = self.reddit.subreddit(sub).new(limit=x)
			for post in posts:
				if not self.seen_before(post):
					self.past_posts[post.id] = time.time()
					value = self.assess_post(post,sub)
					self.assess_value(post,sub,value,bot)

	# Determine score of post
	def assess_post(self, post, sub):
		score = 0.0
		if sub not in self.conf:
			return -1
		sub_dict = self.conf[sub]
		if "require" in sub_dict:
			# If post doesn't contain required keywords,
			# stop processing it
			required = sub_dict["require"]
			for req in required:
				if type(req) == "str":
					if not self.search_for(req,post.title,True):
						return 0
				else:
					if not self.search_or(req,post.title,True):
						return 0
		for point_val in sub_dict:
			# Don't include required towards totals
			if point_val == "require":
				continue
			float_val = float(point_val)
			for keyword in sub_dict[point_val]:
				if type(keyword) == "str":
					if self.search_for(keyword, post.title+post.selftext,False):
						score += float_val
				else:
					if self.search_or(keyword, post.title+post.selftext,False):
						score += float_val
		return score

	# Determine action required from score
	def assess_value(self, post, sub, value, bot):
		if value == -1:
			# Error occurred
			print("Error")
			return
		elif value < 1:
			return
		msg = "[{}]\n".format(str(datetime.datetime.now())[:19])
		if value >= 100:
			msg += "{0}\n\t{1}\n{2}".format(post.title,post.selftext.replace("\n\n","\n").replace("\n","\n\t"),post.url)
			bot.post_message(msg)
		elif value >= 50:
			msg += "{0}\n{1}".format(post.title,post.url)
			bot.post_message(msg.replace("&#x200B;",""))
	
	# Check text for keyword
	def search_for(self, keyword, text, case):
		# Gotta be careful not to have keywords that
		# are too general. Additionally, might be 
		# smart to include spaces on either side of
		# more general keywords, if desired
		if case:
			return (text.find(keyword) != -1)
		return (text.lower().find(keyword.lower()) != -1)

	# Check text for any of several keywords
	def search_or(self, keywords, text, case):
		for keyword in keywords:
			if self.search_for(keyword, text, case):
				return True
		return False


# Testing
if __name__ == '__main__':
	pass
