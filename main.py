from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QTableWidgetItem,QMainWindow,QTableWidget, QWidget
from PyQt6.QtGui import QColor, QPainter, QPixmap
import numpy as np
import sys, traceback
import random
allowed = ('П1','Т1','Кі1','С1','Ф1','Кр1','П2','Т2','Кі2','С2','Ф2','Кр2')
horse_moves_x = (2,2, -2,-2, 1,-1, 1,-1)
horse_moves_y = (1,-1, 1,-1, -2,-2, 2,2)
king_moves_x = (1,1,1,0,0,-1,-1,-1)
king_moves_y = (-1,0,1,-1,1,-1,0,1)
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
		self.edit_mode = False
		self.white_king_pos = "7|4"
		self.black_king_pos = "0|4"
		self.allowed_moves = []
		self.banned_moves_with_team = []
		self.banned_moves = []
		self.possible_moves = []
		self.possible_attacks = []
		self.attack_moves = []
		self.king_possible_moves = []
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
		self.edit_button.clicked.connect(self.edit)
		self.board.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
		for i in range(8):
			self.board.setColumnWidth(i,59)
			self.board.setRowHeight(i,60)
			for k in range(8):
				item = QTableWidgetItem()
				item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				self.board.setItem(i, k, item)
		self.clear_ways()
		self.reset()
		self.board.itemChanged.connect(self.change)
	def calculate(self):
		self.black_count = 0
		self.white_count = 0
		for i in range(8):
			for k in range(8):
				if(self.board.item(i,k).text().__contains__("1")):
					if(self.get_figure(i,k)=="П1"):
						self.white_count += 1
					elif (self.get_figure(i, k) == "С1" or self.get_figure(i, k) == "Кі1"):
						self.white_count += 3
					elif (self.get_figure(i, k) == 'Т1'):
						self.white_count += 5
					elif (self.get_figure(i,k) == "Ф1"):
						self.white_count += 9
				elif(self.board.item(i,k).text().__contains__("2")):
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
	def clear_ways(self):
		for i in range(8):
			for k in range(8):
				if ((k + i) % 2 != 0):
					self.board.item(i, k).setBackground(QColor("#000000"))
					self.board.item(i, k).setForeground(QColor("#000000"))

				else:
					self.board.item(i, k).setBackground(QColor("#ffffff"))
					self.board.item(i, k).setForeground(QColor("#ffffff"))
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
	def edit(self):
		# Режим ручного введення кліток
		if(self.edit_button.isChecked()):
			self.edit_mode = True
			self.board.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
		else:
			self.edit_mode = False
			self.board.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
	def reset(self):
		# Очистка поля
		self.clear_ways()
		self.end_label.hide()
		self.end.hide()
		self.whos_turn.setStyleSheet("background-color : white;")
		self.turn = "White"
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
	def bot_move(self):
		do = []
		# print("="*10)
		self.get_possible_attacks(0,0,False)
		# print("="*10)
		for attack in self.attack_moves:
			# print("Attack" + attack)
			row = int(attack.split("|")[2])
			column = int(attack.split("|")[3])
			# try:
			if(self.get_team(self.board.item(row,column).text()) == 1):
				do.append(attack)
		if(len(do) == 0):
			# print("move")
			for move in self.possible_moves:
				row = move.split("|")[2]
				column = move.split("|")[3]
				if(f"{row}|{column}" in self.banned_moves):
					continue
				# print("Move"+move)
				do.append(move)
		if(len(do) != 0):
			rand_choice = random.choice(do)
			# print("rand - " + rand_choice)
			self.game("",rand_choice)
		else:
			self.end_game("2")
		# row = int(rand_choice.split("|")[0])
		# column = int(rand_choice.split("|")[1])
		# old_row = int(rand_choice.split("|")[2])
		# old_column = int(rand_choice.split("|")[3])
		# print(rand_choice)
		# self.move(row,column,old_row,old_column)
		# print(do)
	def move(self,to_row,to_column,from_row,from_column):
		# print("def move called")
		# print(to_row,to_column,from_row,from_column)
		self.clear_ways()
		figure = self.get_figure(from_row,from_column)
		# Рух фігури
		self.board.item(from_row, from_column).setText('')
		self.remImage(from_row, from_column)
		self.board.item(to_row, to_column).setText(figure)
		self.setImage(to_row,to_column,figure)
		# Переміщення картинки
		# if (figure.__contains__("П")):
		# 	if(self.get_team(figure) == 1):
		# 		self.board.item(to_row+1, to_column).setText('')
		# 		self.remImage(to_row+1,to_column)
		# 	elif(self.get_team(figure) == 2):
		# 		self.board.item(to_row-1, to_column).setText('')
		# 		self.remImage(to_row-1,to_column)
		if (figure.__contains__("П") and (to_row == 7 or to_row == 0)):
			while True:
				rand = random.choice(allowed)
				if(not rand.__contains__("Кр") and not rand.__contains__("П")):
					if self.get_team(rand) == self.get_team(figure):
						self.board.item(to_row, to_column).setText(rand)
						break
		#
		if(self.turn == "Black"):
			self.turn = "White"
			self.whos_turn.setStyleSheet("background-color : white;")
		elif(self.turn == "White"):
			self.turn = "Black"
			self.whos_turn.setStyleSheet("background-color : black;")
			if (self.bot_button.isChecked() == True):
				self.bot_move()
				# self.bot_move()
	def get_team(self,text):
		if(text.__contains__("1")):
			return 1
		elif(text.__contains__("2")):
			return 2
		else:
			return None
	def get_possible_attacks(self,row,column,one=False):
		self.attack_moves = []
		self.banned_moves_with_team = []
		self.banned_moves = []
		self.possible_moves = []
		self.possible_attacks = []
		self.king_possible_moves = []
		if(self.turn == "Black" and self.bot_button.isChecked() == True):
			team = 2
			# self.turn = "Black"
		else:
			team = self.get_team(self.get_figure(row,column))
		# print(team)
		# print(f"Team - {team}, row - {row}, column - {column}")
		if(one == False):
			for i in range(8):
				for k in range(8):
					self.game(f"{i}|{k}")
					if(self.get_figure(i,k).__contains__("Кр")):
						if(self.get_team(self.get_figure(i,k))==1):
							self.white_king_pos = f"{i}|{k}"
							# print("White king pos = "+self.white_king_pos)
						else:
							self.black_king_pos = f"{i}|{k}"
							# print("Black king pos = "+self.black_king_pos)
		else:
			self.game(f"{row}|{column}","")
		#print(self.possible_moves)
		temp = []
		# print(self.turn)
		# print(self.bot_button.isChecked())
		if(self.turn == "Black" and self.bot_button.isChecked() == True):
			for figure in self.possible_moves:
				if (int(figure.split("|")[3]) not in range(0, 8) or int(figure.split("|")[4]) not in range(0, 8)):
					# print(figure)
					# print("skipped")
					continue
				if (self.get_team(figure.split("|")[0]) == team):
					# print(figure)
					temp.append(f"{figure.split('|')[1]}|{figure.split('|')[2]}|{figure.split('|')[3]}|{figure.split('|')[4]}")
			self.possible_moves = temp
		# print(self.possible_moves)
		for figure in self.possible_attacks:
			# print("="*10)
			# print(figure)
			if(int(figure.split("|")[3]) not in range (0,8) or int(figure.split("|")[4]) not in range (0,8)):
				# print(figure)
				# print("skipped")
				continue
			# print(self.get_team(figure.split("|")[0]), team)
			if (self.get_team(figure.split("|")[0]) != team):
				# print(self.get_team(figure.split("|")[0]))
				# print(figure)
				# print(figure)
				# {figure.split('|')[0]}|
				# print(f"{figure.split('|')[0]}|{figure.split('|')[1]}|{figure.split('|')[2]}")
				self.banned_moves_with_team.append(f"{figure.split('|')[0]}|{figure.split('|')[3]}|{figure.split('|')[4]}")
				self.banned_moves.append(f"{figure.split('|')[3]}|{figure.split('|')[4]}")
			else:
				self.attack_moves.append(f"{figure.split('|')[1]}|{figure.split('|')[2]}|{figure.split('|')[3]}|{figure.split('|')[4]}")
		temp = []
		# print(self.king_possible_moves)
		for figure in self.king_possible_moves:
			if(self.get_team(figure.split("|")[0]) == team):
				temp.append(f"{figure.split('|')[1]}|{figure.split('|')[2]}")
		self.king_possible_moves = temp
		# print(self.king_possible_moves)
		# print(self.attack_moves)
	def end_game(self,text):
		if (self.get_team(text) == 1):
			self.end_label.setText('Чорні перемогли')
		else:
			self.end_label.setText('Білі перемогли')
		self.end_label.show()
		self.end.show()
	def game(self,check_coords = "",play=""):
		# print("="*15)
		allowed_moves = []
		if(play == ""):
			row, column = self.current_cell()
			text = self.board.item(row, column).text()
		if(self.edit_mode == False):
			if (play != ""):
				self.old_row = int(play.split("|")[0])
				self.old_column = int(play.split("|")[1])
				row = int(play.split("|")[2])
				column = int(play.split("|")[3])
				self.old_text = self.get_figure(self.old_row,self.old_column)
				text = self.get_figure(row, column)
				# print("=1=")

			elif (check_coords != ""):
				row = int(check_coords.split("|")[0])
				column = int(check_coords.split("|")[1])
				text = self.board.item(row, column).text()
				# print("=2=")
			if (check_coords == ""):
				# print(text)
				# print(self.turn)
				# if(self.turn == "White" and self.get_team(text) not in (1,None) and self.get_team(self.old_text) == 2):
				# 	return
				# elif(self.turn == "Black" and self.get_team(text) not in (2,None) and self.get_team(self.old_text) == 1):
				# 	return
				self.clear_ways()
				if(text!=""):
					self.get_possible_attacks(row, column, False)
					a = np.array(self.king_possible_moves)
					b = np.array(self.banned_moves)
					result = np.isin(a, b)
					# print(result)
					if (len(result) != 0):
						end = True
						for i in result:
							if (i == True):
								continue
							else:
								end = False
						if (end == True):
							self.end_game(self.get_figure(row, column))
		# print(text)
		# print(row,column)
		# print(text)
		# print(text)
		# print(text + ' => ' + self.old_text)
		# print(str(row)+"|"+str(column), self.get_figure(row,column))

		# if (check_coords == "" and self.old_text != '' and text != '' and self.get_team(self.old_text) != self.get_team(text)):
		# 	if ((str(row) + '|' + str(column) in self.allowed_moves)):
		# 		# print("so sad")
		# 		self.move(row, column, self.old_row, self.old_column)
		# 		if (text.__contains__("Кр")):
		# 			self.end_game(text)
			# self.reset()
			# return
		if (self.edit_mode == False):
			# print(self.attack_moves)
			king_in_danger = False
			for figure in self.banned_moves_with_team:
				r = figure.split("|")[1]
				c = figure.split("|")[2]
				t = self.get_team(figure.split("|")[0])
				if (self.white_king_pos == f"{r}|{c}" and t == 2):
					king_in_danger = True
					king_row = int(self.white_king_pos.split("|")[0])
					king_column = int(self.white_king_pos.split("|")[1])
					self.board.item(king_row, king_column).setBackground(QColor("#eb4034"))
					self.board.item(king_row, king_column).setForeground(QColor("#eb4034"))
				elif (self.black_king_pos == f"{r}|{c}" and t == 1):
					king_in_danger = True
					king_row = int(self.black_king_pos.split("|")[0])
					king_column = int(self.black_king_pos.split("|")[1])
					self.board.item(king_row, king_column).setBackground(QColor("#eb4034"))
					self.board.item(king_row, king_column).setForeground(QColor("#eb4034"))

			if(text.__contains__("Кр")):
				# if(check_coords==""):
				# 	self.get_possible_attacks(row,column,False)
				# print(f"= {text}|{row}|{column}")
				self.king_possible_moves.append(f"{text}|{row}|{column}")
				for i in range(8):
					try:
						possible_way = self.board.item(row + king_moves_x[i], column + king_moves_y[i])
						move = f"{row + king_moves_x[i]}|{column + king_moves_y[i]}"
						self.possible_attacks.append(f"{text}|{row}|{column}|{move}")
						if (self.get_team(self.get_figure(row,column)) != self.get_team(possible_way.text())):
							if(move not in self.banned_moves):
								self.king_possible_moves.append(f"{text}|{move}")
								allowed_moves.append(f"{row + king_moves_x[i]}|{column + king_moves_y[i]}")
								if (check_coords == "" or play != ""):
									possible_way.setBackground(QColor("#515151"))
								else:
									self.possible_moves.append(f"{text}|{row}|{column}|{move}")
					except:
						pass
				#print(self.king_possible_moves)
			if(king_in_danger == False or check_coords !=''):
				if (text.__contains__("Кі")):
					for i in range(8):
						try:
							possible_way = self.board.item(row + horse_moves_x[i], column + horse_moves_y[i])
							if (self.get_team(self.get_figure(row, column)) != self.get_team(possible_way.text())):
								allowed_moves.append(f"{row + horse_moves_x[i]}|{column + horse_moves_y[i]}")
								if (check_coords == "" or play != ""):
									possible_way.setBackground(QColor("#515151"))
								else:
									self.possible_moves.append(
										f"{text}|{row}|{column}|{row + horse_moves_x[i]}|{column + horse_moves_y[i]}")
									self.possible_attacks.append(self.possible_moves[-1])
						except:
							pass
				elif (text.__contains__("С")):
					i = row - 1
					k = column - 1
					while (i >= 0 and k >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == "" or play != ""):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i - 1
						k = k - 1
					i = row + 1
					k = column + 1
					while (i <= 7 and k <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == ''):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i + 1
						k = k + 1
					i = row + 1
					k = column - 1
					while (i <= 7 and k >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == ''):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i + 1
						k = k - 1
					i = row - 1
					k = column + 1
					while (i >= 0 and k <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == ''):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i - 1
						k = k + 1
				elif (text == "П1"):
					self.possible_attacks.append(f"{text}|{row}|{column}|{row - 1}|{column - 1}")
					self.possible_attacks.append(f"{text}|{row}|{column}|{row - 1}|{column + 1}")
					# self.possible_attacks.append(f"{text}|{row}|{column + 1}")
					# self.possible_attacks.append(f"{text}|{row}|{column - 1}")
					try:
						if (self.get_team(self.get_figure(row - 1, column - 1)) != self.get_team(text)):
							if (self.get_figure(row - 1, column - 1) != ""):
								allowed_moves.append(f"{row - 1}|{column - 1}")
								if (check_coords == "" or play != ""):
									self.board.item(row - 1, column - 1).setBackground(QColor("#515151"))
					except:
						pass
					# try:
					# 	if (self.get_team(self.get_figure(row, column - 1)) != self.get_team(text)):
					# 		if (self.get_figure(row, column - 1) != ""):
					# 			allowed_moves.append(f"{row - 1}|{column - 1}")
					# 			if (check_coords == "" or play != ""):
					# 				self.board.item(row - 1, column - 1).setBackground(QColor("#515151"))
					# except:
					# 	pass
					# try:
					# 	if (self.get_team(self.get_figure(row, column + 1)) != self.get_team(text)):
					# 		if (self.get_figure(row, column + 1) != ""):
					# 			allowed_moves.append(f"{row - 1}|{column + 1}")
					# 			if (check_coords == "" or play != ""):
					# 				self.board.item(row - 1, column + 1).setBackground(QColor("#515151"))
					# except:
					# 	pass

					try:
						if (self.get_team(self.get_figure(row - 1, column + 1)) != self.get_team(text)):
							if (self.get_figure(row - 1, column + 1) != ""):

								allowed_moves.append(f"{row - 1}|{column + 1}")
								if (check_coords == "" or play != ""):
									self.board.item(row - 1, column + 1).setBackground(QColor("#515151"))
					except:
						pass
					try:
						if (self.get_figure(row - 1, column) == ""):

							if (row == 6 and self.get_figure(row - 2, column) == ""):
								for i in range(1, 3):
									allowed_moves.append(f"{row - i}|{column}")
									if (check_coords == "" or play != ""):
										self.board.item(row - i, column).setBackground(QColor("#515151"))
									else:
										self.possible_moves.append(f"{text}|{row}|{column}|{row - i}|{column}")
							else:
								allowed_moves.append(f"{row - 1}|{column}")
								if (check_coords == "" or play != ""):
									self.board.item(row - 1, column).setBackground(QColor("#515151"))
								else:
									self.possible_moves.append(f"{text}|{row}|{column}|{row - 1}|{column}")
					except:
						pass
				elif (text == "П2"):
					self.possible_attacks.append(f"{text}|{row}|{column}|{row + 1}|{column - 1}")
					self.possible_attacks.append(f"{text}|{row}|{column}|{row + 1}|{column + 1}")
					# self.possible_attacks.append(f"{text}|{row}|{column - 1}")
					# self.possible_attacks.append(f"{text}|{row}|{column + 1}")
					try:
						if (self.get_team(self.get_figure(row + 1, column - 1)) != self.get_team(text)):
							if (self.get_figure(row + 1, column - 1) != ""):

								allowed_moves.append(f"{row + 1}|{column - 1}")
								if (check_coords == "" or play != ""):
									self.board.item(row + 1, column - 1).setBackground(QColor("#515151"))
					except:
						pass
					try:
						if (self.get_team(self.get_figure(row + 1, column + 1)) != self.get_team(text)):
							if (self.get_figure(row + 1, column + 1) != ""):

								allowed_moves.append(f"{row + 1}|{column + 1}")
								if (check_coords == "" or play != ""):
									self.board.item(row + 1, column + 1).setBackground(QColor("#515151"))
					except:
						pass
					# try:
					# 	if (self.get_team(self.get_figure(row, column - 1)) != self.get_team(text)):
					# 		if (self.get_figure(row, column - 1) != ""):
					# 			allowed_moves.append(f"{row + 1}|{column - 1}")
					# 			if (check_coords == "" or play != ""):
					# 				self.board.item(row + 1, column - 1).setBackground(QColor("#515151"))
					# except:
					# 	pass
					# try:
					# 	if (self.get_team(self.get_figure(row, column + 1)) != self.get_team(text)):
					# 		if (self.get_figure(row, column + 1) != ""):
					# 			allowed_moves.append(f"{row + 1}|{column + 1}")
					# 			if (check_coords == "" or play != ""):
					# 				self.board.item(row + 1, column + 1).setBackground(QColor("#515151"))
					# except:
					# 	pass
					try:
						if (self.get_figure(row + 1, column) == ""):
							if (row == 1 and self.get_figure(row + 2, column) == ""):
								for i in range(1, 3):
									allowed_moves.append(f"{row + i}|{column}")
									if (check_coords == "" or play != ""):
										self.board.item(row + i,
										                column).setBackground(QColor("#515151"))
									else:
										self.possible_moves.append(f"{text}|{row}|{column}|{row + i}|{column}")
							else:
								allowed_moves.append(f"{row + 1}|{column}")
								if (check_coords == "" or play != ""):
									self.board.item(row + 1, column).setBackground(QColor("#515151"))
								else:
									self.possible_moves.append(f"{text}|{row}|{column}|{row + 1}|{column}")
					except:
						pass
				elif (text.__contains__("Ф")):
					i = row - 1
					k = column - 1
					while (i >= 0 and k >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == "" or play != ""):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i - 1
						k = k - 1
					i = row + 1
					k = column + 1
					while (i <= 7 and k <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == "" or play != ""):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])

							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i + 1
						k = k + 1
					i = row + 1
					k = column - 1
					while (i <= 7 and k >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == "" or play != ""):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i + 1
						k = k - 1
					i = row - 1
					k = column + 1
					while (i >= 0 and k <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(i, k))):
							allowed_moves.append(f"{i}|{k}")

							if (check_coords == "" or play != ""):
								self.board.item(i, k).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{k}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, k) != ''):
								break
						else:
							break
						i = i - 1
						k = k + 1
					i = row - 1
					while (i >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(i, column))):
							allowed_moves.append(f"{i}|{column}")

							if (check_coords == "" or play != ""):
								self.board.item(i, column).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{column}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, column) != ''):
								break
						else:
							break
						i = i - 1
					i = row + 1
					while (i <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(i, column))):
							allowed_moves.append(f"{i}|{column}")

							if (check_coords == "" or play != ""):
								self.board.item(i, column).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{column}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, column) != ''):
								break
						else:
							break
						i = i + 1
					i = column + 1
					while (i <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(row, i))):
							allowed_moves.append(f"{row}|{i}")

							if (check_coords == "" or play != ""):
								self.board.item(row, i).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{row}|{i}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(row, i) != ''):
								break
						else:
							break
						i = i + 1
					i = column - 1
					while (i >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(row, i))):
							try:
								allowed_moves.append(f"{row}|{i}")

								if (check_coords == "" or play != ""):
									self.board.item(row, i).setBackground(QColor("#515151"))
								else:
									self.possible_moves.append(f"{text}|{row}|{column}|{row}|{i}")
									self.possible_attacks.append(self.possible_moves[-1])
								if (self.get_figure(row, i) != ''):
									break
							except:
								pass
						else:
							break
						i = i - 1
				elif (text.__contains__("Т")):
					i = row - 1
					while (i >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(i, column))):
							allowed_moves.append(f"{i}|{column}")

							if (check_coords == "" or play != ""):
								self.board.item(i, column).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{column}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, column) != ''):
								break
						else:
							break
						i = i - 1
					i = row + 1
					while (i <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(i, column))):
							allowed_moves.append(f"{i}|{column}")

							if (check_coords == "" or play != ""):
								self.board.item(i, column).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{i}|{column}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(i, column) != ''):
								break
						else:
							break
						i = i + 1
					i = column + 1
					while (i <= 7):
						if (self.get_team(text) != self.get_team(self.get_figure(row, i))):
							allowed_moves.append(f"{row}|{i}")

							if (check_coords == "" or play != ""):
								self.board.item(row, i).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{row}|{i}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(row, i) != ''):
								break
						else:
							break
						i = i + 1
					i = column - 1
					while (i >= 0):
						if (self.get_team(text) != self.get_team(self.get_figure(row, i))):
							allowed_moves.append(f"{row}|{i}")

							if (check_coords == "" or play != ""):
								self.board.item(row, i).setBackground(QColor("#515151"))
							else:
								self.possible_moves.append(f"{text}|{row}|{column}|{row}|{i}")
								self.possible_attacks.append(self.possible_moves[-1])
							if (self.get_figure(row, i) != ''):
								break
						# if(self.get_figure(i,column) != ''):
						# 	break
						else:
							break
						i = i - 1
			# print(self.allowed_moves)
			if (self.turn == "Black" and self.bot_button.isChecked() and check_coords == ""):
				self.move(row, column, self.old_row, self.old_column)
			elif (str(row) + '|' + str(
					column) in self.allowed_moves and check_coords=="" and self.get_team(
					self.old_text) != self.get_team(
					text)):
				self.move(row, column, self.old_row, self.old_column)
				# if (self.turn == "White" and self.get_team(self.old_text) == 1):
				# 	self.move(row, column, self.old_row, self.old_column)
				# elif (self.turn == "Black" and self.get_team(self.old_text) == 2):
				# 	self.move(row, column, self.old_row, self.old_column)
		else:
			self.remImage(row, column)
			self.board.item(row, column).setText('')
			text = ''
		#print(self.possible_moves)
		if(check_coords==""):
			self.old_row = row
			self.old_column = column
			self.old_text = text
			self.allowed_moves = allowed_moves

	def selected(self):
		# Допоміжна функція move
		if(self.turn == "White" or self.bot_button.isChecked() == False):
			self.game('')

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