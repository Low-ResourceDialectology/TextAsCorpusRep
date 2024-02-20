# StudyToolkitVid - Graphical User Interface
# 
# Authors: Christian Schuler & Dominik Hauser & Anran Wang
################################################################################

import sys, os 
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtMultimedia import *

# helper class for buttons in the video editing window
class MyButton(QPushButton) : 
	def __init__(self, text="", function=None, toAppend=[], toSetEnabled=True) : 
		super(QPushButton, self).__init__()
		self.setEnabled(toSetEnabled)
		self.setText(text)
		if not function == None: 
			self.clicked.connect(function)
		toAppend.append(self)

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		MyMenu(self, "MTACR")

		self.setWindowTitle("MTACR")
		self.setMinimumSize(QSize(600,400))

		# color palette 
		blue = "#A7C4E6"
		yellow = "#EEE4BC"
		purple = "#BD9FFA"
		green = "#AEC69A"
		pink = "#E8BECC"

		layout = QVBoxLayout()
		# help button
		question = QIcon(QPixmap('question.png'))
		helpButton = MyButton(function=self.help)# function=self.popMsg("github")
		helpButton.setIcon(question)
		helpButton.setFixedSize(20,30)
		layout.addWidget(helpButton,alignment=Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)
		# logo
		logo = QLabel()
		pixmap = QPixmap('TextAsCorpusRep-Auxiliary-Logo.png')
		logo.setPixmap(pixmap)
		layout.addWidget(logo,alignment=Qt.AlignmentFlag.AlignCenter)

		# set up workspace folder - this can be considered to be the "root" of the project
		self.workspaceFolder = "."
		self.inputDir = "."
		self.outputDir = "."

		selectFolderButton = MyButton("Change Project Location", self.selectFolder, toSetEnabled=True)
		selectFolderButton.setStyleSheet('QPushButton {background-color: '+purple+';}')
		selectInputButton = MyButton("Select Input Directory", self.selectInputDir)
		selectInputButton.setStyleSheet('QPushButton {background-color: '+purple+';}')
		selectOutputButton = MyButton("Select Output Directory", self.selectOutputDir)
		selectOutputButton.setStyleSheet('QPushButton {background-color: '+purple+';}')
		# layout.addWidget(selectFolderButton,0,0,1,2,alignment=Qt.AlignmentFlag.AlignCenter)

		# parameters
		# paramLayout = QGridLayout()
		# requires n*m matrix
		# parameters = ["Language", "Data Type", "Input Directory", "Parameter 4"]
		# for i in range(0,len(parameters)) : 
		# 	for j in range(0,len(parameters[0])) : 
		# 		paramLayout.addWidget(QLabel(parameters[i][j]+": "),i*2,j)
		# 		paramLayout.addWidget(QLineEdit(placeholderText=parameters[i][j]), i*2+1,j)
		# layout.addLayout(paramLayout,1,0,2,2,alignment=Qt.AlignmentFlag.AlignCenter)
		# layout area, first line
		lineLayout1 = QHBoxLayout()
		lineLayout1.addWidget(selectFolderButton)
		lineLayout1.addWidget(selectInputButton)
		lineLayout1.addWidget(selectOutputButton)
		layout.addLayout(lineLayout1)
		lineLayout15 = QHBoxLayout()
		lineLayout15.addWidget(QLabel("Language:"))
		lineLayout15.addWidget(QLineEdit(placeholderText="German, English, ..."))
		lineLayout15.addWidget(QLabel("Data Type:"))
		lineLayout15.addWidget(QLineEdit(placeholderText="Word, Sentences, ..."))
		layout.addLayout(lineLayout15)

		lineLayout2 = QHBoxLayout()
		# functional buttons
		loadConfigButton = MyButton("Load Config File")
		loadConfigButton.setStyleSheet('QPushButton {background-color: '+blue+';}')
		acquireButton = MyButton("Acquire Data")
		acquireButton.setStyleSheet('QPushButton {background-color: '+yellow+';}')
		transformButton = MyButton("Transform&Clean Data")
		transformButton.setStyleSheet('QPushButton {background-color: '+yellow+';}')
		identifyButton = MyButton("Identify Language")
		identifyButton.setStyleSheet('QPushButton {background-color: '+green+';}')
		alignButton = MyButton("Align Text")
		alignButton.setStyleSheet('QPushButton {background-color: '+green+';}')
		evalButton = MyButton("Evaluate Quality")
		evalButton.setStyleSheet('QPushButton {background-color: '+green+';}')

		lineLayout2.addWidget(loadConfigButton)
		lineLayout2.addWidget(acquireButton)
		lineLayout2.addWidget(transformButton)
		layout.addLayout(lineLayout2)
		lineLayout25 = QHBoxLayout()
		lineLayout25.addWidget(identifyButton)
		lineLayout25.addWidget(alignButton)
		lineLayout25.addWidget(evalButton)
		layout.addLayout(lineLayout25)

		# save to config file button
		# saveConfigButton = MyButton("Save as .config File", self.saveConfig)
		# layout.addWidget(saveConfigButton,3,0,1,2,alignment=Qt.AlignmentFlag.AlignCenter)

		# column number of the right part
		# rightLayout = QVBoxLayout()

		# # load config file
		# loadButton = MyButton("Load .config File", self.loadConfig)
		# rightLayout.addWidget(loadButton)
		# # make space 
		# rightLayout.addWidget(QLabel(""))
		# # download files
		# rightLayout.addWidget(MyButton("Download Files", self.download))
		# # process files
		# rightLayout.addWidget(MyButton("Process Files", self.process))
		# # align files
		# rightLayout.addWidget(MyButton("Align Files", self.align))

		# layout.addLayout(rightLayout,0,2,5,1,alignment=Qt.AlignmentFlag.AlignCenter)


		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

	def help(self) : 
		msg = QMessageBox()
		msg.setText("For more information, please check our GitHub page:\n\n https://github.com/Low-ResourceDialectology/TextAsCorpusRep")
		msg.exec()
	# select workspace folder
	def selectFolder(self) : 
		self.workspaceFolder = QFileDialog.getExistingDirectory(
			self,
			"Choose Workspace Directory", 
			"${PWD}",
			) + "/"
	def selectInputDir(self) : 
		self.workspaceFolder = QFileDialog.getExistingDirectory(
			self,
			"Choose Input Directory", 
			"${PWD}",
			) + "/"
	def selectOutputDir(self) : 
		self.workspaceFolder = QFileDialog.getExistingDirectory(
			self,
			"Choose Output Directory", 
			"${PWD}",
			) + "/"

	# pop an error message 
	def popMsg(self, msg) : 
		self.msgBox = QMessageBox()
		self.msgBox.setText(msg)
		self.msgBox.exec()

	# save config file
	def saveConfig(self) : 
		configPath = QFileDialog.getSaveFileName(self,"Save config file", self.workspaceFolder)
		# TODO: save config file
	
	# load config file
	def loadConfig(self) : 
		self.configFileName = QFileDialog.getOpenFileName(
			self,
			"Open File",
			self.workspaceFolder,
			"All Files (*);; Python Files (*.py);; PNG Files (*.png)",
		)
		# TODO: load config file

	# download files
	def download(self) : 
		pass
	# process files
	def process(self) : 
		pass
	# align files
	def align(self) : 
		pass


# menu bars
def MyMenu(self, name) : 
	bar = self.menuBar() 
	tk = bar.addMenu(name)
	save = QAction("Close",self)
	save.setShortcut("Ctrl+W")
	tk.addAction(save)
	quit = QAction("Quit",self) 
	tk.triggered[QAction].connect(self.close)


################## main stream of the program #################
def main():
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	# app.setActiveWindow(window)
	# window.activateWindow()

	# check if project folder is empty
	path = "../projects"
	try : 
		dir = os.listdir(path) 
	except FileNotFoundError : 
		dir = []
	# if empty them pop up a window asking whether to set up examples
	# if len(dir) == 0 or len(dir) == 1 and dir[0] == ".DS_Store": # .ds_store is always there for macos
	# 	msgBox=QMessageBox()
	# 	msgBox.setText("Set up example project? ")
	# 	msgBox.setInformativeText("Welcome to the StudyToolkitVid! Seems like you are using it for the first time, you can set up an example project to test it out! ")
	# 	no = MyButton("No", toSetEnabled=True)
	# 	msgBox.addButton(no, QMessageBox.ButtonRole.YesRole)
	# 	msgBox.show()

	app.exec()


if __name__ == "__main__":
	main()
	

