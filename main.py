from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QTableWidgetItem,QMainWindow,QTableWidget, QWidget
from PyQt6.QtGui import QColor, QPainter, QPixmap
import sys, traceback
allowed = ('П1','Т1','Кі1','С1','Ф1','Кр1','П2','Т2','Кі2','С2','Ф2','Кр2')
class ImageWidget(QWidget):

    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)
class App(QMainWindow):
	def __init__(self):
		super(App, self).__init__()
		uic.loadUi('main.ui', self) # Імпорт граф. дизайну

		self.old_row = 0
		self.old_column = 0
		self.old_text = ''
		self.show() # Show the GUI
		self.prepare()
		self.calculate()
	def setImage(self, row, col, text):
		# Добавити іконку фігури в клітинку
		if (text.__contains__("П")):
			if (text.__contains__("1")):
				path = 'resized_sprites/wp.png'
			else:
				path = 'resized_sprites/bp.png'
		elif (text.__contains__("Т")):
			if (text.__contains__("1")):
				path = 'resized_sprites/wr.png'
			else:
				path = 'resized_sprites/br.png'
		elif (text.__contains__("Кі")):
			if (text.__contains__("1")):
				path = 'resized_sprites/wn.png'
			else:
				path = 'resized_sprites/bn.png'
		elif (text.__contains__("С")):
			if (text.__contains__("1")):
				path = 'resized_sprites/wb.png'
			else:
				path = 'resized_sprites/bb.png'
		elif (text.__contains__("Ф")):
			if (text.__contains__("1")):
				path = 'resized_sprites/wq.png'
			else:
				path = 'resized_sprites/bq.png'
		elif (text.__contains__("Кр")):
			if (text.__contains__("1")):
				path = 'resized_sprites/wk.png'
			else:
				path = 'resized_sprites/bk.png'
		else:
			path = None
		image = ImageWidget(path, self.board)
		self.board.setCellWidget(row, col, image)
	def remImage(self, row, col):
		# Видалити іконку фігури з клітинки
		self.board.setCellWidget(row, col, None)
	def prepare(self):
		# Виконується тільки один раз, підготовка таблиці і тд
		self.board.cellClicked.connect(self.selected)
		self.reset_button.clicked.connect(self.reset)
		self.edit_button.clicked.connect(self.edit_mode)
		self.board.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
		for i in range(8):
			self.board.setColumnWidth(i,59)
			self.board.setRowHeight(i,60)
			for k in range(8):
				item = QTableWidgetItem()
				item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				self.board.setItem(i,k,item)
				if((k+i)%2!=0):
					self.board.item(i,k).setBackground(QColor("#000000"))
					self.board.item(i,k).setForeground(QColor("#000000"))

				else:
					self.board.item(i, k).setBackground(QColor("#ffffff"))
					self.board.item(i, k).setForeground(QColor("#ffffff"))
		self.reset()
		self.board.itemChanged.connect(self.change)
	def calculate(self):
		self.black = []
		self.white = []
		self.black_count = 0
		self.white_count = 0
		for i in range(8):
			for k in range(8):
				if(self.board.item(i,k).text().__contains__("1")):
					self.white.append(f'{i}/{k}')
					if(self.get_figure(i,k)=="П1"):
						self.white_count += 1
					elif (self.get_figure(i, k) == "С1" or self.get_figure(i, k) == "Кі1"):
						self.white_count += 3
					elif (self.get_figure(i, k) == 'Т1'):
						self.white_count += 5
					elif (self.get_figure(i,k) == "Ф1"):
						self.white_count += 9
				elif(self.board.item(i,k).text().__contains__("2")):
					self.black.append(f'{i}/{k}')
					if(self.get_figure(i,k)=="П2"):
						self.black_count += 1
					elif (self.get_figure(i, k) == "С2" or self.get_figure(i, k) ==  "Кі2"):
						self.black_count += 3
					elif (self.get_figure(i, k) == 'Т2'):
						self.black_count += 5
					elif (self.get_figure(i,k) == "Ф2"):
						self.black_count += 9
		self.calc_label.setText(f'Ціна білих:{self.white_count}\n'
		                        f'Ціна чорних:{self.black_count}')
	def get_figure(self,row,column):
		return self.board.item(row,column).text()
	def change(self):
		# Перевірка введеної користувачем назви фігури на правильність написання
		row, column = self.current_cell()
		text = self.board.item(row,column).text()
		self.calculate()
		if(text not in allowed):
			self.board.item(row,column).setText('')
			self.remImage(row, column)
		else:
			self.board.item(row, column).setText(text)
			self.setImage(row, column, text)
	def edit_mode(self):
		# Режим ручного введення кліток
		if(self.edit_button.isChecked()):
			self.board.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
		else:
			self.board.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
	def reset(self):
		# Очистка поля
		for i in range(8):
			for k in range(8):
				self.board.item(i,k).setText('')
				self.remImage(i,k)
		# Розстановка стартових фігур
		for i in range(8):
			self.board.item(6,i).setText("П1")
			self.board.item(1,i).setText("П2")
		# Команда білих
		self.board.item(7,0).setText("Т1")
		self.board.item(7,7).setText("Т1")
		self.board.item(7,1).setText("Кі1")
		self.board.item(7,6).setText("Кі1")
		self.board.item(7,2).setText("С1")
		self.board.item(7,5).setText("С1")
		self.board.item(7,3).setText("Ф1")
		self.board.item(7,4).setText("Кр1")
		# Команда чорних
		self.board.item(0,7).setText("Т2")
		self.board.item(0,0).setText("Т2")
		self.board.item(0,1).setText("Кі2")
		self.board.item(0,6).setText("Кі2")
		self.board.item(0,2).setText("С2")
		self.board.item(0,5).setText("С2")
		self.board.item(0,3).setText("Ф2")
		self.board.item(0,4).setText("Кр2")
		for i in range(8):
			for k in range(8):
				text = self.board.item(i,k).text()
				self.setImage(i,k,text)
	def current_cell(self):
		row = self.board.currentRow()
		column = self.board.currentColumn()
		return row, column
	def move(self,to_row,to_column,from_row,from_column,figure):
		# Рух фігури
		self.board.item(from_row,from_column).setText('')
		self.board.item(to_row,to_column).setText(figure)
		# Переміщення картинки
		self.remImage(from_row,from_column)
	def selected(self):
		# Допоміжна функція move
		row, column = self.current_cell()
		text = self.board.item(row,column).text()
		if (self.old_text != text and text == "" and not self.edit_button.isChecked()):
			self.move(row, column, self.old_row, self.old_column, self.old_text)
		if(self.edit_button.isChecked()):
			self.remImage(row,column)
			self.board.item(row,column).setText('')
			text = ''
		self.old_row = row
		self.old_column = column
		self.old_text = text
def excepthook(exc_type, exc_value, exc_tb):
	# На випадок, якщо програма крашнеться, зберігає код помилки у файл
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    file = open("error.txt","w")
    file.write(tb)
    file.close()
    app.quit()
if __name__ == "__main__":
	sys.excepthook = excepthook
	app = QApplication(sys.argv)
	window = App()
	app.exec()