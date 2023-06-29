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