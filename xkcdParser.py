#A simple scraper that downloads xkcd comics from the xkcd website
#allows for random, most recent, or all comic downloads

import urllib
import urllib.request
import re
import os
import random
from lxml import etree

class Downloader():
	
	def __init__(self, url):
		self.url = url
		self.contents = ""

	def download(self, imageName = "",isImage = False):
		browser = urllib.request.urlopen(self.url)
		response = browser.getcode()
		if (response == 200):
			self.contents = browser.read()

		if isImage:
			#must check if there are symbols in name
			imageFile = open("xkcd Comics/" +imageName + ".png", "wb")
			imageFile.write(self.contents)
			imageFile.close()

class xkcdParser(Downloader):

	def __init__(self, url):
		Downloader.__init__(self, url)
		self.latestComic = None
		self.title = ""
		self.caption = ""
		self.status = ""
		self.imgurl = ""

	def getLatest(self):
		try:
			self.latestComic = re.search(b"http://xkcd.com/(\d+)", self.contents).group(1)
			self.latestComic = int(self.latestComic)
		except:
			self.latestComic = None

	def getCurrent(self):
		self.download(self.url)
		self.getLatest()
		parser.getTitle()
		parser.getCaption()
		parser.getImage()

	def getRandom(self):
		if (self.latestComic != 0):
			comicNumber = random.randint(1, self.latestComic)
			self.url = "http://xkcd.com/" + str(comicNumber)
			self.download(self.url)
			parser.getTitle()
			parser.getCaption()
			parser.getImage()

	def getAll(self):
		self.download(self.url)
		self.getLatest()
		if (self.latestComic != 0):
			for x in range(1,self.latestComic):
				try:
					self.url = "http://xkcd.com/" + str(x)
					self.download(self.url)
					parser.getTitle()
					parser.getCaption()
					parser.getImage()
					print(self.title)
				except:
					print("Symbol in name" + self.url)

	def getTitle(self):
		if (self.contents != ""):
			tree = etree.HTML(self.contents)
			self.title = tree.xpath("string(//div[@id='ctitle'])")

	def getCaption(self):
		if (self.contents != ""):
			tree = etree.HTML(self.contents)
			self.caption = tree.xpath("string(//div[@id='comic']/img/@title)")

	def getImage(self):
		if (self.contents != ""):
			tree = etree.HTML(self.contents)
			self.imgurl = tree.xpath("string(//div[@id='comic']/img/@src)")
			self.imgurl = "http://" + self.imgurl[2:]
			self.download(self.title, isImage = True)

if __name__ == "__main__":
	if (not os.path.exists ("xkcd Comics")):
		os.mkdir("xkcd Comics")

	url = "http://xkcd.com/"
	parser = xkcdParser(url)

	#Saves the latest comic
	parser.getCurrent()

	#Saves a random comic to the device
	#parser.getRandom()
	
	#Returns a every comic from beginning to date
	#parser.getAll()


	#Prints the comic number, title and caption
	# print (parser.latestComic)
	# print (parser.title)
		self.download(self.url)
	# print (parser.caption)