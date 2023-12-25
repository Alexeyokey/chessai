import sqlite3
import sys
import threading

from new_ai import get_ai_move, model
import datetime
import chess
import torch
import numpy as np
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPainter, QColor, QCursor
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QMainWindow, QLayout, QButtonGroup, QMessageBox
from ui_forms import *
from painting import figures_with_circles


class Lobby(QMainWindow, UiFormLobby):
    def __init__(self):
        super().__init__()
        self.MENU = ['НОВАЯ ИГРА', 'ИГРА С БОТОМ', "ОТКРЫТЬ", "НАСТРОЙКИ"]
        self.menu_btns = []
        self.initUI()
        self.sql_tables()

    def initUI(self):
        self.setupUi(self)
        self.dev_btn.clicked.connect(self.mes_box_dev_act)
        self.menu_btns[0].clicked.connect(self.new_game_btn_act)
        self.menu_btns[1].clicked.connect(self.new_game_bot)
        self.menu_btns[2].clicked.connect(self.open_btn_act)
        self.menu_btns[3].clicked.connect(self.options_btn_act)

    def new_game_btn_act(self):
        self.msg = NewGameNicknamesWindow(self)
        self.msg.show()

    def new_game_bot(self):
        self.msg = NewGameNicknamesWindowBot(self)
        self.msg.show()

    def open_btn_act(self):
        self.msg = OpenWindow(self)
        self.msg.show()

    def options_btn_act(self):
        self.secondform = Settings()
        self.secondform.show()

    def mes_box_dev_act(self):
        self.msg = DevWindow(self)
        self.msg.show()

    def sql_tables(self):
        """Create tables in databes.db if they don't exist"""
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS SAVES (
                            saveid INTEGER PRIMARY KEY,
                            game_name nvarchar(1000) NOT NULL,
                            firstname nvarchar(1000) NOT NULL,
                            secondname nvarchar(1000) NOT NULL,
                            amount_of_actions INTEGER,
                            general_time INTEGER)
                            """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS USERS (
                            userid INTEGER PRIMARY KEY,
                            name nvarchar(1000) NOT NULL,
                            amount_of_plays INTEGER)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS USERCOMMENT (
                                    commentid INTEGER PRIMARY KEY,
                                    score INTEGER,
                                    comment nvarchar(1000) NOT NULL,
                                    userid INTEGER,
                                    FOREIGN KEY (userid)  REFERENCES USERS (userid))
                                    """)
        con.commit()
        con.close()


