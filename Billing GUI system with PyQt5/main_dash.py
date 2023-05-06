import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5 import QtCore
import os

class UI(QMainWindow):
	def __init__(self):
		super(UI,self).__init__()
		uic.loadUi("dash_board.ui",self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.log_out = self.findChild(QPushButton,"log_out")
		self.log_out.clicked.connect(self.close_it)
		self.customer_data  = self.findChild(QPushButton,'customer_master_3')
		self.customer_data.clicked.connect(self.customer_func)
		self.prod_mas = self.findChild(QPushButton,'product_master_3')
		self.prod_mas.clicked.connect(self.pro_maa)
		self.show()
	def close_it(self):
		self.close()

	def pro_maa(self):
		self.close()
		os.system("product_main.py")
	def customer_func(self):
		self.close()
		os.system("cus_main.py")

app = QApplication(sys.argv)
win = UI()
app.exec_()