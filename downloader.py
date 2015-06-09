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