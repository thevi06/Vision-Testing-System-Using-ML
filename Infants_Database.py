from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QPainter, QColor
import mysql.connector

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        # Create main layout
        self.layout = QVBoxLayout()

        # Create container widget
        self.container_widget = QWidget()

        # Set background color of container widget and table widget to white
        self.container_widget.setStyleSheet("background-color: white;")
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("background-color: white;")

        # Create heading label
        self.heading_label = QLabel("Ecta Infant Database")
        self.heading_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px; margin-bottom: 10px;")

        # Create button layout
        self.button_layout = QHBoxLayout()

        # Create buttons
        self.login_button = QPushButton("Return to LOGINPAGE")
        self.testing_button = QPushButton("SELECT & START TESTING")
        self.home_button = QPushButton("RETURN TO HOME PAGE")

        # Set background color of buttons to gray
        self.login_button.setStyleSheet("background-color: #D9D9D9;")
        self.testing_button.setStyleSheet("background-color: #D9D9D9;")
        self.home_button.setStyleSheet("background-color: #D9D9D9;")

        # Add buttons to button layout
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.testing_button)
        self.button_layout.addWidget(self.home_button)

        # Add heading label, table widget, and button layout to container widget
        self.container_layout = QVBoxLayout()
        self.container_layout.addWidget(self.heading_label)
        self.container_layout.addWidget(self.table_widget)
        self.container_layout.addLayout(self.button_layout)
        self.container_widget.setLayout(self.container_layout)

        # Add container widget to main layout
        self.layout.addWidget(self.container_widget)

        # Set main layout for widget
        self.setLayout(self.layout)

        # Set background color of main window to blue
        self.setStyleSheet("background-color: #D0DAFF;")

        # Initialize UI
        self.initUI()