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
	def __init__(self, text, function=None, toAppend=[], toSetEnabled=True) : 
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

		# a list for buttons to be clickable after selecting workspace
		self.inactiveButtons = []

		layout = QGridLayout()
		
		# set up workspace folder - this can be considered to be the "root" of the project
		self.workspaceFolder = "."
		selectFolderButton = MyButton("Change Project Location", self.selectFolder, toSetEnabled=True)
		layout.addWidget(selectFolderButton,0,0,1,2,alignment=Qt.AlignmentFlag.AlignCenter)

		# parameters
		paramLayout = QGridLayout()
		# requires n*m matrix
		parameters = [["Parameter 1", "Parameter 2"], ["Parameter 3", "Parameter 4"]]
		for i in range(0,len(parameters)) : 
			for j in range(0,len(parameters[0])) : 
				paramLayout.addWidget(QLabel(parameters[i][j]+": "),i*2,j)
				paramLayout.addWidget(QLineEdit(placeholderText=parameters[i][j]), i*2+1,j)
		
		layout.addLayout(paramLayout,1,0,2,2,alignment=Qt.AlignmentFlag.AlignCenter)

		# save to config file button
		saveConfigButton = MyButton("Save as .config File", self.saveConfig)
		layout.addWidget(saveConfigButton,3,0,1,2,alignment=Qt.AlignmentFlag.AlignCenter)


		# column number of the right part
		rightLayout = QVBoxLayout()

		# load config file
		loadButton = MyButton("Load .config File", self.loadConfig)
		rightLayout.addWidget(loadButton)
		# make space 
		rightLayout.addWidget(QLabel(""))
		# download files
		rightLayout.addWidget(MyButton("Download Files", self.download))
		# process files
		rightLayout.addWidget(MyButton("Process Files", self.process))
		# align files
		rightLayout.addWidget(MyButton("Align Files", self.align))

		layout.addLayout(rightLayout,0,2,5,1,alignment=Qt.AlignmentFlag.AlignCenter)


		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

	# select workspace folder
	def selectFolder(self) : 
		self.workspaceFolder = QFileDialog.getExistingDirectory(
			self,
			"Choose Workspace Directory", 
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
	

