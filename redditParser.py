import urllib
import urllib.request
import re
import os
import time
from lxml import etree
from multiprocessing import Pool
from xkcdParser import Downloader

class redditParser(Downloader):
	def __init__(self):
		self.url = "http://reddit.com/r/all"
		self.today = ""
		self.lastID = ""

	def getTitles(self):
		self.download()
		itemArray = []
		if (self.contents):
			#count of titles wanted
			count = 0
			while (count < 50):
				i = 1
				self.download()
				time.sleep(0.1)
				while (i < 51):
					item = redditItem()
					tree = etree.HTML(self.contents)
					item.rank = int((i + 1)/2)
					item.title = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[1]/a)")
					item.link = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[1]/a/@href)")
					item.date = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[2]/time/@title)")
					item.user = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[2]/a[1])")
					item.thumbnail = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/a/img/@src)") #CREATE OWN
					if (item.thumbnail != ""):
						item.hasThumbnail = True
					i = i + 2
					itemArray.append(item)
					print(item.user)

				pageLastID = tree.xpath("string(//*[@id='siteTable']/div[49]/@data-fullname)")

				count = count + 25
				self.url = "http://www.reddit.com/r/all/?count="+str(count) + "&after=" + str(pageLastID)

class redditItem():
	def __init__(self):
		self.title = ""
		self.link = ""
		self.user = ""
		self.date = ""
		self.rank = ""
		self.hasThumbnail = False
		self.thumbnail = ""


if __name__ == "__main__":
	if (not os.path.exists ("Reddit")):
		os.mkdir("Reddit")
	test = redditParser()
	#retreive the first 500 pages from reddit.com/r/all
	test.getTitles()