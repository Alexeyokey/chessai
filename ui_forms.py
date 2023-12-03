from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from stylesheets import *


class UiFormLobby(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setMinimumSize(800, 600)
        Form.setStyleSheet('background-image: url("backgrounds/lobby_background_w.jpg");')
        self.centralwidg = QWidget()
        self.setCentralWidget(self.centralwidg)
        vertical = QVBoxLayout(self.centralwidg)
        vertical.setAlignment(Qt.AlignCenter)
        for i in Form.MENU:
            btn = QPushButton(i, self.centralwidg)
            vertical.addWidget(btn)
            btn.setStyleSheet(stylesheet_btn_lobby + 'font-size: 32px;')
            Form.menu_btns.append(btn)
        self.dev_btn = QPushButton('ОТЗЫВЫ\n РАЗРАБОТЧИКУ', self.centralwidg)
        self.dev_btn.setStyleSheet(stylesheet_btn_lobby + 'font-size: 24px;')
        vertical.addWidget(self.dev_btn)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Шахматы"))


class UiFormNewGameNicknamesWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.vertical = QVBoxLayout(self)
        notice = QLabel("Введите имена игроков для стаитистики:")
        notice.setAlignment(Qt.AlignHCenter)
        notice.setStyleSheet(stylesheet_labels_new_game_nicknames)
        first_player_label = QLabel('Имя первого игрока(белые):')
        first_player_label.setStyleSheet(stylesheet_labels_new_game_nicknames)
        self.first_player_line = QLineEdit()
        self.first_player_line.setMaxLength(15)
        self.first_player_line.setFixedSize(500, 50)
        self.first_player_line.setFont(QFont('Inter', 14))
        second_player_label = QLabel('Имя второго игрока(черные):')
        second_player_label.setStyleSheet(stylesheet_labels_new_game_nicknames)
        self.second_player_line = QLineEdit()
        self.second_player_line.setMaxLength(15)
        self.second_player_line.setFixedSize(500, 50)
        self.second_player_line.setFont(QFont('Inter', 14))
        confirmation_button = QPushButton('Подтвердить')
        confirmation_button.setStyleSheet(stylesheet_btn_confirmation)
        confirmation_button.clicked.connect(self.confirm)
        self.first_player_line.setStyleSheet(stylesheet_line_new_game_window)
        self.second_player_line.setStyleSheet(stylesheet_line_new_game_window)
        self.vertical.addWidget(notice)
        self.vertical.addWidget(first_player_label)
        self.vertical.addWidget(self.first_player_line)
        self.vertical.addWidget(second_player_label)
        self.vertical.addWidget(self.second_player_line)
        self.vertical.addWidget(confirmation_button)
        self.setWindowTitle("Начать игру")
        self.btn_back = QPushButton("Назад")
        self.btn_back.setStyleSheet(stylesheet_normal_btn)
        self.vertical.addWidget(self.btn_back)
        self.btn_back.clicked.connect(self.back)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class UiFormStatisticsOpen(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(800, 640)
        Form.setStyleSheet("QScrollArea {\n"
                           "    background-color: rgb(51, 51, 51);\n"
                           "}\n"
                           "\n"
                           "QScrollBar:vertical {\n"
                           "    background: rgb(45, 45, 68);\n"
                           "    margin: 15px 0px 15px 0px;\n"
                           "    width: 14px;\n"
                           " }\n"
                           "\n"
                           "QScrollBar::handle:vertical {    \n"
                           "    background-color: #D9D9D9;\n"
                           "   stroke-width: 1px;\n"
                           "   stroke: #000;\n"
                           "   filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));\n"
                           "    min-height: 30px;\n"
                           "    border-radius: 7px;\n"
                           "}\n"
                           "QScrollBar::handle:vertical:hover{    \n"
                           "    background-color: rgb(0, 0, 0);\n"
                           "}\n"
                           "QScrollBar::handle:vertical:pressed {    \n"
                           "    background-color: rgb(185, 0, 92);\n"
                           "}\n"
                           "\n"
                           "/* BTN TOP - SCROLLBAR */\n"
                           "QScrollBar::sub-line:vertical {\n"
                           "    border: none;\n"
                           "    background-color: rgb(59, 59, 90);\n"
                           "    height: 15px;\n"
                           "    border-top-left-radius: 7px;\n"
                           "    border-top-right-radius: 7px;\n"
                           "    subcontrol-position: top;\n"
                           "    subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-line:vertical:hover {    \n"
                           "    background-color: rgb(255, 0, 127);\n"
                           "}\n"
                           "QScrollBar::sub-line:vertical:pressed {    \n"
                           "    background-color: rgb(185, 0, 92);\n"
                           "}\n"
                           "\n"
                           "/* BTN BOTTOM - SCROLLBAR */\n"
                           "QScrollBar::add-line:vertical {\n"
                           "    border: none;\n"
                           "    background-color: rgb(59, 59, 90);\n"
                           "    height: 15px;\n"
                           "    border-bottom-left-radius: 7px;\n"
                           "    border-bottom-right-radius: 7px;\n"
                           "    subcontrol-position: bottom;\n"
                           "    subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::add-line:vertical:hover {    \n"
                           "    background-color: rgb(255, 0, 127);\n"
                           "}\n"
                           "QScrollBar::add-line:vertical:pressed {    \n"
                           "    background-color: rgb(185, 0, 92);\n"
                           "}\n"
                           "\n"
                           "\n"
                           "\n"
                           "\n"
                           "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                           "    background: none;\n"
                           "}\n"
                           "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                           "    background: none;\n"
                           "}\n"
                           "\n"
                           "\n"
                           "")
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 250, 600))
        self.scrollArea.setFixedSize(250, 600)
        self.scrollArea.setStyleSheet("border: 0px")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 234, 1518))
        self.scrollAreaWidgetContents.setStyleSheet("QWidget {\n"
                                                    "    background-color: rgb(51, 51, 51);\n"
                                                    "}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setStyleSheet("background-color: rgb(51, 51, 51);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class UiFormDevNew(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(600, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 250))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Окно отзыва разработчику"))
        self.pushButton.setText(_translate("Form", "Написать новый отзыв"))


class UiFormNewComment(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(600, 500)
        Form.setStyleSheet("ratio:: {\n"
                           "  float: left;\n"
                           "  pointer-events: none;\n"
                           "}\n"
                           "\n"
                           "ratio:not(:checked)>input {\n"
                           "  position: absolute;\n"
                           "  top: -9999px;\n"
                           "}\n"
                           "\n"
                           "ratio:not(:checked)>label {\n"
                           "  float: right;\n"
                           "  width: 1em;\n"
                           "  overflow: hidden;\n"
                           "  white-space: nowrap;\n"
                           "  cursor: pointer;\n"
                           "  font-size: 30px;\n"
                           "  color: #ccc;\n"
                           "}\n"
                           "\n"
                           "ratio:not(:checked)>label:before {\n"
                           "  content: \'★ \';\n"
                           "}\n"
                           "\n"
                           "ratio>input:checked~label {\n"
                           "  color: #ffc700;\n"
                           "}\n"
                           "\n"
                           "ratio:not(:checked)>label:hover,\n"
                           "ratio:not(:checked)>label:hover~label {\n"
                           "  color: #deb217;\n"
                           "}\n"
                           "\n"
                           "ratio>input:checked+label:hover,\n"
                           "ratio>input:checked+label:hover~label,\n"
                           "ratio>input:checked~label:hover,\n"
                           "ratio>input:checked~label:hover~label,\n"
                           "rate>label:hover~input:checked~label {\n"
                           "  color: #c59b08;\n"
                           "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.player_name = QLineEdit('Введите имя')
        self.player_name.setMaxLength(15)
        self.player_name.setFont(QFont('Inter', 14))
        self.verticalLayout.addWidget(self.player_name)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.buttongroup = QtWidgets.QButtonGroup(Form)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_5.setObjectName("radioButton_5")
        self.horizontalLayout.addWidget(self.radioButton)
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.horizontalLayout.addWidget(self.radioButton_3)
        self.horizontalLayout.addWidget(self.radioButton_4)
        self.horizontalLayout.addWidget(self.radioButton_5)
        self.buttongroup.addButton(self.radioButton)
        self.buttongroup.addButton(self.radioButton_2)
        self.buttongroup.addButton(self.radioButton_3)
        self.buttongroup.addButton(self.radioButton_4)
        self.buttongroup.addButton(self.radioButton_5)
        self.radioButton.setFont(QFont('Inter', 12))
        self.radioButton_2.setFont(QFont('Inter', 12))
        self.radioButton_3.setFont(QFont('Inter', 12))
        self.radioButton_4.setFont(QFont('Inter', 12))
        self.radioButton_5.setFont(QFont('Inter', 12))
        self.confirmation_btn = QtWidgets.QPushButton('Подтвердить')
        self.verticalLayout.addWidget(self.groupBox)
        self.label_left_opinion = QtWidgets.QLabel(Form)
        self.label_left_opinion.setObjectName("label_left_opinion")
        self.label_left_opinion.setFont(QFont('Inter', 14))
        self.verticalLayout.addWidget(self.label_left_opinion)
        self.comment_section = QtWidgets.QTextEdit(Form)
        self.comment_section.setObjectName("comment_section")
        self.verticalLayout.addWidget(self.comment_section)
        self.verticalLayout.addWidget(self.confirmation_btn)
        self.confirmation_btn.setEnabled(False)  # нельзя отправить отзыв, не поставив оценку
        self.confirmation_btn.clicked.connect(self.confirmation)
        self.buttongroup.buttonToggled.connect(self.click)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Оставьте мнение"))
        self.radioButton_5.setText(_translate("Form", "5"))
        self.radioButton_4.setText(_translate("Form", "4"))
        self.radioButton_3.setText(_translate("Form", "3"))
        self.radioButton.setText(_translate("Form", "1"))
        self.radioButton_2.setText(_translate("Form", "2"))
        self.label_left_opinion.setText(_translate("Form", "Оставьте развернутое мнение об игре:"))


class UiFormAreYouSure(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.firstlabel = QtWidgets.QLabel(Form)
        self.firstlabel.setStyleSheet("font: 16pt \"Segoe UI Symbol\";")
        self.firstlabel.setObjectName("firstlabel")
        self.verticalLayout.addWidget(self.firstlabel)
        self.secondlabel = QtWidgets.QLabel(Form)
        self.secondlabel.setStyleSheet("font: 12pt \"Segoe UI\";")
        self.secondlabel.setObjectName("secondlabel")
        self.verticalLayout.addWidget(self.secondlabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Are you sure?"))
        self.firstlabel.setText(_translate("Form", "Вы уверены, что хотите выйти?"))
        self.secondlabel.setText(_translate("Form", "Игра не сохраняется автоматически"))


class UiFormSaveDialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setMaxLength(15)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(QFont('Inter', 14))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название партии:"))


class UiFormBasicInterface(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.pause_label = QLabel('ПАУЗА\nкликните, чтобы продолжить', self)
        self.pause_label.setStyleSheet("background-color: rgba(0, 0, 0, 50);"
                                       "color: white;"
                                       "font-size: 24px;")
        self.pause_label_for_promoting = QLabel(self)
        self.pause_label_for_promoting.setStyleSheet("background-color: rgba(0, 0, 0, 50);")
        self.finish_screen = QPushButton(self)
        self.finish_screen.setStyleSheet("background-color: rgba(0, 0, 0, 50);"
                                         "color: white;"
                                         "font-size: 48px;")
        self.pause_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pause_label.resize(700, 800)
        self.finish_screen.resize(700, 800)
        self.pause_label_for_promoting.resize(700, 800)
        self.lbl = QLabel(self)
        self.lbl.setFixedSize(80, 80)
        self.vertical = QVBoxLayout(self)
        self.frame = QHBoxLayout()
        self.grid = QGridLayout()
        self.vertical.addLayout(self.frame)
        self.vertical.addLayout(self.grid)
        self.grid.setSpacing(0)
        self.btn_pause = QPushButton()
        self.btn_save = QPushButton()
        self.btn_save.setMinimumHeight(50)
        self.btn_save.setStyleSheet(stylesheet_labels_new_game_nicknames)
        self.btn_undo = QPushButton()
        self.btn_redo = QPushButton()
        self.menu_btn = QPushButton()
        self.menu_btn.setStyleSheet(stylesheet_labels_new_game_nicknames)
        self.menu_btn.setMinimumHeight(50)
        self.btn_pause.setFixedSize(80, 50)
        self.btn_undo.setFixedSize(80, 50)
        self.btn_redo.setFixedSize(80, 50)
        self.btn_pause.clicked.connect(self.pause)
        self.menu_btn.clicked.connect(self.go_to_menu)
        self.btn_redo.clicked.connect(self.redo)
        self.btn_redo.setEnabled(False)
        self.btn_undo.clicked.connect(self.undo)
        self.btn_undo.setEnabled(False)
        self.btn_save.clicked.connect(self.save)
        self.frame.addWidget(self.btn_undo)
        self.frame.addWidget(self.btn_pause)
        self.frame.addWidget(self.btn_redo)
        self.frame.addWidget(self.btn_save)
        self.frame.addWidget(self.menu_btn)
        self.winner_label = QLabel()
        winner_horisontal_layout = QHBoxLayout()
        self.vertical.addLayout(winner_horisontal_layout)
        winner_horisontal_layout.addWidget(self.winner_label)
        self.labeL_can_go = QLabel('Ход:')
        winner_horisontal_layout.addWidget(self.labeL_can_go)
        self.change_label_color()
        self.retranslateUi(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Игра"))
        self.btn_save.setText(_translate("Form", "save game"))
        self.menu_btn.setText(_translate("Form", "main menu"))
        self.btn_undo.setText(_translate("Form", "<--"))
        self.btn_redo.setText(_translate("Form", "-->"))
        self.btn_pause.setText(_translate("Form", "||"))


class UiFormSettings(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(600, 275)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.label.setStyleSheet(stylesheet_general_label)
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_2.addWidget(self.horizontalSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setStyleSheet(stylesheet_general_label)
        self.verticalLayout.addWidget(self.checkBox)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(stylesheet_normal_btn)
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setFixedHeight(30)
        self.lineEdit.setFont(QFont('Inter', 14))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(stylesheet_normal_btn)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.btn_back = QtWidgets.QPushButton(Form)
        self.btn_back.setObjectName("btn_back")
        self.verticalLayout.addWidget(self.btn_back)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройки"))
        self.label.setText(_translate("Form", "Громкость музыки"))
        self.checkBox.setText(_translate("Form", "Отключить музыку"))
        self.label_2.setText(_translate("Form", "Выберите папку со спрайтами шахмат\n(по умолчанию alpha):"))
        self.pushButton_2.setText(_translate("Form", "Изменить спрайт"))
        self.btn_back.setText(_translate("Form", "Назад"))
