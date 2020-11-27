from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
import json
from uploadfiletodrive import update_file, upload_file
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QTextEdit, QLabel, QInputDialog, QFileDialog, QListWidgetItem, QListWidget, QTreeWidget, QVBoxLayout, QStackedWidget, QGridLayout, QProgressBar, QListWidget, QTreeWidgetItem, QWidget, QPushButton, QHBoxLayout,QDesktopWidget
import sys
import sip
import time


class Superapp(QWidget):
	def __init__(self,screensize,service,treefileid):
		super().__init__()
		self.requesttre = None
		self.loadedjson = None
		self.listoffiles = []
		self.nowdirectory = "root"
		self.screensize = screensize
		self.service = service
		self.treefileid = treefileid
		self.listofchilds = None
		self.initUI()

	def initUI(self):

		self.setWindowTitle("discoord")
		self.resize(int(self.screensize.width()/2),int(self.screensize.height()/1.1))
		self.layout = QHBoxLayout()
		self.layout = QGridLayout()

		# self.vertrightlay = QVBoxLayout()
		# self.textsendlay = QHBoxLayout()
		self.btn = QPushButton('Bottom')
		self.progress = QProgressBar()
		self.progress.setGeometry(200, 80, 250, 20)
		self.progress.setValue(20)
		self.progress1 = QProgressBar()
		self.progress1.setGeometry(200, 80, 250, 20)
		self.progress1.setValue(0)
		self.waitico = QLabel()
		self.pixmap = QPixmap('waiting.png').scaled(100,100)
		self.waitico.setPixmap(self.pixmap)
		self.tree = QListWidget()
		self.boxe = QStackedWidget()
		self.boxe.addWidget(self.progress1)
		self.boxe.addWidget(self.tree)
		self.boxe.addWidget(self.waitico)
		self.boxe.setCurrentWidget(self.progress1)
		self.megalist = QListWidget()
		self.texttosend = QTextEdit()
		self.timer = QBasicTimer()
		self.step = 0
		self.downloadedbool = 0
		self.status = 0
		self.check = 1
		self.step = 0;
		self.layout.addWidget(self.boxe,1,0,2,1)
		self.layout.addWidget(self.megalist,1,1,1,2)
		self.layout.addWidget(self.texttosend,2,1)
		self.layout.addWidget(self.btn,2,2)
		self.layout.setColumnStretch(0,1)
		self.layout.setColumnStretch(1,4)
		self.layout.setRowStretch(1,10)
		self.layout.setRowStretch(2,1)
		self.btn.clicked.connect(self.showDialog)
		

		self.setLayout(self.layout)
		self.timer.start(100,self)
		self.gettree()
		self.show()

	def loadchildlist(self,parentfold):
		listofchilds = []
		if self.loadedjson[parentfold]['childs'][0]['id'] == '0':
			return []
		for childs in self.loadedjson[parentfold]['childs']:
			buff = []
			buff.append(self.loadedjson[childs['id']]['name'])
			buff.append(self.loadedjson[childs['id']]['id'])
			buff.append(self.loadedjson[childs['id']]['mimeType'])
			buff.append(self.loadedjson[childs['id']]['type'])
			listofchilds.append(buff)
		return listofchilds

	def reloadtree(self):
		with open("wowitwork.json", "r",encoding = 'utf-8') as read_file:
			self.loadedjson = json.load(read_file)
		self.listofchilds = self.loadchildlist(self.nowdirectory)
		self.tree = self.createtree(self.listofchilds)
		self.boxe.addWidget(self.tree)
		self.boxe.setCurrentWidget(self.tree)
		# self.boxe.setCurrentWidget(self.waitico)
			

	def timerEvent(self, e):
		self.progress1.setValue(int(self.status.progress() * 100))
		if self.check:
			if self.downloadedbool:
				self.reloadtree()
				self.check=0

	def testbtn(self):
		self.gettree(self.service,self.treefileid)

	def _on_item_clicked(self,item):
		# print(self.tree.currentRow())
		print( self.listofchilds[self.listofchilds.index(item.text())])
		self.nowdirectory = self.listofchilds[self.listofchilds.index(item.text())][1]
		print("wrf")
		self.reloadtree()
		print(self.nowdirectory)
		


	def createtree(self,childlist):
		listing = QListWidget()
		for i in range(len(childlist)):
			listing.addItem(childlist[i][0])
		listing.itemClicked.connect(self._on_item_clicked)
		self.boxe.addWidget(self.tree)
		self.boxe.setCurrentWidget(self.tree)
		return listing
	
	# def createtree(self,q):
	# 	tree = QTreeWidget ()
	# 	# tree.setFixedWidth(200)
	# 	headerItem  = QTreeWidgetItem()
	# 	item = QTreeWidgetItem()
	# 	for i in range(q):
	# 		parent = QTreeWidgetItem(tree)
	# 		parent.setText(0, "Parent {}".format(i))
	# 		for x in range(5):
	# 			child = QTreeWidgetItem(parent)
	# 			child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
	# 			child.setText(0, "Child {}".format(x))
	# 			child.setCheckState(0, Qt.Unchecked)
	# 	return tree

	def gettree(self):
		self.downloadedbool = 0
		self.status = 0
		self.check = 1
		self.boxe.setCurrentWidget(self.waitico)
		request = self.service.files().get_media(fileId=self.treefileid)
		self.requesttre = io.FileIO('wowitwork.json', 'wb')
		downloader = MediaIoBaseDownload(self.requesttre, request)
		self.status, self.downloadedbool = downloader.next_chunk()

	def procedureupload(self,pathtofile,folder_id,typef):
		if typef == 'file':
			rq = upload_file(self.service,pathtofile,folder_id)
			smalljson = json.load(rq)
			self.loadedjson.update({smalljson['id']:{'id':  smalljson['id'],
													'name': os.path.basename(pathtofile)}})
			with open("wowitwork.json", "w",encoding='utf-8') as write_file:
				json.dump(self.loadedjson, write_file)
			update_file(self.service,self.treefileid,"wowitwork.json")
			
	def showDialog(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
		if fname!=None:
			self.procedureupload(fname,'1LrIMfvoHRwL-g5XrwI3gLfuyaXQ6Dm1u','file')


if __name__ == '__main__':
	# main()

	SCOPES = ['https://www.googleapis.com/auth/drive']
	SERVICE_ACCOUNT_FILE = 'D:/Desing/group0v81-e066441ff3c2.json'
	credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=credentials)
	treefileid = '152xGDISi4m6fyRzuYOjVhaZgknNJQm2I'
	# update_file(service,treefileid,'need.json')
	app = QApplication(sys.argv)
	screen = app.primaryScreen()
	screensize = screen.size()
	ex = Superapp(screensize,service,treefileid)
	sys.exit(app.exec_())