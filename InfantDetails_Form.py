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

    def __init__(self):
        super().__init__()
        self.connect_to_db = False
        # Create the database and table
        self.create_database_and_table()
        self.database = MyWidget()

        # Set the window size as a percentage of the screen size
        screen_size = QApplication.primaryScreen().availableGeometry()
        width_percent = 0.5
        height_percent = 0.6
        self.setGeometry(
            int((1 - width_percent) * screen_size.width() / 2),
            int((1 - height_percent) * screen_size.height() / 2),
            int(width_percent * screen_size.width()),
            int(height_percent * screen_size.height())
        )

        # Set the background color to blue
        self.setStyleSheet("background-color: #D0DAFF;")

        self.setWindowTitle("ECTA")

        # Create a white container in the middle of the page
        container = QWidget(self)
        container.setStyleSheet("background-color: white;")

        container_layout = QVBoxLayout()

        # Create the heading label and add it to the container layout
        heading_label = QLabel("Infants Details Form", self)
        heading_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        heading_label.setStyleSheet("color: #3136AF;")  # Set the text color to blue