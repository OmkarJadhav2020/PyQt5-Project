from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import os
class UI(QMainWindow):
	def __init__(self):
		super(UI,self).__init__	()
		uic.loadUi("add_pro.ui",self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.data = self.findChild(QLineEdit,'lineEdit_5')
		self.save_button = self.findChild(QPushButton,'pushButton_2')
		self.save_button.clicked.connect(self.add_item_to)
		self.combobox = self.findChild(QComboBox,'comboBox')
		self.combobox.addItem("Plate")
		self.combobox.addItem("Other")
		self.rate = self.findChild(QLineEdit,'lineEdit_6')
		self.show()

	def add_item_to(self):
		conn = sqlite3.connect("customer_database.db")
		c = conn.cursor()
		try:
			c.execute("CREATE TABLE pro(name text,type text ,rate text)")
		except:
			pass
		if self.data.text() != "":
			c.execute(f"INSERT INTO pro VALUES('{self.data.text()}','{self.combobox.currentText()}','{self.rate.text()}')")
			conn.commit()
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Successfull")
			dialog.setText("Product added")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()

		else:
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Warning")
			dialog.setText("Add product name")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()

		self.close()
		os.system("product_main.py")

app = QApplication(sys.argv)
win = UI()

app.exec_()