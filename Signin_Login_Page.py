import sys
import mysql.connector
from mysql.connector import errorcode
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QStackedWidget, QLabel, \
    QLineEdit, QSizePolicy, QGridLayout, QDateEdit, QComboBox, QMessageBox, QMainWindow
from InfantDetails_Form import MyPage

class Login(QWidget):  # Login Page
    login_signal =pyqtSignal()
    sendcursor = pyqtSignal(object)

    def __init__(self):
        super().__init__()


        #self.signUp = Signup()
        self.my_page = MyPage()

        self.connect_to_db_done = True
        self.input_details_correct = False
        self.msg = QMessageBox

        self.connect_to_db()
        self.signUp = Signup()
        self.signUp.sendSignal.connect(self.getData)

        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 350
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()  # Layout
        fulllayout = QHBoxLayout()
        self.setLayout(fulllayout)

        imglabel = QLabel(self)  # image
        pixmap = QPixmap('baby.jpg')
        imglabel.setPixmap(pixmap)
        fulllayout.addWidget(imglabel)
        fulllayout.addLayout(layout)

        imglabel1 = QLabel(self)  # Logo
        pixmap = QPixmap('logoMINI.JPG')
        imglabel1.setPixmap(pixmap)
        imglabel1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(imglabel1, 0, 2)

        labels = {}  # Labels and Input fields
        self.lineEdits = {}

        labels['Login'] = QLabel('Login')
        labels['Login'].setStyleSheet('font-size: 25px; color: blue;')
        labels['Username'] = QLabel('Username')
        labels['Password'] = QLabel('Password')
        labels['register'] = QLabel("Don't have an account? Signup")
        labels['register'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Login'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)