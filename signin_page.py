import sys
import mysql.connector
from mysql.connector import errorcode
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QStackedWidget, QLabel, \
    QLineEdit, QSizePolicy, QGridLayout, QDateEdit, QComboBox, QMessageBox, QMainWindow
from InfantDetails_Form import MyPage

class Login(QWidget):  # Login Page
    login_signal =pyqtSignal()
    def __init__(self):
        super().__init__()
        self.signUp = Signup()
        self.my_page = MyPage()
        self.signUp.send_data.connect(self.send_data)
        self.connect_to_db_done = True
        self.input_details_correct = False
        self.msg = QMessageBox

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

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Username'].setPlaceholderText("Username")
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setPlaceholderText("Password")
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Login'], 0, 0, 1, 1)

        layout.addWidget(labels['Username'], 2, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'], 2, 1, 1, 2)

        layout.addWidget(labels['Password'], 3, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'], 3, 1, 1, 2)

        layout.addWidget(labels['register'], 6, 0, 1, 2)

        button_login = QPushButton('&Log In', clicked=self.checkcredential)  ####Login Button Click ######
        layout.addWidget(button_login, 4, 2, 1, 1)
        button_register = QPushButton('&Signup', clicked=self.open_second_gui)  ####Signup page button#####
        layout.addWidget(button_register, 6, 2, 1, 1)

        self.status = QLabel('')  #########Validate Error Message##########
        self.status.setStyleSheet('font-size: 13px; color: red;')
        layout.addWidget(self.status, 4, 0, 1, 1)

    def connect_to_db(self):
        try:
            cnx = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password="",
                                          database="users",
                                          autocommit=True)
            self.cursor = cnx.cursor()
            print("Connected to database")
            self.connect_to_db_done = True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # Create the database and table if they don't exist
                cnx = mysql.connector.connect(host="localhost",
                                              user="root",
                                              password="",
                                              autocommit=True)
                self.cursor = cnx.cursor()
                try:
                    self.cursor.execute("CREATE DATABASE users")
                    print("Created database")
                except mysql.connector.Error as err:
                    print(f"Failed creating database: {err}")
                try:
                    self.cursor.execute("USE users")
                    self.cursor.execute(
                        "CREATE TABLE usertable (first_name VARCHAR(255),last_name VARCHAR(255),username VARCHAR(255),"
                        "user_password VARCHAR(255),mobile_number INT,nic VARCHAR(255) PRIMARY KEY,date_of_birth DATE,"
                        "gender VARCHAR(255));")
                    print("Created table")
                except mysql.connector.Error as err:
                    print(f"Failed creating table: {err}")

    def checkcredential(self):
        if self.connect_to_db_done is True:
            username = self.lineEdits['Username'].text()
            password = self.lineEdits['Password'].text()

            query = "SELECT * FROM `usertable`WHERE username= %s and user_password= %s "  #####select username and password form database######
            value = (username, password)
            self.cursor.execute(query, value)
            results = self.cursor.fetchone()  ######assign password and username to a variable#######
            self.lineEdits['Username'].setText("")
            self.lineEdits['Password'].setText("")

            if len(username):
                if len(password):
                    if results:
                        self.status.setText(
                            'all ok')
                        self.my_page.show()
                        self.my_page.start_signal.connect(self.send_signal)
                        self.hide()
                        self.my_page.close_gignal.connect(self.show)
                        ###########check if password and username exist in the database############
                        # self.lineEdits['Username'].setText("")
                        # self.lineEdits['Password'].setText("")
                        else:
                        self.status.setText('User or Password is wrong')
                        # self.lineEdits['Username'].setText("")
                        # self.lineEdits['Password'].setText("")
                else:
                    self.status.setText('enter password')
                else:
                self.status.setText('enter username')
        else:
            QMessageBox.critical(self, "Error", "No Data Base. Contact the IT team")