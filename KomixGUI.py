import sys
from PyQt4 import QtGui
import tkinter as tk
from garfParser import garfParser

class KomixGUI():
	def __init__(self):
		root = tk.Tk()
		garfield = garfParser()
		self.width = root.winfo_screenwidth()
		self.height = root.winfo_screenheight()
		self.windowWidth = self.width
		self.windowHeight = self.height
		self.bottomButtonWidth = self.windowWidth/4
		self.bottomButtonHeight = self.windowHeight/5
		self.topHeight = self.height*0.07
		self.comic = ""
		self.filename = "startImage.png"
		self.count = 0
		self.comics = ["Garfield", "xkcd"]
		self.comicCount = 0

	def setUpWindow(self):
		app = QtGui.QApplication(sys.argv)  
		self.w = QtGui.QWidget()
		self.w.setGeometry(self.windowWidth, self.windowHeight, self.windowWidth, self.windowHeight)
		self.w.setGeometry(0,0, self.width, self.height)
		self.w.setWindowTitle('KOMIX')
		self.w.setStyleSheet("background-color: white")
		self.setUpButtons()
		self.setUpScript()
		self.setUpTop()
		self.w.show()

		sys.exit(app.exec_())

	def createButton(self, name, x, y, width, height):
		fontFamily = QtGui.QFontDatabase.addApplicationFont("komikax.ttf")
		fontName = QtGui.QFontDatabase.applicationFontFamilies(fontFamily)[0]
		font = QtGui.QFont(fontName)
		font.setPixelSize(self.bottomButtonHeight * 0.2)
		
		bottomButtonStyle = "QPushButton {background-color: #e74c3c; color: white; border-radius: 0px; font: bold; border:1px solid #fff}\
							QPushButton:hover {background-color: #2472a4;}"

		button = QtGui.QPushButton(name, self.w)
		button.setGeometry(x,y,width,height)
		button.setStyleSheet(bottomButtonStyle)
		button.setFont(font)

		return button

	def newComic(self):
		self.count = (self.count + 1) % len(self.comics)
		self.comic = self.comics[self.count]
		self.comicCount = 0

	def prevComic(self):
		if (self.comicCount > 0):
			self.comicCount = self.comicCount - 1
		else:
			self.comicCount = 0
		self.filename = garfParser().getComicByDate(self.comicCount)
		self.setUpScript()

	def nextComic(self):
		self.comicCount = self.comicCount + 1
		self.filename = garfParser().getComicByDate(self.comicCount)
		self.setUpScript()
	#def randomComic(self):

	def setUpButtons(self):
		btmBtnWidth = self.bottomButtonWidth
		btmBtnHeight = self.bottomButtonHeight
		
		newComicButton = self.createButton("New Comic", 0, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		newComicButton.clicked.connect(self.newComic)
		prevComicButton = self.createButton("Previous Strip", btmBtnWidth, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		prevComicButton.clicked.connect(self.prevComic)
		nextComicButton = self.createButton("Next Strip", btmBtnWidth*2, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		nextComicButton.clicked.connect(self.nextComic)
		randomComicButton = self.createButton("Random Strip", btmBtnWidth*3, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		#randomComicButton.clicked.connect(self.randomComic)

	def setUpScript(self):
		pic = QtGui.QLabel(self.w)
		pic.setGeometry(0,self.topHeight,self.windowWidth, self.windowHeight - self.topHeight - self.bottomButtonHeight)
		scriptArea = QtGui.QPixmap(self.filename)
		scriptArea = scriptArea.scaledToHeight(self.windowHeight)
		scriptArea = scriptArea.scaledToWidth(self.windowWidth)
		pic.setPixmap(scriptArea)
	
	def setUpTop(self):
		fontFamily = QtGui.QFontDatabase.addApplicationFont("komikax.ttf")
		fontName = QtGui.QFontDatabase.applicationFontFamilies(fontFamily)[0]
		font = QtGui.QFont(fontName,self.topHeight/2,QtGui.QFont.Bold,True)

		top = QtGui.QLabel(self.w)
		top.setGeometry(0,0 ,self.windowWidth, self.topHeight)
		top.setStyleSheet("background-color: #2980b9")

		comic = QtGui.QLabel(self.w)
		comic.setStyleSheet("background-color: #2980b9; color: white")
		comic.setFont(font)
		comic.setText("Comic: " + self.comic)

		title = QtGui.QLabel(self.w)
		title.setStyleSheet("background-color: #2980b9; color: white")
		title.setFont(font)
		title.setText(garfParser().getToday())
		width = title.fontMetrics().boundingRect(title.text()).width()
		title.setGeometry(self.width - width - 5, 0, width - 5, self.topHeight - 5)

def main():
	app = KomixGUI()
	app.setUpWindow()

if __name__ == '__main__':
	main()