class Settings(QWidget, UiFormSettings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.player = QMediaPlayer()
        file_path = os.path.join(os.getcwd(), 'music/premonition.mp3')
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(content)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        self.checkBox.toggled.connect(self.mute_unmute)
        self.btn_back.setStyleSheet(stylesheet_normal_btn)
        self.horizontalSlider.valueChanged.connect(self.value)
        self.pushButton_2.clicked.connect(self.sprite_change)
        self.btn_back.clicked.connect(self.back)
        self.horizontalSlider.setValue(music_volume)
        self.checkBox.setChecked(music_muted)
        self.mute_unmute(music_muted)
        self.msg = QMessageBox()

    def value(self, event):
        global music_volume
        music_volume = event
        self.player.setVolume(music_volume)

    def mute_unmute(self, event):
        global music_muted
        if not event:
            self.player.isSeekable()
            self.player.play()
            music_muted = False
            self.player.setMuted(False)
        else:
            music_muted = True
            self.player.setMuted(True)

    def sprite_change(self):
        global current_folder
        folder_name = self.lineEdit.text()
        self.msg.setText('Смена спрайтов провалилась! '
                         '\nПроверьте наличие папки с таким именем, размер картинок и их количество')
        if folder_name in os.listdir('sprites'):
            if figures_with_circles(folder_name):
                current_folder = folder_name
                self.msg.setText('Смена спрайтов удалась!')
        self.msg.show()

    def back(self):
        self.close()


class DevWindow(QWidget, UiFormDevNew):
    def __init__(self, lobby_obj: QWidget):
        super().__init__()
        self.lobby_obj = lobby_obj
        self.initUI()
        self.btn_comments()

    def initUI(self):
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click_create_new_comment)
        self.btn_back = QPushButton("Назад")
        self.btn_back.setStyleSheet(stylesheet_normal_btn)
        self.verticalLayout.addWidget(self.btn_back)
        self.btn_back.clicked.connect(self.back)

    def back(self):
        self.close()

    def fetchall_data(self):  # получение всех комментариев и оценок для создания кнопок изменения комментариев
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM USERCOMMENT;")
        data_fetch = cursor.fetchall()
        con.close()
        return data_fetch

    def sql_data_btn_comment(self, id):
        """Receiving a comment_line by id in databse"""
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM USERCOMMENT WHERE commentid={id};")
        line = cursor.fetchone()
        con.close()
        return line

    def btn_comments(self):
        """Creating comment buttons in the ScrollArea"""
        vertical = QVBoxLayout(self.frame)
        rows = self.fetchall_data()  # получение всех комментариев
        for row in rows:
            btn = QPushButton(f'Отзыв {row[0]}')
            btn.setMinimumHeight(50)
            btn.setStyleSheet(stylesheet_comment_btns)
            btn.clicked.connect(self.click_comment)
            vertical.addWidget(btn)
            vertical.setAlignment(Qt.AlignTop)

    def click_comment(self):
        """processing a click on the comment button"""
        id = self.sender().text().split()[-1]
        row = self.sql_data_btn_comment(id)  # получение отдельного комментария по id
        self.lobby_obj.msg = NewCommentWindow(self.lobby_obj, row)
        self.lobby_obj.msg.show()

    def click_create_new_comment(self):
        """add a new comment to the database"""
        self.lobby_obj.msg = NewCommentWindow(self.lobby_obj)
        self.lobby_obj.msg.show()


class NewCommentWindow(QWidget, UiFormNewComment):
    def __init__(self, lobby_obj: QWidget, line=tuple()):  # принятие объектов для последующего
        # их закрытия
        super().__init__()
        self.lobby_obj = lobby_obj
        self.line = line
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        if self.line:  # если есть переданное значение(отзыв), то устанавливаем ту же оценку и текст,что и в row
            con = sqlite3.connect("datebase.db")
            cursor = con.cursor()
            name = cursor.execute(f"SELECT name from USERS where userid = '{self.line[3]}'").fetchone()
            con.close()
            self.horizontalLayout.itemAt(int(self.line[1]) - 1).widget().toggle()
            self.comment_section.setText(self.line[2])
            self.player_name.setText(name[0])

    def back(self):
        self.close()

    def click(self, btn):
        self.user_score = btn.text()
        self.confirmation_btn.setEnabled(True)

    def confirmation(self):
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        message = QMessageBox(self)
        if "'" not in self.player_name.text():
            check = cursor.execute(
                f"SELECT userid from USERS where users.name = '{self.player_name.text()}'").fetchone()
            if check:
                if self.line:  # если есть row(т.е. комментарий уже есть в базе данных, то обновляем его
                    cursor.execute(f'UPDATE USERCOMMENT SET score = "{self.user_score}", comment = '
                                   f'"{self.comment_section.toPlainText()}", userid= {check[0]} WHERE commentid = {self.line[0]};')
                else:
                    cursor.execute('INSERT INTO USERCOMMENT (score, comment, userid) VALUES (?, ?, ?)',
                                   # в ином случае создаем новый
                                   (self.user_score, self.comment_section.toPlainText(), check[0]))
                con.commit()
                con.close()
                self.lobby_obj.msg = DevWindow(self.lobby_obj)
                self.lobby_obj.msg.show()
            else:
                message.setText('Введите корректное имя пользователя\nОно должно быть уже введено в новой игре')
                message.show()
        else:
            message.setText("Имя не должно содержать апострафа")
            message.show()


