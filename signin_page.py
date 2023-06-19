import sys
import mysql.connector
from mysql.connector import errorcode
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QStackedWidget, QLabel, \
    QLineEdit, QSizePolicy, QGridLayout, QDateEdit, QComboBox, QMessageBox, QMainWindow
from InfantDetails_Form import MyPage