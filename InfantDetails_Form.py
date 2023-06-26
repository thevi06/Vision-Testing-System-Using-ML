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

        # Set up the blue underline
        underline = QLabel()
        underline.setStyleSheet("background-color: #869EF4;")
        underline.setFixedHeight(2)

        # Get the width of the text and add padding of 20 pixels on each side
        text_width = heading_label.fontMetrics().boundingRect(heading_label.text()).width() + 2
        underline.setFixedWidth(text_width)

        # Create a layout to hold the heading and underline
        heading_layout = QVBoxLayout()
        heading_layout.addWidget(heading_label)
        heading_layout.addWidget(underline)

        # Add the heading layout to the container layout
        container_layout.addLayout(heading_layout)

        # Create the icon widget and add it to the container layout
        icon = QLabel(self)
        pixmap = QPixmap('ECTALogo.png').scaledToHeight(90)  # Set the height of the pixmap to 50 pixels
        pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
        icon.setPixmap(pixmap)
        icon.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align the icon to the top

        # Create a vertical spacer item to push the form elements to the top of the container
        vspacer = QWidget(self)
        vspacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a horizontal layout to add the vertical spacer, icon and spacer to the container layout
        hbox = QHBoxLayout()
        hbox.addWidget(heading_label)
        hbox.addWidget(vspacer)
        hbox.addWidget(icon)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)