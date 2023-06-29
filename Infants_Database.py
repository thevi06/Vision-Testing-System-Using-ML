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