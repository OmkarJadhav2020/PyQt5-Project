from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import os

items = None
inder = None
class UI(QMainWindow):
	def __init__(self):
		super(UI,self).__init__	()
		uic.loadUi("product_master.ui",self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		self.pro_name = self.findChild(QComboBox,'comboBox_1')
		conn = sqlite3.connect("customer_database.db")
		c = conn.cursor()
		try:

			c.execute("SELECT rowid,* FROM pro")
			data = c.fetchall()
			for item in data:
				self.pro_name.addItem(item[1])

		except:
			pass
		conn.close()
		self.pro_name.activated.connect(self.listarr)
		self.pro_type_combo = self.findChild(QComboBox,'comboBox_3')
		self.date = self.findChild(QDateEdit,'dateEdit')
		self.decr = self.findChild(QLineEdit,'lineEdit_2')
		self.quantity = self.findChild(QLineEdit,'lineEdit_3')
		self.rate = self.findChild(QLineEdit,'lineEdit_4')
		self.dashboard = self.findChild(QPushButton,'pushButton_6')
		self.dashboard.clicked.connect(self.dash)
		self.save = self.findChild(QPushButton,'pushButton')
		self.save.clicked.connect(self.savedata)
		self.delete = self.findChild(QPushButton,'pushButton_2')
		self.update = self.findChild(QPushButton,'pushButton_3')
		self.refresh = self.findChild(QPushButton,'pushButton_4')
		self.refresh.clicked.connect(self.ref)
		self.add_new = self.findChild(QPushButton,'pushButton_5')
		self.add_new.clicked.connect(self.open_dial)
		self.table = self.findChild(QTableWidget,'tB')
		self.table.setColumnCount(7)
		self.pro_type_combo.addItem("Plate")
		self.pro_type_combo.addItem("Other")
		self.date.setDateTime(QtCore.QDateTime.currentDateTime())		
		self.update.clicked.connect(self.update_existing)
		self.table.cellPressed.connect(self.activate)
		self.createtab()
		self.table_setter()
		# self.listarr(None)
		QApplication.instance().focusChanged.connect(self.on_focusChanged)

		self.show()

	def listarr(self,index):
		try:
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute(f"SELECT rowid,* FROM pro WHERE rowid = {index+1}")
			data = c.fetchall()
			print(data)
			self.pro_type_combo.setCurrentText(str(data[0][2]))
			self.rate.setText(data[0][3])
		except:
			self.pro_name.clear()

	def open_dial(self):
		self.close()
		os.system("add_pro_main.py")
	def ref(self):
		self.table_setter()
		self.date.setDateTime(QtCore.QDateTime.currentDateTime())	

	def createtab(self):
		try:
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute("""CREATE TABLE PRODUCTS(pro_name text,pro_type text,dec text,quan int,rate int,datee date)""" )
			conn.commit()
		except:
			pass

	def dash(self):
		self.close()
		os.system("main_dash.py")


	def savedata(self):
		if self.pro_name.currentText() == "" or self.quantity.text() == "" or self.rate.text() == "":
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Warning")
			dialog.setText("Please enter Compulsary field")
			dialog.setIcon(QMessageBox.Warning)
			dialog.exec_()
			self.pro_name.setFocus()
		else:
			prod1 = self.pro_name.currentText()
			protype1 = self.pro_type_combo.currentText()
			dec = self.decr.text()
			quan1 = self.quantity.text()
			rat1 = self.rate.text()
			datenew = self.date.date()
			day = str(datenew.day())
			month = str(datenew.month())
			year = str(datenew.year())
			if len(str(datenew.day())) == 1:
				day = "0" + day
			if len(str(datenew.month())) == 1:
				month = "0" + month
			maii = year+'-'+month+'-'+day
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute(f"INSERT INTO PRODUCTS VALUES('{prod1}','{protype1}' , '{dec}', '{quan1}', '{rat1}' , '{maii}')")
			conn.commit()
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Successfull")
			dialog.setText("Product added")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()
			self.table_setter()	

	def table_setter(self):
		try:
			self.table.clear()
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute("""SELECT rowid FROM PRODUCTS""")
			data = c.fetchall()
			no = data[-1][0]
			self.table.setRowCount(no+1)
			column = 0
			c.execute("""SELECT rowid,* FROM PRODUCTS""")
			data = c.fetchall()
			self.table.setItem(0,0,QTableWidgetItem('ID'))
			self.table.setItem(0,1,QTableWidgetItem('PRODUCT NAME'))

			self.table.setItem(0,2,QTableWidgetItem('PRODUCT TYPE'))

			self.table.setItem(0,3,QTableWidgetItem('DESCRIPTION'))
			self.table.setItem(0,4,QTableWidgetItem('QUANTITY'))
			self.table.setItem(0,5,QTableWidgetItem('RATE'))
			self.table.setItem(0,6,QTableWidgetItem('DATE'))												
			row = 1
			for item in data:
				self.table.setItem(row,column,QTableWidgetItem(str(item[0])))
				self.table.setItem(row,column+1,QTableWidgetItem(str(item[1])))
				self.table.setItem(row,column+2,QTableWidgetItem(str(item[2])))
				self.table.setItem(row,column+3,QTableWidgetItem(str(item[3])))
				self.table.setItem(row,column+4,QTableWidgetItem(str(item[4])))
				self.table.setItem(row,column+5,QTableWidgetItem(str(item[5])))
				self.table.setItem(row,column+6,QTableWidgetItem(str(item[6])))
				row = row + 1

		except:
			self.table.clear()
			self.table.setRowCount(1)
			self.table.setItem(0,0,QTableWidgetItem("ID"))
			self.table.setItem(0,1,QTableWidgetItem('PRODUCT NAME'))
			self.table.setItem(0,2,QTableWidgetItem('PRODUCT TYPE'))
			self.table.setItem(0,3,QTableWidgetItem('DESCRIPTION'))
			self.table.setItem(0,4,QTableWidgetItem('QUANTITY'))
			self.table.setItem(0,5,QTableWidgetItem('RATE'))
			self.table.setItem(0,6,QTableWidgetItem('DATE'))


	def keyPressEvent(self,e):
		if e.key() == 16777223 and QApplication.focusWidget().objectName() == 'tB':
			self.deleter()

		if e.key() == Qt.Key_Down:
			if QApplication.focusWidget().objectName() == 'lineEdit_2':
			 	self.quantity.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_3':
			 	self.rate.setFocus()		
			elif QApplication.focusWidget().objectName() == 'lineEdit_4':
			 	self.save.setFocus()
		if e.key() == Qt.Key_Up:
			if QApplication.focusWidget().objectName() == "lineEdit_2":
				self.pro_name.setFocus()
			elif QApplication.focusWidget().objectName() == "lineEdit_3":
				self.decr.setFocus()
			elif QApplication.focusWidget().objectName() == "lineEdit_4":
				self.quantity.setFocus()
	
	def deleter(self):
		try:
			dialog = QMessageBox.question(self,'PyQt5 message', "Do you want to delete this item?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if dialog == QMessageBox.Yes:
				conn = sqlite3.connect("customer_database.db")
				c = conn.cursor()
				c.execute(f"DELETE FROM PRODUCTS WHERE rowid = {inder}")
				conn.commit()
				self.table_setter()
			elif dialog == QMessageBox.No:
				print("No")
		except:
			print("error")
		
		


	def on_focusChanged(self):
		# pass
		fwidget = QApplication.focusWidget()
		if fwidget is not None:
			print(fwidget.objectName())


	def update_existing(self):

		if self.pro_name.currentText() == "" or self.quantity.text() == "":
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Warning")
			dialog.setText("Enter Product name and quantity")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()
		
		else:
			try:
				conn = sqlite3.connect("customer_database.db")
				c = conn.cursor()
				datenew = self.date.date()
				day = str(datenew.day())
				month = str(datenew.month())
				year = str(datenew.year())
				if len(str(datenew.day())) == 1:
					day = "0" + day
				if len(str(datenew.month())) == 1:
					month = "0" + month
				maii = year+'-'+month+'-'+day
	
				c.execute(f"UPDATE PRODUCTS SET pro_name = '{self.pro_name.currentText()}' ,pro_type = '{self.pro_type_combo.currentText()}' ,dec = '{self.decr.text()}' ,quan = '{self.quantity.text()}' ,rate = '{self.rate.text()}', datee = '{maii}' where rowid = {items[0]}")
				conn.commit()
				self.table_setter()
				dialog = QMessageBox(self)
				dialog.setWindowTitle("Updated")
				dialog.setText("Record updated successfully")
				dialog.setIcon(QMessageBox.Information)
				dialog.exec_()
			except:
				dialog = QMessageBox(self)
				dialog.setWindowTitle("Updated")
				dialog.setText("Record doesn't exist or select item from table")
				dialog.setIcon(QMessageBox.Information)
				dialog.exec_()

	def activate(self,index):
		global inder
		try:
			inder = int(self.table.currentItem().text())
		except:
			dialog = QMessageBox(self)
			dialog.setWindowTitle("ID")
			dialog.setText("Please Select Id")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()
		try:
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()

			c.execute(f"SELECT rowid,* FROM PRODUCTS WHERE rowid = {self.table.currentItem().text()}")
			data = c.fetchall()
			item = data[0]
			self.pro_name.setCurrentText(str(item[1]))
			self.pro_type_combo.setCurrentText(str(item[2]))
			self.decr.setText(str(item[3]))
			self.quantity.setText(str(item[4]))
			self.rate.setText(str(item[5]))
			global items
			items = item
	
			new = item[6]
			qdate = QtCore.QDateTime.fromString(new,'yyyy-MM-dd')
			self.date.setDateTime(qdate)	
		except:
			pass

app = QApplication(sys.argv)
win = UI()

app.exec_()