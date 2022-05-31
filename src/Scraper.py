"""
@author: jormungandr1105
@desc:
@created: 05/27/2022

"""
import json
import os.path as path
import praw
from DiscordBot import DiscordBot


data_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"data")


class Scraper:
	def __init__(self, config, reddit):
		self.ready = False
		self.past_posts = {}
		self.reddit = reddit
		if path.exists(path.join(data_path,config)):
			f = open(path.join(data_path,config))
			self.conf = json.load(f)
			f.close()
			if path.exists(path.join(data_path,"notifications.json")):
				f = open(path.join(data_path,"notifications.json"))
				self.notif = json.load(f)
				f.close()
				self.ready = True
			else:
				print("Missing file: \"notifications.json\"")
		else:
			print("Missing file: \"{}\"".format(config))

	def seen_before(self, post):
		if post.id in self.past_posts:
			return True
		return False

	def getXPosts(self, x, sub, bot):
		if self.ready:
			posts = self.reddit.subreddit(sub).new(limit=x)
			for post in posts:
				if not self.seen_before(post):
					self.past_posts[post.id] = True
					value = self.assess_post(post,sub)
					self.assess_value(post,sub,value,bot)

	# Determine score of post
	def assess_post(self, post, sub):
		score = 0.0
		if sub not in self.conf:
			return -1
		sub_dict = self.conf[sub]
		if "require" in sub_dict:
			required = sub_dict["require"]
			for req in required:
				if type(req) == "str":
					if not self.search_for(req,post.title,True):
						return 0
				else:
					if not self.search_or(req,post.title,True):
						return 0
		for point_val in sub_dict:
			if point_val == "require":
				continue
			float_val = float(point_val)
			for keyword in sub_dict[point_val]:
				if type(keyword) == "str":
					if self.search_for(keyword, post.selftext,False):
						score += float_val
				else:
					if self.search_or(keyword, post.selftext,False):
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
		if value >= 100:
			msg = "{0}\n\t{1}\n{2}".format(post.title,post.selftext.replace("\n\n","\n").replace("\n","\n\t"),post.url)
			bot.post_message(msg)
		elif value >= 50:
			msg = "{0}\n{1}".format(post.title,post.url)
			bot.post_message(msg)
	
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