class NewGameNicknamesWindow(QWidget, UiFormNewGameNicknamesWindow):
    def __init__(self, lobby_obj: QWidget):
        super().__init__()
        self.lobby_obj = lobby_obj
        self.initUI()

    def initUI(self):
        self.setupUi(self)

    def add_users(self):
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        name1 = self.first_player_line.text()
        name2 = self.second_player_line.text()
        if "'" not in name1 and "'" not in name2:
            first_check = cursor.execute(f'SELECT name from users WHERE users.name = "{name1}"').fetchone()
            second_check = cursor.execute(f'SELECT name from users WHERE users.name = "{name2}"').fetchone()

            if first_check and name1 in first_check:
                cursor.execute(f"UPDATE users SET amount_of_plays = amount_of_plays + 1 where users.name = '{name1}'")
            else:
                cursor.execute(f"INSERT INTO users (name, amount_of_plays) VALUES(?, ?)", (name1, 1))
            if second_check and name2 in second_check:
                cursor.execute(f"UPDATE users SET amount_of_plays = amount_of_plays + 1 where users.name = '{name2}'")
            else:
                cursor.execute(f"INSERT INTO users (name, amount_of_plays) VALUES(?, ?)", (name2, 1))
            con.commit()
            con.close()
            return True
        else:
            message = QMessageBox(self)
            message.setText("Имена не должны содержать апострафа")
            message.show()
            return False

    def back(self):
        self.close()

    def confirm(self):
        if self.first_player_line.text() != self.second_player_line.text():
            if self.add_users():
                self.msg = NewGame(self.first_player_line.text(), self.second_player_line.text())
                self.msg.show()
                self.close()
                self.lobby_obj.close()
        else:
            message = QMessageBox(self)
            message.setText('Нельзя играть с самим собой:<')
            message.show()


class NewGameNicknamesWindowBot(QWidget, UiFormNewGameNicknamesWindow):
    def __init__(self, lobby_obj: QWidget):
        super().__init__()
        self.lobby_obj = lobby_obj
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.second_player_line.setText('MODEL1')
        self.second_player_line.setEnabled(False)

    def add_users(self):
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        name1 = self.first_player_line.text()
        if "'" not in name1:
            first_check = cursor.execute(f'SELECT name from users WHERE users.name = "{name1}"').fetchone()
            if first_check and name1 in first_check:
                cursor.execute(f"UPDATE users SET amount_of_plays = amount_of_plays + 1 where users.name = '{name1}'")
            else:
                cursor.execute(f"INSERT INTO users (name, amount_of_plays) VALUES(?, ?)", (name1, 1))
            con.commit()
            con.close()
            return True
        else:
            message = QMessageBox(self)
            message.setText("Имя не должно содержать апострафа")
            message.show()
            return False

    def back(self):
        self.close()

    def confirm(self):
        if self.add_users():
            self.msg = NewGame(self.first_player_line.text(), "MODEL1", bot=1)
            self.msg.show()
            self.close()
            self.lobby_obj.close()


