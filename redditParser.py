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

	def getTitles(self):
		self.download()
		if (self.contents):
			count = 0
			while (count < 501):
				i = 1
				self.download()
				while (i < 51):
					tree = etree.HTML(self.contents)
					redditurl = tree.xpath("string(//*[@id='siteTable']/div["+str(i)+"]/div[2]/p[1]/a)")
					print(redditurl)
					i = i + 2
				pageLast = tree.xpath("string(//*[@id='siteTable']/div[49]/@class)")
				pageLast = pageLast[10:]
				print(pageLast)
				pageLast = pageLast[:9]
				print(pageLast)
				count = count + 25
				self.url = "http://www.reddit.com/r/all/?count="+str(count) + "&after=" + str(pageLast)
				print(self.url)

if __name__ == "__main__":
	if (not os.path.exists ("Reddit")):
		os.mkdir("Reddit")
	test = redditParser()
	#retreive the first 500 pages from reddit.com/r/all
	test.getTitles()