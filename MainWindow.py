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

# give euclidean distance of two points
def euclidean_distance(point1, point2):
    return math.dist(point1, point2)


# get center and the radius of iris
def iris_details(points):
    (r_x, r_y), r_radius = cv.minEnclosingCircle(points)
    return (r_x, r_y), r_radius


# normalize distance of points
def normalized_distance(distance, total_distance):
    return round((distance / total_distance), 2)

# convert rectangular to polar coordinates
def polar_coordinates(point1, point2):
    x1 = point1[0] - point2[0]
    y1 = point1[1] - point2[1]
    rho = math.sqrt(math.pow(x1, 2) + math.pow(y1, 2)) / (point2[2] + 1e-6)
    theta = abs(math.degrees(math.atan(y1 / (x1 + 1e-6))))

    if x1 > 0 and y1 > 0:
        theta = 360 - theta

    if x1 > 0 and y1 < 0:
        theta = theta

    if x1 < 0 and y1 < 0:
        theta = 180 - theta

    if x1 < 0 and y1 > 0:
        theta = 180 + theta

    return rho, theta

# get the initial details of the iris point
def get_initial_details_of_center_of_the_eye(face_points, iris_points, eye_points, delay_time):
    reference_points = np.zeros((1, 3))
    start_time = time()

    while time() - start_time < delay_time:
        points = face_points[iris_points]
        (x, y), radius = cv.minEnclosingCircle(points)
        reference_points = np.append(reference_points, [[x, y, radius]], axis=0)

    mean_reference_point = np.mean(reference_points, axis=0, dtype=np.int32)

    width = euclidean_distance(face_points[eye_points[0]], face_points[eye_points[1]])
    height = euclidean_distance(face_points[eye_points[2]], face_points[eye_points[3]])

    center_to_left_corner_horizontal_width = euclidean_distance(mean_reference_point[:2],
                                                                face_points[eye_points[0]]) / width + 1e-6
    center_to_up_vertical_height = euclidean_distance(mean_reference_point[:2],
                                                      face_points[eye_points[2]]) / height + 1e-6

    return mean_reference_point, center_to_left_corner_horizontal_width, center_to_up_vertical_height

def current_position_details(face_points):
    # "minEnclosingCircle" opencv for finding the smallest circle
    (x, y), radius = cv.minEnclosingCircle(face_points)
    return [int(x), int(y), int(radius)]


def filter_current_position(current_point, reference_point):
    position_vector = np.zeros(9)
    rho, theta = polar_coordinates(current_point, reference_point)
    if rho < 0.2:
        position_vector[0] = 1
        # print("center")
    if rho > 0.2 and 160 < theta < 200:
        position_vector[1] = 1
        # print("left")
    if rho > 0.2 and 0 <= theta <= 20 or 340 <= theta <= 360:
        position_vector[2] = 1
        # print("right")
    if rho > 0.2 and 70 <= theta <= 110:
        position_vector[3] = 1
        # print("up")
    if rho > 0.2 and 250 <= theta <= 290:
        position_vector[4] = 1
        # print("down")
    if rho > 0.2 and 20 < theta < 70:
        position_vector[5] = 1
        # print("right upper")
    if rho > 0.2 and 110 < theta < 160:
        position_vector[6] = 1
        # print("left upper")
    if rho > 0.2 and 200 < theta < 250:
        position_vector[7] = 1
        # print("left lower")
    if rho > 0.2 and 290 < theta < 340:
        position_vector[8] = 1
        # print("right lower")
    return position_vector

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('main.ui', self)

        self.login = Login()
        self.login.show()
        self.hide()

        self.file_path = "C:\\Users\\senar\\OneDrive\\Desktop\\Report"

        self.vector = np.zeros(9)
        self.x = 550
        self.y = 275

        self.login.login_signal.connect(self.access)
        self.pushButtonStart.clicked.connect(self.start)
        self.pushButtonStop.clicked.connect(self.stop)
        self.pushButtonPause.clicked.connect(self.pause)

        self.Image_label = QLabel(self)
        self.Image_label.setGeometry(self.x, self.y, 100, 100)
        self.Image_label.setPixmap(QPixmap("butterfly.png").scaled(100, 100))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)

        self.thread_process = process_thread(self.file_path)
        self.thread_process.position_vector_signal.connect(self.get_information)

        self.result_left = result("left", self.file_path)
        self.result_right = result("right", self.file_path)

        def access(self):
            self.show()

        def start(self):
            self.thread_process.start_process()
            self.result_left.start_get_result()
            self.result_right.start_get_result()
            s_time = time()
            while time() - s_time < 8:
                continue
            self.x = 0
            self.y = 0
            self.timer.start(100)

        def stop(self):
            self.timer.stop()
            self.x = 550
            self.y = 275
            self.Image_label.move(self.x, self.y)
            self.thread_process.stop_process()
            self.result_left.cal_result()
            self.result_right.cal_result()
            # self.result_left.stop_get_result()
            # self.result_right.stop_get_result()
            print("stop")

        def pause(self):
            # Pause the timer
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start(10)

        def update_position(self):
            # Move the object in a square shape
            if self.x < 1480 and self.y == 0:
                self.x += 5
            elif self.x == 1480 and self.y < 570:
                self.y += 5
            elif self.x > 0 and self.y == 570:
                self.x -= 5
            elif self.x == 0 and self.y > 0:
                self.y -= 5

            # Set the position of the object
            self.Image_label.move(self.x, self.y)

            # x value of center,  center y  value, center y value
            center = (550, 275, 275)
            self.vector = filter_current_position((self.x, self.y, 275), center)

    def get_information(self, left_vector, right_vector):
        self.result_left.process(left_vector, self.vector)
        self.result_right.process(right_vector, self.vector)