class NewGame(QWidget, UiFormBasicInterface):
    def __init__(self, name_player1, name_player2, amount_of_actions=0, general_time=0, fen=None, finished_game=0, bot=0):
        super().__init__()
        self.bot = bot
        self.name_player1 = name_player1
        self.name_player2 = name_player2
        self.amount_of_actions = amount_of_actions
        self.time_now = datetime.datetime.now()
        self.general_time = general_time
        self.game_finished = finished_game
        self.game = chess.Board()
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if fen:
            self.game = chess.Board(fen)
        self.row = None
        self.col = None
        self.last_figure = None
        self.unshow = 0
        self.pause_game_for_bot = 0
        self.flag_mouse = 0
        self.initUI()
        if self.bot:
            self.model = model
            self.model.load_state_dict(torch.load("last_model.pth"))
            self.model.eval()

    def initUI(self):
        self.setupUi(self)
        for i in range(8):
            for j in range(8):
                cell = QWidget()
                cell.label = QLabel(cell)
                name = str(self.game.piece_at(i * 8 + j))
                if name:
                    if name.lower() == name:
                        name = 'b' + name
                    else:
                        name = 'w' + name
                    im = QPixmap(f'sprites/{current_folder}/{name}.png')
                    cell.label.setPixmap(im)
                cell.label.setFixedSize(80, 80)
                cell.lower()
                cell.setObjectName(str(i) + str(j))
                cell.mousePressEvent = lambda event, cell=cell: self.mouse_click(event, cell)
                cell.mouseMoveEvent = lambda event: self.mouse_moving(event)
                cell.mouseReleaseEvent = lambda event: self.mouse_release(event)
                cell.setFixedSize(80, 80)
                self.grid.addWidget(cell, 7 - i, j)
                cell.setStyleSheet(f'background-image: url(board_cells/{7 - i}{j});')
        self.pause_label.raise_()
        self.finish_screen.hide()
        self.finish_screen.raise_()
        self.finish_screen.clicked.connect(self.finish_click)
        self.pause_label_for_promoting.raise_()
        self.pause_label.hide()
        self.pause_label_for_promoting.hide()
        self.pause_label.mouseReleaseEvent = self.pause_hide
        self.lbl.raise_()
        self.lbl.hide()
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def set_pix_maps(self):
        for i in range(8):
            for j in range(8):
                name = str(self.game.piece_at(i * 8 + j))
                if name:
                    if name.lower() == name:
                        name = 'b' + name
                    else:
                        name = 'w' + name
                    im = QPixmap(f'sprites/{current_folder}/{name}.png')
                    widget = self.grid.itemAtPosition(7 - i, j).widget()
                    widget.label.setPixmap(im)

    def mouse_click(self, event, cell):
        if event.button() == QtCore.Qt.LeftButton and not self.game_finished:
            widget_under_cursor = QApplication.instance().widgetAt(QCursor.pos())
            row, col = self.find_indexs_of_widget(widget_under_cursor)
            row = 7 - row # преобразуем в соответсвии с доской
            self.flag_mouse = 1
            if self.pause_label.isVisible():
                self.pause_label.hide()
            if self.last_figure and self.game.color_at(row * 8 + col) != self.game.turn:
                self.mouse_release(event)
            elif cell.label.pixmap():
                self.unshow_movements()
                self.last_figure = cell
                self.row, self.col = row, col
                self.show_movements()

    def find_indexs_of_widget(self, widget):
        for row in range(8):
            for col in range(8):
                item = self.grid.itemAtPosition(row, col).widget()
                if item.label == widget:
                    return row, col
        return None, None

    def mouse_moving(self, event):
        if self.row is not None and self.col is not None and self.last_figure.label.pixmap():
            self.event_pos = event.windowPos()
            self.lbl.move(int(self.event_pos.x()) - 40, int(self.event_pos.y()) - 40)
            self.lbl.setPixmap(self.last_figure.label.pixmap())
            self.lbl.show()

    def mouse_release(self, event):
        if event.button() == QtCore.Qt.LeftButton and not self.game_finished and not self.pause_game_for_bot:
            """hides the image of moving figure and checks all requests for releasing figure"""
            self.lbl.hide()
            self.flag_mouse = 0
            widget_under_cursor = QApplication.instance().widgetAt(QCursor.pos())
            if self.row is not None and self.col is not None and self.game.piece_at(self.row * 8 + self.col):
                row1, col1 = self.find_indexs_of_widget(widget_under_cursor)
                if row1 is not None and col1 is not None:
                    row1 = 7 - row1
                    self.move = self.letters[self.col] + str(self.row + 1) + self.letters[col1] + str(row1 + 1)# преобразуем в соответсвии с доской
                    if self.move in map(str, self.game.legal_moves) or self.move + 'q' in map(str, self.game.legal_moves):
                        self.make_move(self.move)
                        self.amount_of_actions += 1
                        self.change_label_color()
                        self.last_figure = None
                        self.row, self.col = None, None
                        self.unshow_movements()

    def make_move(self, move):
        flag = True
        row, row1 = int(move[1]) - 1, int(move[3]) - 1
        col, col1 = self.letters.index(move[0]), self.letters.index(move[2])
        piece = str(self.game.piece_at(row * 8 + col))
        if piece == "p" and row1 == 0 or piece == "P" and row1 == 7:
            self.init_promotion_gui(move)
            flag = False
        if flag:
            self.game.push_san(move)
            self.set_pix_maps()
            self.finish_if_can()
            self.btn_undo.setEnabled(True)
            if self.bot and not self.game_finished:
                self.pause_game_for_bot = 1
                self.btn_undo.setEnabled(False)
                self.set_pix_maps()
                self.bot_move()

    def bot_move(self):
        move, result = get_ai_move(self.model, self.game)
        print(move, result)
        self.game.push(move)
        self.finish_if_can()
        if len(self.game.move_stack) > 2:
            self.btn_undo.setEnabled(True)
        self.change_label_color()
        self.pause_game_for_bot = 0
        self.set_pix_maps()

    def undo(self):
        self.move = str(self.game.pop())
        if self.bot:
            self.move_2 = str(self.game.pop())
        self.winner_label.clear()
        self.change_label_color()
        self.amount_of_actions -= 1
        self.btn_undo.setEnabled(False)
        self.btn_redo.setEnabled(True)
        self.set_pix_maps()

    def redo(self):
        if self.bot:
            self.make_move(self.move_2)
        if not self.bot:
            self.make_move(self.move)
        self.change_label_color()
        self.amount_of_actions += 1
        self.btn_undo.setEnabled(True)
        self.btn_redo.setEnabled(False)
        self.set_pix_maps()

    def unshow_movements(self):
        self.unshow = 0
        for move in self.game.legal_moves:
            move = str(move)
            if self.letters.index(move[0]) == self.col and int(move[1]) == self.row + 1:
                row1 = int(move[3]) - 1
                col1 = self.letters.index(move[2])
                item = self.grid.itemAtPosition(7 - row1, col1).widget()
                if self.game.piece_at(row1 * 8 + col1):
                    color = 'w' if self.game.color_at(row1 * 8 + col1) else 'b'
                    item.label.setPixmap(
                        QPixmap(f"sprites/{current_folder}/{color}{str(self.game.piece_at(row1 * 8 + col1))}.png"))
                else:
                    item.label.clear()

    def show_movements(self):
        self.unshow = 1
        for move in self.game.legal_moves:
            move = str(move)
            if self.letters.index(move[0]) == self.col and int(move[1]) == self.row + 1:
                row1 = int(move[3]) - 1
                col1 = self.letters.index(move[2])
                item = self.grid.itemAtPosition(7 - row1, col1).widget()
                if self.game.piece_at(row1 * 8 + col1):
                    color = 'w' if self.game.color_at(row1 * 8 + col1) else 'b'
                    item.label.setPixmap(QPixmap(f"green/{color}{str(self.game.piece_at(row1 * 8 + col1))}.png"))
                else:
                    item.label.setPixmap(QPixmap("images/circle.png"))

    def finish_if_can(self):
        if self.game.outcome():
            res = self.game.outcome()
            if res.winner:
                text = 'Победили белые'
            elif res.winner is False:
                text = 'Победили черные'
            else:
                text = 'Ничья'
            self.winner_label.setText(text)
            self.finish_screen.setText(text)
            self.finish_screen.show()
            time = datetime.datetime.now() - self.time_now
            self.general_time += time.total_seconds()
            self.game_finished = 1
            self.btn_undo.setEnabled(False)

    def finish_click(self):
        self.finish_screen.hide()

    def init_promotion_gui(self, move):
        self.promotion_flag_finish = False
        figures = ['Q', "R", "B", "N"]
        text_color = 'w' if self.game.turn == 1 else 'b'
        self.btn_group = QButtonGroup()
        self.promote_widget = QWidget(self)
        self.btn_group.buttonClicked.connect(lambda event, move=move: self.promote_pawn_click(event, move))
        self.promote_widget.setFixedSize(350, 150)
        self.layer = QHBoxLayout(self.promote_widget)
        for i in range(len(figures)):
            self.promote_btn = QPushButton(self.promote_widget)
            self.promote_btn.setObjectName(text_color + figures[i])
            self.promote_btn.setFixedSize(80, 80)
            self.promote_btn.setStyleSheet(
                f"background-image: url(sprites/{current_folder}/{text_color}{figures[i]}.png);")
            self.btn_group.addButton(self.promote_btn)
            self.layer.addWidget(self.promote_btn)
        self.promote_widget.move(160, 300)
        self.promote_widget.raise_()
        self.promote_widget.show()
        self.pause_label_for_promoting.show()

    def promote_pawn_click(self, event, move):
        self.promotion_flag_finish = True
        char = event.objectName()[1]
        self.game.push_san(move + char)
        self.promote_widget.hide()
        self.pause_label_for_promoting.hide()
        self.finish_if_can()
        if self.bot and not self.game_finished:
            self.btn_undo.setEnabled(False)
            self.bot_move()
            self.finish_if_can()
        self.set_pix_maps()
        self.change_label_color()

    def change_label_color(self):
        self.labeL_can_go.setText(self.labeL_can_go.text()[0:4] + " Белых" if self.game.turn
                                  else self.labeL_can_go.text()[0:4] + ' Черных')

    def go_to_menu(self):
        self.second_form = AreUSureExit(self)
        self.second_form.show()

    def pause(self):
        if not self.game_finished:
            time = datetime.datetime.now() - self.time_now
            self.general_time += time.total_seconds()
            self.pause_label.show()

    def pause_hide(self, event):
        if not self.game_finished:
            self.time_now = datetime.datetime.now()
            self.pause_label.hide()

    def save(self):
        time = datetime.datetime.now() - self.time_now
        self.general_time += time.total_seconds()
        self.second_form = SaveDialog(self.name_player1, self.name_player2, self.amount_of_actions,
                                      self.general_time // 60, self.game.fen(), self.game_finished, self.bot)
        self.second_form.show()


class AreUSureExit(QWidget, UiFormAreYouSure):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.ok_or_cancel)

    def ok_or_cancel(self, event):
        if event.text() == 'OK':
            self.parent.close()
            examp.show()
            self.close()
        else:
            self.close()


