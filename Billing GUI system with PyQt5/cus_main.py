from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import sqlite3
class UI(QMainWindow):
	def __init__(self):
		super(UI,self).__init__()
		uic.loadUi("customer_master.ui",self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.open_dashboard = self.findChild(QPushButton,'open_dash')
		self.open_dashboard.clicked.connect(self.dash)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.lists = self.findChild(QListWidget,'listWidget')
		self.lists.itemActivated.connect(self.get_data)
		self.lists.hide()
		self.ID = self.findChild(QLineEdit,'lineEdit')
		self.cusName = self.findChild(QLineEdit,'lineEdit_2')
		self.cusName.textChanged.connect(self.list_widgets)
		self.cusName.returnPressed.connect(self.clost)
		self.conName = self.findChild(QLineEdit,'lineEdit_3')
		self.decr = self.findChild(QLineEdit,'lineEdit_4')
		self.cont1 = self.findChild(QLineEdit,'lineEdit_5')
		self.cont2 = self.findChild(QLineEdit,'lineEdit_6')
		self.add1 = self.findChild(QLineEdit,'lineEdit_7')
		self.add2 = self.findChild(QLineEdit,'lineEdit_8')
		self.emailId = self.findChild(QLineEdit,'lineEdit_9')
		self.addharId = self.findChild(QLineEdit,'lineEdit_10')
		self.date = self.findChild(QDateEdit,'dateEdit')
		self.date.setDateTime(QtCore.QDateTime.currentDateTime())
		self.sav = self.findChild(QPushButton,'save')
		self.update1 = self.findChild(QPushButton,'update')
		self.update1.clicked.connect(self.updated)
		self.ref = self.findChild(QPushButton,'refresh')
		self.ref.clicked.connect(self.refsetter)
		self.det = self.findChild(QPushButton,'deleteit')
		self.det.clicked.connect(self.update_existing)
		self.table = self.findChild(QTableWidget,'tb')
		self.table.cellPressed.connect(self.activate)
		##Main Work##
		self.cusName.setFocus()
		self.sav.clicked.connect(self.save_data)
		QApplication.instance().focusChanged.connect(self.on_focusChanged)
		self.table_set()
		self.set_cus_Id()
		self.show()
	def activate(self):
		# print(self.table.currentRow(),self.table.currentColumn())
		conn = sqlite3.connect("customer_database.db")
		c = conn.cursor()
		c.execute(f"SELECT rowid,* FROM DATA WHERE rowid = {self.table.currentRow()}")
		data = c.fetchall()
		item = data[0]
		self.ID.setText(str(item[0]))
		self.cusName.setText(str(item[1]))
		self.conName.setText(str(item[2]))
		self.decr.setText(str(item[3]))
		self.cont1.setText(str(item[4]))
		self.cont2.setText(str(item[5]))
		self.add1.setText(str(item[6]))
		self.add2.setText(str(item[7]))
		self.emailId.setText(str(item[8]))
		self.addharId.setText(str(item[9]))
		new = item[10]
		qdate = QtCore.QDateTime.fromString(new,'yyyy-MM-dd')
		self.date.setDateTime(qdate)	
		self.lists.hide()	
	def refsetter(self):
		self.set_cus_Id()
		self.cusName.setFocus()
		self.date.setDateTime(QtCore.QDateTime.currentDateTime())
		self.table_set()

	def updated(self):
		if self.cusName.text() == '':			
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Warning")
			dialog.setText("Please enter Customer name.")
			dialog.setIcon(QMessageBox.Warning)
			dialog.exec_()
			self.cusName.setFocus()
		else:
			try:
				conn = sqlite3.connect("customer_database.db")
				c = conn.cursor()
				c.execute(f"SELECT rowid,* FROM DATA WHERE cus_name LIKE '{self.cusName.text()}'")
				data = c.fetchall()
				item = data[0]
				self.ID.setText(str(item[0]))
				self.cusName.setText(str(item[1]))
				self.conName.setText(str(item[2]))
				self.decr.setText(str(item[3]))
				self.cont1.setText(str(item[4]))
				self.cont2.setText(str(item[5]))
				self.add1.setText(str(item[6]))
				self.add2.setText(str(item[7]))
				self.emailId.setText(str(item[8]))
				self.addharId.setText(str(item[9]))
				new = item[10]
				qdate = QtCore.QDateTime.fromString(new,'yyyy-MM-dd')
				self.date.setDateTime(qdate)

				# self.date.setDateTextFormat()
				# self.date.setSelectedDate(dates)
				# self.date.setDateTime(int(date1),int(mon1),int(year1))
			except:
				dialog = QMessageBox(self)
				dialog.setWindowTitle("Warning")
				dialog.setText("Record Doesn't Exist")
				dialog.setIcon(QMessageBox.Warning)
				dialog.exec_()
				self.cusName.setFocus()
	def table_set(self):
		try:
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute("""SELECT rowid FROM DATA""")
			data = c.fetchall()
			no = data[-1][0]
			self.table.setColumnCount(11)
			self.table.setRowCount(no+1)
			column = 0
			c.execute("""SELECT rowid,* FROM DATA""")
			data = c.fetchall()
			self.table.setItem(0,0,QTableWidgetItem('ID'))
			self.table.setItem(0,1,QTableWidgetItem('CUSTOMER NAME'))

			self.table.setItem(0,2,QTableWidgetItem('CONTRACTOR NAME'))

			self.table.setItem(0,3,QTableWidgetItem('DESCRIPTION'))
			self.table.setItem(0,4,QTableWidgetItem('CONTACT 1'))
			self.table.setItem(0,5,QTableWidgetItem('CONTACT 2'))
			self.table.setItem(0,6,QTableWidgetItem('ADDRESS 1'))
			self.table.setItem(0,7,QTableWidgetItem('ADDRESS 2'))	
			self.table.setItem(0,8,QTableWidgetItem('EMAIL ID'))
			self.table.setItem(0,9,QTableWidgetItem('AADHAR'))
			self.table.setItem(0,10,QTableWidgetItem('DATE'))													
			# print(data[0])
			for i in range(1,no+1):
				self.table.setItem(i,column,QTableWidgetItem(str(data[i-1][0])))
				self.table.setItem(i,column+1,QTableWidgetItem(str(data[i-1][1])))
				self.table.setItem(i,column+2,QTableWidgetItem(str(data[i-1][2])))
				self.table.setItem(i,column+3,QTableWidgetItem(str(data[i-1][3])))
				self.table.setItem(i,column+4,QTableWidgetItem(str(data[i-1][4])))
				self.table.setItem(i,column+5,QTableWidgetItem(str(data[i-1][5])))
				self.table.setItem(i,column+6,QTableWidgetItem(str(data[i-1][6])))
				self.table.setItem(i,column+7,QTableWidgetItem(str(data[i-1][7])))
				self.table.setItem(i,column+8,QTableWidgetItem(str(data[i-1][8])))
				self.table.setItem(i,column+9,QTableWidgetItem(str(data[i-1][9])))
				self.table.setItem(i,column+10,QTableWidgetItem(str(data[i-1][10])))

		except:
		 	pass		

	def on_focusChanged(self):
		# pass
		fwidget = QApplication.focusWidget()
		if fwidget is not None:
			print(fwidget.objectName())
	def keyPressEvent(self,e):
		if e.key() == Qt.Key_Down:
			 if QApplication.focusWidget().objectName() == 'lineEdit_2':
			 	self.lists.setFocus()
		if e.key() == Qt.Key_Down:
			if QApplication.focusWidget().objectName() == 'lineEdit_2':
			 	self.conName.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_3':
			 	self.decr.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_4': 
				self.cont1.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_5': 
				self.cont2.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_6': 
				self.add1.setFocus()			
			elif QApplication.focusWidget().objectName() == 'lineEdit_7': 
				self.add2.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_8': 
				self.emailId.setFocus()			
			elif QApplication.focusWidget().objectName() == 'lineEdit_9': 
				self.addharId.setFocus()				
			elif QApplication.focusWidget().objectName() == 'lineEdit_10': 
				self.date.setFocus()	
		if e.key() == Qt.Key_Up:
			if QApplication.focusWidget().objectName() == 'lineEdit_3':
				self.cusName.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_4':
				self.conName.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_5':
				self.decr.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_6':
				self.cont1.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_7': 
				self.cont2.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_8': 
				self.add1.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_9': 
				self.add2.setFocus()
			elif QApplication.focusWidget().objectName() == 'lineEdit_10': 
				self.emailId.setFocus()				

	def get_data(self):
		self.cusName.setText(self.lists.currentItem().text())
		self.lists.hide()
		self.cusName.setFocus()
	def clost(self):
		self.lists.close()
	def list_widgets(self):
		if self.cusName.text() == "":
			self.lists.clear()
		else:
			self.lists.show()
			self.lists.clear()
		conn = sqlite3.connect("customer_database.db")
		c = conn.cursor()
		c.execute(f"""SELECT * FROM DATA WHERE cus_name LIKE '%{self.cusName.text()}%'""")
		data = c.fetchall()
		if data == []:
			self.lists.hide()
		else:
			for item in data:
					self.lists.addItem(item[0])
	def save_data(self):
		if self.cusName.text() == "" or self.cont1.text() == "":
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Warning")
			dialog.setText("Please enter Customer name and contact no to save.")
			dialog.setIcon(QMessageBox.Warning)
			dialog.exec_()
			self.cusName.setFocus()
		else:
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute(f"SELECT rowid,* FROM DATA WHERE cus_name LIKE '{self.cusName.text()}'")
			data = c.fetchall()
			# print(data)
			if data == []:
				datenew = self.date.date()
				day = str(datenew.day())
				month = str(datenew.month())
				year = str(datenew.year())
				if len(str(datenew.day())) == 1:
					day = "0" + day
				if len(str(datenew.month())) == 1:
					month = "0" + month
				maii = year+'-'+month+'-'+day


				c.execute(f"INSERT INTO DATA VALUES('{self.cusName.text()}','{self.conName.text()}','{self.decr.text()}','{self.cont1.text()}','{self.cont2.text()}','{self.add1.text()}','{self.add2.text()}','{self.emailId.text()}','{self.addharId.text()}','{maii}')")
				conn.commit()
				dialog = QMessageBox(self)
				dialog.setWindowTitle("Warning")
				dialog.setText("Customer added to database")
				dialog.setIcon(QMessageBox.Information)
				dialog.exec_()
				self.set_cus_Id()
				self.table_set()

			else:
				dialog = QMessageBox(self)
				dialog.setWindowTitle("Warning")
				dialog.setText("Customer with same name exist")
				dialog.setIcon(QMessageBox.Information)
				dialog.exec_()
			c.execute("SELECT * FROM DATA ORDER BY datee")
			items = c.fetchall()
			# for i in items:
				# print(i)
	def update_existing(self):
		if self.cusName.text() == "":
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Warning")
			dialog.setText("Enter Customer name and then press load and then press update")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()
		else:

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
			c.execute(f"UPDATE DATA SET cus_name = '{self.cusName.text()}' ,con_name = '{self.conName.text()}' ,dec = '{self.decr.text()}' ,contact_1 = '{self.cont1.text()}' ,contact_2 = '{self.cont2.text()}', add1 = '{self.add1.text()}' ,add2 = '{self.add2.text()}' ,email = '{self.emailId.text()}', aadhar = '{self.addharId.text()}',datee = '{maii}' where rowid = {int(self.ID.text())}")
			conn.commit()
			self.table_set()
			dialog = QMessageBox(self)
			dialog.setWindowTitle("Updated")
			dialog.setText("Record updated successfully")
			dialog.setIcon(QMessageBox.Information)
			dialog.exec_()
	def set_cus_Id(self):
		try:
			conn = sqlite3.connect("customer_database.db")
			c = conn.cursor()
			c.execute("""CREATE TABLE DATA(cus_name text,con_name text,dec text,contact_1 int,contact_2 int,add1 text,add2 text,email text,aadhar int,datee date)""" )
			conn.commit()
		except:
			pass
		finally:
			conn = sqlite3.connect("customer_database.db")
			c.execute("""SELECT rowid FROM DATA""")
			data = c.fetchall()
			if data == []:
				self.ID.setText("1")
			else:
				self.ID.setText(str((data[-1][0])+1))
	def dash(self):
		self.close()
		os.system("main_dash.py")


				# c.execute(f"UPDATE DATA SET cus_name = '{self.cusName.text()}' con_name = '{self.conName.text()}' dec = '{self.decr.text()}' contact_1 = '{self.cont1.text()}' contact_2 = '{self.cont2.text()}' add1 = '{self.add1.text()}' add2 = '{self.add2.text()}' email = '{self.emailId.text()}' aadhar = '{self.addharId.text()}' where rowid = {int(self.ID.text())}")
				# conn.commit()
app = QApplication(sys.argv)
win = UI()
app.exec_()