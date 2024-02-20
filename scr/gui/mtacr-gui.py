# MTACR - Graphical User Interface
# 
# Author: Anran Wang
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

		# set up workspace folder - this can be considered to be the "root" of the project
		self.workspaceFolder = os.getcwd()+"/"
		self.inputDir = os.getcwd()+"/"
		self.outputDir = os.getcwd()+"/"
		self.configFileName = os.getcwd()+"/"
		
		# central layout
		offset = 0
		gridLayout = QGridLayout()
		# logo area 
		logo = QLabel()
		pixmap = QPixmap('TextAsCorpusRep-Auxiliary-Logo.png')
		logo.setPixmap(pixmap)
		gridLayout.addWidget(logo,offset,0,1,3,alignment=Qt.AlignmentFlag.AlignCenter)
		font = QFont()
		font.setPointSize(20)
		name = QLabel("Multilingual Text As Corpus Repository for Machine Translation of Low-Resource Languages")
		name.setText("<font color=\"#6317dc\">Multilingual </font> <font color=\"#4272ea\">Text </font><font color=\"#e5a93a\">As </font><font color=\"#44922a\">Corpus </font><font color=\"#a83b51\">Repository </font><font>for Machine Translation of Low-Resource Languages</font>")
		name.setFont(font)
		gridLayout.addWidget(name,offset+1,0,1,3,alignment=Qt.AlignmentFlag.AlignCenter)
		
		# purple area
		offset += 2
		selectFolderButton = MyButton("Change Project Location", self.selectFolder, toSetEnabled=True)
		selectFolderButton.setStyleSheet('QPushButton {background-color: '+purple+';}')
		self.folderLabel = QLabel("Current: "+self.workspaceFolder)
		selectInputButton = MyButton("Select Input Directory", self.selectInputDir)
		selectInputButton.setStyleSheet('QPushButton {background-color: '+purple+';}')
		self.inputLabel = QLabel("Current: "+self.workspaceFolder)
		selectOutputButton = MyButton("Select Output Directory", self.selectOutputDir)
		selectOutputButton.setStyleSheet('QPushButton {background-color: '+purple+';}')
		self.outputLabel = QLabel("Current: "+self.workspaceFolder)
		
		gridLayout.addWidget(selectFolderButton,offset,0)
		gridLayout.addWidget(self.folderLabel,offset+1,0)
		gridLayout.addWidget(selectInputButton,offset,1)
		gridLayout.addWidget(self.inputLabel,offset+1,1)
		gridLayout.addWidget(selectOutputButton,offset,2)
		gridLayout.addWidget(self.outputLabel,offset+1,2)

		layout.addLayout(gridLayout)

		# add space
		gridLayout.addWidget(QLabel(""))
		
		# blue area
		offset += 3
		languageLabel = QLabel("Select Target Languages:")
		languageLabel.setStyleSheet('QLabel {background-color: '+blue+';}')
		typeLabel = QLabel("Select Data Types:")
		typeLabel.setStyleSheet('QLabel {background-color: '+blue+';}')
		loadConfigButton = MyButton("Load Config File",self.loadConfig)
		loadConfigButton.setStyleSheet('QPushButton {background-color: '+blue+';}')
		self.configLabel = QLabel("Current: "+self.configFileName)

		gridLayout.addWidget(languageLabel,offset,0)
		gridLayout.addWidget(QLineEdit(placeholderText="German, English, ..."),offset+1,0)
		gridLayout.addWidget(typeLabel,offset,1)
		gridLayout.addWidget(QLineEdit(placeholderText="Word, Sentences, ..."),offset+1,1)
		gridLayout.addWidget(loadConfigButton,offset,2)
		gridLayout.addWidget(self.configLabel,offset+1,2)

		# add space
		gridLayout.addWidget(QLabel(""))

		# yellow area 
		offset += 3
		acquireButton = MyButton("Acquire Data")
		acquireButton.setStyleSheet('QPushButton {background-color: '+yellow+';}')
		cleanButton = MyButton("Clean Data")
		cleanButton.setStyleSheet('QPushButton {background-color: '+yellow+';}')
		transformButton = MyButton("Transform Data")
		transformButton.setStyleSheet('QPushButton {background-color: '+yellow+';}')

		gridLayout.addWidget(QLineEdit(placeholderText="Location (URLs)"),offset,0)
		gridLayout.addWidget(QLineEdit(placeholderText="Mode of Collection"),offset+1,0)
		gridLayout.addWidget(QLineEdit(placeholderText="Exploration Depth"),offset+2,0)
		gridLayout.addWidget(QLineEdit(placeholderText="Error Handling"),offset+3,0)
		gridLayout.addWidget(acquireButton,offset+4,0)

		gridLayout.addWidget(QLineEdit(placeholderText="NLP-Tool 1"),offset,1)
		gridLayout.addWidget(QLineEdit(placeholderText="NLP-Tool 2"),offset+1,1)
		gridLayout.addWidget(QLineEdit(placeholderText="Parameter 1"),offset+2,1)
		gridLayout.addWidget(QLineEdit(placeholderText="Parameter 2"),offset+3,1)
		gridLayout.addWidget(cleanButton,offset+4,1)

		gridLayout.addWidget(QLineEdit(placeholderText="NLP-Tool 1"),offset,2)
		gridLayout.addWidget(QLineEdit(placeholderText="NLP-Tool 2"),offset+1,2)
		gridLayout.addWidget(QLineEdit(placeholderText="Parameter 1"),offset+2,2)
		gridLayout.addWidget(QLineEdit(placeholderText="Parameter 2"),offset+3,2)
		gridLayout.addWidget(transformButton,offset+4,2)

		# add space
		gridLayout.addWidget(QLabel(""))
		
		# green area
		offset += 6
		identifyButton = MyButton("Identify Language")
		identifyButton.setStyleSheet('QPushButton {background-color: '+green+';}')
		alignButton = MyButton("Align Text")
		alignButton.setStyleSheet('QPushButton {background-color: '+green+';}')
		evalButton = MyButton("Evaluate Quality")
		evalButton.setStyleSheet('QPushButton {background-color: '+green+';}')

		gridLayout.addWidget(QLineEdit(placeholderText="Select Identification Tool"),offset,0)
		gridLayout.addWidget(QLineEdit(placeholderText="Confidence Thresholds"),offset+1,0)
		gridLayout.addWidget(QLineEdit(placeholderText="Secondary Languages"),offset+2,0)
		gridLayout.addWidget(QLineEdit(placeholderText="Detail Level of Output"),offset+3,0)
		gridLayout.addWidget(identifyButton,offset+4,0)

		gridLayout.addWidget(QLineEdit(placeholderText="Alignment Method"),offset,1)
		gridLayout.addWidget(QLineEdit(placeholderText="Pivot Language"),offset+1,1)
		gridLayout.addWidget(QLineEdit(placeholderText="Plot Frequencies"),offset+2,1)
		gridLayout.addWidget(QLineEdit(placeholderText="Detail Level of Output"),offset+3,1)
		gridLayout.addWidget(alignButton,offset+4,1)

		gridLayout.addWidget(QLineEdit(placeholderText="Automatic Assessment"),offset,2)
		gridLayout.addWidget(QLineEdit(placeholderText="Generate Potato Task"),offset+1,2)
		gridLayout.addWidget(QLineEdit(placeholderText="Server Setup (Local and Online)"),offset+2,2)
		gridLayout.addWidget(QLineEdit(placeholderText="Post-Process Results"),offset+3,2)
		gridLayout.addWidget(evalButton,offset+4,2)

		# add space
		gridLayout.addWidget(QLabel(""))
		
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
		self.folderLabel.setText("Current: "+self.workspaceFolder)

	def selectInputDir(self) : 
		self.inputDir = QFileDialog.getExistingDirectory(
			self,
			"Choose Input Directory", 
			"${PWD}",
			) + "/"
		self.inputLabel.setText("Current: "+self.inputDir)
	def selectOutputDir(self) : 
		self.outputDir = QFileDialog.getExistingDirectory(
			self,
			"Choose Output Directory", 
			"${PWD}",
			) + "/"
		self.outputLabel.setText("Current: "+self.outputDir)

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
		self.configFileName = self.configFileName[0]
		self.configLabel.setText("Current: "+self.configFileName)

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
	