class SaveDialog(QWidget, UiFormSaveDialog):
    def __init__(self, name1, name2, amount_of_actions, general_time, fen, game_finished, bot):
        super().__init__()
        self.name_player1 = name1
        self.name_player2 = name2
        self.amount_of_actions = amount_of_actions
        self.general_time = general_time
        self.fen = fen
        self.bot = bot
        self.game_finished = game_finished
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.save_or_close)

    def save_or_close(self, event):
        if event.text() == "Save":
            con = sqlite3.connect("datebase.db")
            cursor = con.cursor()
            cursor.execute("SELECT game_name FROM SAVES;")
            data_fetch = list(map(lambda x: x[0], cursor.fetchall()))
            if self.lineEdit.text() not in data_fetch:
                cursor.execute('INSERT INTO SAVES (game_name, firstname, secondname, amount_of_actions, '
                               'general_time) VALUES (?, ?, ?, ?, ?)',
                               (self.lineEdit.text(), self.name_player1, self.name_player2,
                                self.amount_of_actions, self.general_time))
                self.close()
            else:
                id = data_fetch.index(self.lineEdit.text())
                cursor.execute('UPDATE SAVES SET amount_of_actions = ?, '
                               'general_time = ? WHERE saveid=?;',
                               (self.amount_of_actions, self.general_time, id + 1))
                self.close()
            with open(f'saves/{self.lineEdit.text()}', 'w', encoding='utf-8') as f:
                for i in [self.fen, self.game_finished, self.bot]:
                    print(i, file=f)
            con.commit()
            con.close()

        else:
            self.close()


