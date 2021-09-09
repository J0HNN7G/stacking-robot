# -*- coding: utf-8 -*-

import error
from component import Component

import math
from adafruit_servokit import ServoKit
from picamera import PiCamera
import cv2
import numpy as np

class Head(Component):
    """A class for controlling the head of the robot."""


    # The domain of the function which controls the view angle.
    VIEW_DOM = 100

    # The actual range of the view angle.
    VIEW_RNG = 60

    # The number of times we measure the distance to an object.
    NUM_TRIES = 10

    # Distance from axis of rotation for the head and the ultrasonic sensor
    AX_TO_SEN = math.sqrt(0.0265 ** 2 + 0.025 ** 2)

    # difference between x values of the shoulder axis to axis of rotation for the head
    X_ORIG_TO_AX = -0.0375

    # difference between y values of the shoulder axis to axis of rotation for the head
    Y_ORIG_TO_AX = -0.0475

    # Conversion factor from radians to degrees.
    DEG_TO_RAD = math.pi / 180

    # Precision of object coordinates calculated with ultrasonic sensor
    PRECISION = 3

    # Camera resolution width in pixels.
    IMG_WIDTH = 640

    # Camera resolution height in pixels.
    IMG_HEIGHT = 480

    # Horizontal center of camera images in pixels.
    CENTER_IMG_X = IMG_WIDTH // 2

    # Vertical center of camera images in pixels.
    CENTER_IMG_Y = IMG_HEIGHT // 2

    # Minimum area of object in image.
    MIN_AREA = 250

    # Maximum area of object in image.
    MAX_AREA = 10 ** 5

    # Camera framerate.
    FRAMERATE = 32

    # Minimum yellow HSV.
    Y_HSV_MIN = np.array([17,100,50])

    # Maximum yellow HSV.
    Y_HSV_MAX = np.array([37,255,255])

    # Minimum blue HSV.
    B_HSV_MIN = np.array([108,100,50])

    # Maximum blue HSV.
    B_HSV_MAX = np.array([118,255,255])

    # Minimum red HSV.
    R_HSV_MIN = np.array([169,100,50])

    # Maximum red HSV.
    R_HSV_MAX = np.array([179,255,255]))


    def __init__(self, viewPin, ultra):
        """
        Initialise the head view movement.

        :param viewPin: PCA9685 numbering of the pin controlling the head
        :raise ValueError: if viewPin is not a PCA9685 numbering
        """
        error.checkPCA9685(viewPin)

        self.status = False
        kit = ServoKit(channels=16)
        self._view = kit.servo[viewPin]
        self.ultra = ultra


    def setup(self):
        """
        Setup the view to be at the standard angle.
        """
        self._view.angle = self.VIEW_DOM

        if not self.ultra.status:
            self.ultra.setup()

        self.status = True


    def cleanup(self):
        """
        Cleanup the view by turning off the servo.
        """
        self._view.angle = None
        self.ultra.cleanup()
        self.status = False


    @property
    def view(self):
        """
        Get the actual view angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :return: view angle in degrees
        """
        return round(self.VIEW_RNG * (1 - self._view.angle / self.VIEW_DOM), 0)


    @view.setter
    def view(self, angle):
        """
        Set the view angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :param angle: view angle in degrees
        :raise ValueError: if the angle is not between 0 to 60, or
                           the head is off
        """
        error.checkComponent(self, 'Head')
        error.checkInRange(angle, 0, self.VIEW_RNG)
        self._view.angle = self.VIEW_DOM * (1 - angle / self.VIEW_RNG)


    def objPos(self):
        """
        Calculate the cartesian coordinates of an object with the ultrasonic
        sensor relative to the axis of the shoulder.

        :return: the cartesian position of the object in metres relative to the
                 axis of the shoulder
        :raise ValueError: if the ultrasonic sensor is off
        """
        error.checkComponent(self.ultra, 'Ultrasonic sensor')

        senToObj = self.ultra.meanAdjDist(self.NUM_TRIES)

        print(senToObj)
        x = self.X_ORIG_TO_AX + self.AX_TO_SEN * math.cos(self.view * self.DEG_TO_RAD + (3/4)*math.pi) \
            - senToObj * math.cos(self.view * self.DEG_TO_RAD)
        y = self.Y_ORIG_TO_AX + self.AX_TO_SEN * math.sin(self.view * self.DEG_TO_RAD - (1/4)*math.pi) \
            + senToObj * math.sin(self.view * self.DEG_TO_RAD)

        return round(x, self.PRECISION), round(y, self.PRECISION)


    def allObjCamPos(self):
        """
        Get the position of all blocks in camera view.
        """

        with PiCamera() as camera:
            camera = PiCamera()
            camera.resolution = (self.IMG_WIDTH, self.IMG_HEIGHT)
            camera.framerate = self.FRAMERATE

            stream = io.BytesIO()
            camera.start_preview()
            time.sleep(2)
            camera.capture(stream, format='jpeg')
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            camera.stop_preview()

            img = cv2.imdecode(data, 1)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            yellowMask = cv2.inRange(hsv, self.Y_HSV_MIN, self.Y_HSV_MAX)
            yellowObj = findImgObjProp(yellowMask)

            blueMask = cv2.inRange(hsv, self.B_HSV_MIN, self.B_HSV_MAX)
            blueObj = findImgObjProp(blueMask)

            redMask = cv2.inRange(hsv, self.R_HSV_MIN, self.R_HSV_MAX)
            redObj = findImgObjProp(redMask)

            allMask = cv2.bitwise_or(cv2.bitwise_or(yellowMask, blueMask), redMask)
            result = cv2.bitwise_and(img, img, mask=allMask)

            cv2.imshow("Image", img)
            cv2.imshow("HSV", hsv)
            cv2.imshow("Result", result)

            return (yellowObj, blueObj, redObj)



    def findImgObjProp(colMask):
        objA = 0
        objX = 0
        objY = 0

        contours, _ = cv2.findContours(colMask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, curW, curH = cv2.boundingRect(contour)
            curA = curW * curH
            curX = x + (curW // 2)
            curY = y + (curH // 2)
            if objA < curA:
                objA = curA
                objX = curX
                objY = curY

        if objA > 0:
            imgObjProp = [objA, objX, objY]
        else:
            imgObjProp = None
        return imgObjProp
