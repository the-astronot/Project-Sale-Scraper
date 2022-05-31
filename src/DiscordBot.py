"""
@author: jormungandr1105
@desc: Code for discord bot to notify me of sales
@created: 05/30/2022
"""
import os
import os.path as path
from dotenv import load_dotenv
import requests
import json


class DiscordBot:
	def __init__(self, token, channel):
		self.botToken = token
		self.channelID = channel
		self.baseURL = "https://discordapp.com/api/channels/{}/messages".format(self.channelID)
		self.headers = { "Authorization":"Bot {}".format(self.botToken),
            "User-Agent":"myBotThing (http://some.url, v0.1)",
            "Content-Type":"application/json", }


	def post_message(self, msg):
		POSTedJSON =  json.dumps ( {"content":msg} )
		r = requests.post(self.baseURL, headers = self.headers, data = POSTedJSON)


# Testing
if __name__ == '__main__':
	env_file = path.join(path.dirname(path.dirname(path.abspath(__file__))),"data/.env")
	load_dotenv(env_file)
	bot = DiscordBot(os.getenv("DISCORD_TOKEN"),os.getenv("DISCORD_CHANNEL"))
	bot.post_message("Boot test...")
