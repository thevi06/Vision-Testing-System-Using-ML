from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QPainter, QColor
import mysql.connector

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        # Create main layout
        self.layout = QVBoxLayout()