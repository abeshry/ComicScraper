import urllib
import urllib.request
import re
import os
import time
from lxml import etree
from multiprocessing import Pool
from xkcdParser import Downloader
from datetime import timedelta
from datetime import date

class garfParser(Downloader):
	def ___init__(self, url):
		self.url = url
		self.today = ""

	def getToday(self):
		self.download()
		if (self.contents):
			tree = etree.HTML(self.contents)
			imgurl = tree.xpath("string(//*[@id='home_comic']/img/@src)")
			self.today = imgurl.lstrip("htp:/garfield/uos/t.cm").rstrip(".jpg")

	def getStrip(self, date):
		if (self.contents):
			imageFile = open("Garfield Comics/" + self.url.lstrip("http://garfield.com/uploads/strips/"), "wb")
			imageFile.write(self.contents)
			imageFile.close()
			
	def getLatestComic(self):
		self.getToday()
		self.url = "http://garfield.com/uploads/strips/" + self.today + ".jpg"
		self.download(self.url)
		self.getStrip(self.today)

	def getAllComics(self):
		self.getToday()
		response = True
		recentDay = date(int(self.today[:4]),int(self.today[5:7]), int(self.today[8:10]))
		counter = 0
		while (response == True):
			day = (recentDay - timedelta(days=counter))
			self.url = "http://garfield.com/uploads/strips/" + str(day) + ".jpg"
			self.download(self.url)
			self.getStrip(day)
			counter = counter + 1

	def getComicByDate(self, wantedDate):
		comicDate = date(int(wantedDate[:4]),int(wantedDate[5:7]), int(wantedDate[8:10]))
		if (comicDate):
			self.url = "http://garfield.com/uploads/strips/" + str(comicDate)+ ".jpg"
			self.download(self.url)
			self.getStrip(comicDate)

	def getAllMultiProcess(self):
		self.getToday()
		response = True
		recentDay = date(int(self.today[:4]),int(self.today[5:7]), int(self.today[8:10]))
		counter = 0
		pool = Pool(processes = 4)
		while (response == True):
			day = (recentDay - timedelta(days=counter))
			self.url = "http://garfield.com/uploads/strips/" + str(day) + ".jpg"
			self.download(self.url)
			counter = counter + 1
			valuesProcessed =  pool.apply_async(self.getStrip, [str(day)])

if __name__ == "__main__":
	if (not os.path.exists ("Garfield Comics")):
		os.mkdir("Garfield Comics")
	test = garfParser("http://garfield.com")
	test.getAllComics()
	#test.getComicByDate("2015-01-01")
	#test.getAllMultiProcess()