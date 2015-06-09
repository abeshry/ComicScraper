import urllib
import urllib.request
import re
import os
import time
from lxml import etree
from xkcdParser import Downloader
class redditParser(Downloader):

	def __init__(self):
		self.url = "http://reddit.com/r/all"

	def getTitles(self):
		self.download()
		itemArray = []
		if (self.contents):
			#count of titles wanted
			count = 0
			while (count < 50):
				contents = self.contents
				item = redditItem()
				item.retrieveInfo(contents)
				itemArray.append(item)
				tree = etree.HTML(contents)
				count = count + 25
				pageLastID = tree.xpath("string(//*[@id='siteTable']/div[49]/@data-fullname)")
				self.url = "http://www.reddit.com/r/all/?count=" + str(count) + "&after=" + str(pageLastID)
				self.download(self.url)

class redditItem():
	def __init__(self):
		self.title = ""
		self.link = ""
		self.user = ""
		self.date = ""
		self.rank = ""
		self.thumbnail = ""
		self.hasThumbnail = False

	def retrieveInfo(self, info):
		tree = etree.HTML(info)
		i = 1
		while (i < 51):
			self.rank = int((i + 1)/2)
			self.title = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[1]/a)") #recognize symbols/slow down
			self.link = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[1]/a/@href)")
			self.date = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[2]/time/@title)")
			self.user = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[2]/a[1])")
			self.thumbnail = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/a/img/@src)") #CREATE OWN

			if (self.thumbnail != ""):
				self.hasThumbnail = True
			i = i + 2
		return self

if __name__ == "__main__":
	if (not os.path.exists ("Reddit")):
		os.mkdir("Reddit")
	test = redditParser()

	#retreive the first 50 links from reddit.com/r/all
	test.getTitles()