from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5 import uic
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
import mediapipe as mp
import cv2 as cv
import json
import math
from time import time
from Signin_Login_Page import Login
import os

with open("parameters.json", "r") as read_file:
    param = json.load(read_file)


def file_path_create():
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Get the desktop path
    folder_name = "result_1"  # Set the folder name
    #folder_path = os.path.join(desktop_path, folder_name)  # Create the full path to the new folder
    folder_path = "result"
    print(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the new folder
    else:
        print("Folder already exists.")
    return folder_path