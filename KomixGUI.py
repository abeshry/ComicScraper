import sys
from PyQt4 import QtGui
import tkinter as tk
from garfParser import garfParser

class KomixGUI():
	def __init__(self):
		root = tk.Tk()
		self.width = root.winfo_screenwidth()
		self.height = root.winfo_screenheight()
		self.windowWidth = self.width/3
		self.windowHeight = self.height/3
		self.bottomButtonWidth = self.windowWidth/4
		self.bottomButtonHeight = self.windowHeight/5
		self.topHeight = 30


	def setUpWindow(self):
		app = QtGui.QApplication(sys.argv)  
		self.w = QtGui.QWidget()
		#For full screen use: w.setGeometry(0,0, self.width, self.height)
		self.w.setGeometry(self.windowWidth, self.windowHeight, self.windowWidth, self.windowHeight)
		self.w.setWindowTitle('KOMIX')
		self.setUpButtons()
		self.setUpScript()
		self.w.show()

		sys.exit(app.exec_())

	def createButton(self, name, x, y, width, height):
		button = QtGui.QPushButton(name, self.w)
		button.setGeometry(x,y,width,height)
		return button

	def setUpButtons(self):
		btmBtnWidth = self.bottomButtonWidth
		btmBtnHeight = self.bottomButtonHeight
		bottomButtonStyle = "QPushButton {background-color: rgb(66, 184, 221); color: white ;border-radius: 5px; font: bold 14px; border:1px solid #ae4553}"

		newComicButton = self.createButton("New Comic", 0, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		newComicButton.setStyleSheet(bottomButtonStyle)
		prevComicButton = self.createButton("Previous Strip", btmBtnWidth, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		prevComicButton.setStyleSheet(bottomButtonStyle)
		nextComicButton = self.createButton("Next Strip", btmBtnWidth*2, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		nextComicButton.setStyleSheet(bottomButtonStyle)
		randomComicButton = self.createButton("Random Strip", btmBtnWidth*3, self.windowHeight - btmBtnHeight, btmBtnWidth, btmBtnHeight)
		randomComicButton.setStyleSheet(bottomButtonStyle)

	def setUpScript(self):
		pic = QtGui.QLabel(self.w)
		pic.setGeometry(0,self.topHeight,self.windowWidth, self.windowHeight - self.topHeight - self.bottomButtonHeight)
		filename = garfParser().getLatestComic()
		scriptArea = QtGui.QPixmap(filename)
		scriptArea = scriptArea.scaledToHeight(self.windowHeight)
		scriptArea = scriptArea.scaledToWidth(self.windowWidth)
		pic.setPixmap(scriptArea)



def main():
	app = KomixGUI()
	app.setUpWindow()

if __name__ == '__main__':
	main()

