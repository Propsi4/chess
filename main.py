from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QTableWidgetItem,QMainWindow,QTableWidget
from PyQt6.QtGui import QColor
import sys
allowed = ('П','Т','К','С','Ф','Кр','п','т','к','с','ф','кр','КР')
class App(QMainWindow):
	def __init__(self):
		super(App, self).__init__()
		uic.loadUi('main.ui', self) # Імпорт граф. дизайну
		self.old_row = 0
		self.old_column = 0
		self.old_text = ''
		self.show() # Show the GUI
		self.prepare()
	def prepare(self):
		# Виконується тільки один раз, підготовка таблиці і тд
		self.board.cellClicked.connect(self.selected)
		self.reset_button.clicked.connect(self.reset)
		self.edit_button.clicked.connect(self.edit_mode)
		self.board.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
		for i in range(8):
			self.board.setColumnWidth(i,59)
			self.board.setRowHeight(i,58)
			for k in range(8):
				item = QTableWidgetItem()
				item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				self.board.setItem(i,k,item)
				if((k+i)%2!=0):
					self.board.item(i,k).setBackground(QColor("#000000"))
					self.board.item(i,k).setForeground(QColor("#ffffff"))

				else:
					self.board.item(i, k).setBackground(QColor("#ffffff"))
					self.board.item(i, k).setForeground(QColor("#000000"))
		self.reset()
		self.board.itemChanged.connect(self.change)
	def change(self):
		# Перевірка введеної користувачем назви фігури на правильність написання
		row, column = self.current_cell()
		text = self.board.item(row,column).text()
		if(text not in allowed):
			self.board.item(row,column).setText('')

	def edit_mode(self):
		# Режим ручного введення кліток
		if(self.edit_button.isChecked()):
			self.board.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
		else:
			self.board.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
	def reset(self):
		# Розстановка стартових фігур
		for i in range(8):
			self.board.item(1,i).setText("П")
			self.board.item(6,i).setText("П")
		self.board.item(7,0).setText("Т")
		self.board.item(7,7).setText("Т")
		self.board.item(0,7).setText("Т")
		self.board.item(0,0).setText("Т")
		self.board.item(0,1).setText("К")
		self.board.item(0,6).setText("К")
		self.board.item(7,1).setText("К")
		self.board.item(7,6).setText("К")
		self.board.item(0,2).setText("С")
		self.board.item(0,5).setText("С")
		self.board.item(7,2).setText("С")
		self.board.item(7,5).setText("С")
		self.board.item(7,3).setText("Ф")
		self.board.item(0,3).setText("Ф")
		self.board.item(7,4).setText("Кр")
		self.board.item(0,4).setText("Кр")
	def current_cell(self):
		row = self.board.currentRow()
		column = self.board.currentColumn()
		return row, column
	def move(self,to_row,to_column,from_row,from_column,figure):
		# Рух фігури
		self.board.item(from_row,from_column).setText('')
		self.board.item(to_row,to_column).setText(figure)
	def selected(self):
		# Допоміжна функція move
		row, column = self.current_cell()
		text = self.board.item(row,column).text()
		if (self.old_text != text and text == ''):
			self.move(row, column, self.old_row, self.old_column, self.old_text)
			#pass
		self.old_row = row
		self.old_column = column
		self.old_text = text

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = App()
	app.exec()
#


