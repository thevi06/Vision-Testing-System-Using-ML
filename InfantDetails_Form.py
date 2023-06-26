import os
import re
import datetime
import mysql.connector
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGridLayout, QCheckBox, \
    QPushButton, QDateEdit, QFormLayout, QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from Infants_Database import MyWidget

class MyPage(QWidget):

    start_signal = pyqtSignal()
    close_signal = pyqtSignal(bool)