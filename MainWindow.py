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