import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window size
        self.setGeometry(100, 100, 1800, 900)

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 200, 200)
        self.image_label.setPixmap(QPixmap("image.png").scaled(200, 200))

        # Set the initial position of the object
        self.x = 0
        self.y = 0

        # Create a timer to update the object's position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)  # Update every 50 milliseconds