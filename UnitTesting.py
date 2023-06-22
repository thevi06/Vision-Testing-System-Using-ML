import unittest
from MainWindow import euclidean_distance
import numpy as np
import cv2

class TestIrisDetails(unittest.TestCase):

    def test_iris_details(self):
        # create mock input data
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        points = np.array(points)

        # calculate expected output
        expected_center = (0.5, 0.5)
        expected_radius = 0.7071067811865476

        # call the function with mock input data
        (center, radius) = cv2.minEnclosingCircle(points)

        # check if the actual output matches the expected output
        self.assertAlmostEqual(center[0], expected_center[0], places=2)
        self.assertAlmostEqual(center[1], expected_center[1], places=2)
        self.assertAlmostEqual(radius, expected_radius, places=2)

class TestEuclideanDistance(unittest.TestCase):

    def test_euclidean_distance(self):
        # create mock input data
        point1 = (0, 0)
        point2 = (3, 4)

        # calculate expected output
        expected_distance = 5

        # call the function with mock input data
        distance = euclidean_distance(point1, point2)

        # check if the actual output matches the expected output
        self.assertAlmostEqual(distance, expected_distance, places=2)