class result(QThread):

    def __init__(self, side, file_path):
        super(result, self).__init__()
        self.side = side
        self.file_path = file_path
        self.center = np.zeros((1, 9))
        self.left = np.zeros((1, 9))
        self.right = np.zeros((1, 9))
        self.up = np.zeros((1, 9))
        self.down = np.zeros((1, 9))
        self.left_upper = np.zeros((1, 9))
        self.left_lower = np.zeros((1, 9))
        self.right_upper = np.zeros((1, 9))
        self.right_lower = np.zeros((1, 9))

    def start_get_result(self):
        self.start()

    def stop_get_result(self):
        self.wait()

    def process(self, vector, ref_vector):
        if ref_vector[0] == 1 and np.array_equiv(vector, ref_vector):
            self.center = np.append(self.center, [vector], axis=0)
        elif ref_vector[1] == 1 and np.array_equiv(vector, ref_vector):
            self.left = np.append(self.left, [vector], axis=0)
        elif ref_vector[2] == 1 and np.array_equiv(vector, ref_vector):
            self.right = np.append(self.right, [vector], axis=0)
        elif ref_vector[3] == 1 and np.array_equiv(vector, ref_vector):
            self.up = np.append(self.up, [vector], axis=0)
        elif ref_vector[4] == 1 and np.array_equiv(vector, ref_vector):
            self.down = np.append(self.down, [vector], axis=0)
        elif ref_vector[5] == 1 and np.array_equiv(vector, ref_vector):
            self.right_upper = np.append(self.right_upper, [vector], axis=0)
        elif ref_vector[6] == 1 and np.array_equiv(vector, ref_vector):
            self.left_upper = np.append(self.left_upper, [vector], axis=0)
        elif ref_vector[7] == 1 and np.array_equiv(vector, ref_vector):
            self.left_lower = np.append(self.left_lower, [vector], axis=0)
        elif ref_vector[8] == 1 and np.array_equiv(vector, ref_vector):
            self.left_lower = np.append(self.right_lower, [vector], axis=0)

    def cal_result(self):
        center_result = np.mean(self.center, axis=0)
        left_result = np.mean(self.left, axis=0)
        right_result = np.mean(self.right, axis=0)
        up_result = np.mean(self.up, axis=0)
        down_result = np.mean(self.down, axis=0)
        right_upper_result = np.mean(self.right_upper, axis=0)
        left_upper_result = np.mean(self.left_upper, axis=0)
        left_lower_result = np.mean(self.left_lower, axis=0)
        right_lower_result = np.mean(self.right_lower, axis=0)

        with open(os.path.join(self.file_path, "init.txt"), "a") as file:
            file.write(f'\n\n'
                       f'{self.side} eye tracking details\n'
                       f'center details      : average tracking {str(center_result[0])} \n'
                       f'left details        : average tracking {str(left_result[1])} \n'
                       f'right details       : average tracking {str(right_result[2])} \n'
                       f'up details          : average tracking {str(up_result[3])} \n'
                       f'down details        : average tracking {str(down_result[4])} \n'
                       f'right upper details : average tracking {str(right_upper_result[5])} \n'
                       f'left upper details  : average tracking {str(left_upper_result[6])} \n'
                       f'left lower details  : average tracking {str(left_lower_result[7])} \n'
                       f'right lower details : average tracking {str(right_lower_result[8])} \n\n')

face_mesh_points = mp.solutions.face_mesh


class process_thread(QThread):
    # values inside the parameters can be taken out
    position_vector_signal = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, file_path):
        super(process_thread, self).__init__()

        self.position_vector = np.zeros((1, 9))
        self.process_status = True
        self.time_delay = 1
        self.file_path = file_path

    def start_process(self):
        self.process_status = True
        self.start()

    def stop_process(self):
        self.process_status = False
        self.wait()