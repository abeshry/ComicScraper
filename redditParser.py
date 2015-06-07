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
					i = i + 2
				pageLast = tree.xpath("string(//*[@id='siteTable']/div[49]/@class)")
				pageLast = pageLast.lstrip("thing d").rstrip(" linkflair linkflair-album odd  link ")
				pageLast = pageLast[1:]
				print(pageLast)
				count = count + 25
				self.url = "http://www.reddit.com/r/all/?count="+str(count) + "&after=" + str(pageLast)	

if __name__ == "__main__":
	if (not os.path.exists ("Reddit")):
		os.mkdir("Reddit")
	test = redditParser()
	#retreive the first 500 pages from reddit.com/r/all
	test.getTitles()

	#test.getComicByDate("2015-01-01")
	#test.getLatestComic()
	#test.getAllMultiProcess()