class AreUSureDeleteSave(QWidget, UiFormAreYouSure):
    def __init__(self, lobby: object, parent: object, id: int, name: str):
        super().__init__()
        self.lobby = lobby
        self.parent = parent
        self.id = id
        self.name = name
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.firstlabel.setText('Вы уверены, что хотите удалить сохранение?')
        self.secondlabel.setText('Это действие нельзя будет отменить')
        self.buttonBox.clicked.connect(self.ok_or_cancel)

    def ok_or_cancel(self, event):
        if event.text() == 'OK':
            con = sqlite3.connect("datebase.db")
            cursor = con.cursor()
            cursor.execute(f"DELETE FROM SAVES WHERE saveid={self.id};")
            if self.name in os.listdir('saves'):
                os.remove(f"saves/{self.name}")
            con.commit()
            con.close()
            self.parent.close()
            self.lobby.msg = OpenWindow(self.lobby)
            self.lobby.msg.show()
        self.close()


class OpenWindow(QWidget, UiFormStatisticsOpen):
    def __init__(self, lobby):
        super().__init__()
        self.msg = None
        self.lobby = lobby
        self.initUI()
        self.btn_games()

    def initUI(self):
        self.setupUi(self)
        self.labels = [QLabel("Имя первого Игрока:"), QLabel("Имя второго Игрока: "),
                       QLabel("Количество ходов:"), QLabel("Общее время ходов:")]
        self.horisontal = QHBoxLayout(self)
        self.horisontal.addWidget(self.scrollArea)
        self.vertical = QVBoxLayout(self)
        self.horisontal.addLayout(self.vertical)
        for i in self.labels:
            i.setStyleSheet(stylesheet_statistics_labels)
            self.vertical.addWidget(i)
        self.vertical.setAlignment(Qt.AlignTop)
        self.btn_open = QPushButton("Открыть")
        self.btn_delete = QPushButton("Удалить")
        self.btn_back = QPushButton("Назад")
        self.btn_open.setStyleSheet(stylesheet_normal_btn)
        self.btn_delete.setStyleSheet(stylesheet_normal_btn)
        self.btn_back.setStyleSheet(stylesheet_normal_btn)
        self.btn_open.clicked.connect(self.open)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.back)
        self.vertical.addWidget(self.btn_open)
        self.vertical.addWidget(self.btn_delete)
        self.vertical.addWidget(self.btn_back)
        self.btn_open.setEnabled(False)
        self.btn_delete.setEnabled(False)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.setBrush(QColor(51, 51, 51))
        qp.drawRect(0, 0, 265, 640)
        qp.end()

    def fetchall_data(self):
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM SAVES;")
        data_fetch = cursor.fetchall()
        con.close()
        return data_fetch

    def sql_data_btn(self, id):
        con = sqlite3.connect("datebase.db")
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM SAVES WHERE saveid={id};")
        line = cursor.fetchone()
        con.close()
        return line

    def back(self):
        self.close()

    def delete(self):
        self.secondform = AreUSureDeleteSave(self.lobby, self, self.id, self.info_open_game[1])
        self.secondform.show()

    def btn_games(self):
        self.vertical_frame = QVBoxLayout(self.frame)
        rows = self.fetchall_data()
        for row in rows:
            btn = QPushButton(row[1])
            btn.setMinimumHeight(50)
            btn.setStyleSheet(stylesheet_statistics_btns)
            btn.setObjectName(str(row[0]))
            self.vertical_frame.setAlignment(Qt.AlignTop)
            self.vertical_frame.addWidget(btn)
            btn.clicked.connect(self.click)

    def click(self):
        self.id = int(self.sender().objectName())
        row = self.sql_data_btn(self.id)
        self.btn_open.setEnabled(True)
        self.btn_delete.setEnabled(True)
        self.info_open_game = row
        for game_i, label_i in zip(row[2:], self.labels):
            label_i.setText(label_i.text().split(':')[0] + ': ' + str(game_i))

    def open(self):
        if self.info_open_game[1] in os.listdir('saves'):
            with open(f"saves/{self.info_open_game[1]}", 'r') as f:
                save_data = f.read().split('\n')
                fen = save_data[0]
                finished_game = save_data[1]
                bot = int(save_data[2])
            self.msg = NewGame(*self.info_open_game[2:], fen, int(finished_game), bot=bot)
            self.msg.show()
            self.close()
        else:
            message = QMessageBox(self)
            message.setText('Соответствующий файл не обнаружен в сохранениях')
            message.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    music_volume = 100
    music_muted = True
    current_folder = 'alpha'
    figures_with_circles(current_folder)
    examp = Lobby()
    examp.show()
    sys.exit(app.exec())
