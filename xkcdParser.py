#A simple scraper that downloads xkcd comics from the xkcd website
#allows for random, most recent, or all comic downloads

import urllib
import urllib.request
import re
import os
import random
import threading
from queue import Queue
from lxml import etree
from PIL import Image, ImageFont, ImageDraw

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
			browser = urllib.request.urlopen(self.imgurl)
			if (response == 200):
				self.imgContents = browser.read()

			imageName = re.sub(r'[^\w]', ' ', imageName)
			imageFile = open("xkcd Comics/" +imageName + ".png", "wb")
			imageFileName = ("xkcd Comics/" +imageName + ".png")
			imageFile.write(self.imgContents)
			imageFile.close()

			img = Image.open(imageFileName)
			(width, height) = img.size
			draw = ImageDraw.Draw(img)
			font = ImageFont.truetype("Quand_tu_dors_.otf", 26)
			draw.text((5, height - 26), self.title, fill = "red", font=font)
			img.save(imageFileName)

class xkcdParser(Downloader):

	def __init__(self, url):
		Downloader.__init__(self, url)
		self.latestComic = None
		self.title = ""
		self.imgContents = ""
		self.caption = ""
		self.status = ""
		self.imgurl = ""
		self.threads = []
		self.q = Queue()

	def getLatest(self):
		try:
			self.latestComic = re.search(b"http://xkcd.com/(\d+)", self.contents).group(1)
			self.latestComic = int(self.latestComic)
		except:
			self.latestComic = None

	def getCurrent(self):
		self.download(self.url)
		self.getLatest()
		self.getTitle()
		self.getCaption()
		self.getImage()

	def getRandom(self):
		if (self.latestComic != 0):
			comicNumber = random.randint(1, self.latestComic)
			self.url = "http://xkcd.com/" + str(comicNumber)
			self.download(self.url)
			self.getTitle()
			self.getCaption()
			self.getImage()

	def getAll(self):
		self.download(self.url)
		self.getLatest()
		if (self.latestComic != 0):
			for x in range(1,self.latestComic):
				try:
					self.url = "http://xkcd.com/" + str(x)
					self.download(self.url)
					self.getTitle()
					self.getCaption()
					self.getImage()
					print(self.title)
				except:
					print("Error in: " + self.url)


	def multiThreadWork(self):	
		while (self.q.qsize() > 0):
			self.url = self.q.get()	
			self.q.task_done()
			self.download(self.url)
			self.getTitle()
			self.getImage()
			

	def getAllMultiThreaded(self):
		self.getLatest()
		for x in range(1, self.latestComic):
			self.q.put("http://xkcd.com/" + str(x))

		for y in range(0, 8):
			thread = threading.Thread(target = self.multiThreadWork)
			thread.daemon = True
			self.threads.append(thread)
		
		for t in self.threads:
			t.start()

		for t in self.threads:
			t.join()

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
	parser.getAll()

	#Returns a every comic from beginning to date with multithreading
	#parser.getAllMultiThreaded()
	#print("done")

	#Prints the comic number, title and caption
	# print (parser.latestComic)
	# print (parser.title)
	# print (parser.caption)