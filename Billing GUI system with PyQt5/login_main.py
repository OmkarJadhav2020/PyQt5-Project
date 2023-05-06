from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys
from PyQt5 import QtCore
import os
class UI(QMainWindow):
	"""docstring for UI"""
	def __init__(self):
		super(UI, self).__init__()
		uic.loadUi("login.ui",self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


		self.close_button = self.findChild(QPushButton,'close_it')
		self.close_button.clicked.connect(self.close1)
		self.login = self.findChild(QPushButton,'log_in')
		self.login.clicked.connect(self.open_dash)
		self.user = self.findChild(QLineEdit,'user_name')
		self.passs = self.findChild(QLineEdit,'pass_word')
		self.passs.returnPressed.connect(self.open_dash)
		self.user.returnPressed.connect(self.next1)
		self.username = 'vijay'
		self.password = '1234'
		self.show()
	def close1(self):
		self.close()
	def open_dash(self):
		if self.user.text() == self.username and self.passs.text() == self.password:
			self.close1()
			os.system('main_dash.py')
		else:
			self.user.setText("")
			self.passs.setText("")
			self.user.setFocus()
			self.user.setPlaceholderText("Incorrect Username")
			self.passs.setPlaceholderText("Incorrect Password")
	def next1(self):
		self.passs.setFocus()

app = QApplication(sys.argv)
win = UI()
app.exec_()