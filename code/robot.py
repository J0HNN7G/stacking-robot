# -*- coding: utf-8 -*-

import error
from component import Component
from inverse_kinematics import calcAngles
from arm import Arm
from head import Head
import head
from entity import Entity
from direction import Direction

import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

class Robot(Component):
    """A class for controlling the robot."""


    # Time for grabber to open
    OPEN_TIME = 0.5

    # Time for grabber to grab
    CLOSE_TIME = 1

    # Minimum area of object in image.
    MIN_AREA = 250

    # Maximum area of object in image.
    MAX_AREA = 10 ** 5

    # Horizontal center of camera images in pixels.
    CENTER_IMG_X = Head.IMG_WIDTH // 2

    # Vertical center of camera images in pixels.
    CENTER_IMG_Y = Head.IMG_HEIGHT // 2

    # The divisor of image width or height in pixels to determine if object is within center view
    THRESH_DIV = 3

    # Duration of movement per camera frame in entity search.
    MOVE_TIME = 0.2

    # Angle change per camera frame if object is outside of vertical center view
    VIEW_DIFF = 5


    def __init__(self, head, body, arm):
        """
        Initialise the robot components

        :param head: robot head component
        :param body: robot body component
        :param arm: robot arm component
        """
        self.status = False
        self.head = head
        self.body = body
        self.arm = arm


    def setup(self):
        """
        Setup all the robot components
        """
        if not self.head.status:
            self.head.setup()
        if not self.arm.status:
            self.arm.setup()
        self.body.setup()
        self.status = True


    def cleanup(self):
        """
        Cleanup all the robots components.
        """
        self.head.cleanup()
        self.body.cleanup()
        self.arm.cleanup()
        self.status = False


    def pickup(self):
        """
        Pick up an object close to the front of the robot.

        :return: True if the pick up was possible, otherwise False
        """
        error.checkComponent(self, 'Robot')

        result = False
        objPos = self.head.objPos()
        angles = calcAngles(objPos)

        if angles is not None:
            shoulderAngle, elbowAngle = angles

            if (Arm.SHOULDER_MIN_DOM <= shoulderAngle <= Arm.SHOULDER_MAX_DOM) and (Arm.ELBOW_MIN_DOM <= elbowAngle <= Arm.ELBOW_MAX_DOM):
                # open
                self.arm.planGrabber(Arm.MIN_ANGLE)
                self.arm.executePlan()
                time.sleep(self.OPEN_TIME)

                # position
                self.arm.planShoulder(shoulderAngle)
                self.arm.planElbow(elbowAngle)
                self.arm.executePlan()
                time.sleep(self.CLOSE_TIME)

                # close
                self.arm.planGrabber(Arm.GRABBER_DOM)
                self.arm.executePlan()
                time.sleep(self.CLOSE_TIME)

                # position
                self.arm.planShoulder(Arm.SHOULDER_MAX_DOM)
                self.arm.planElbow(ARM.ELBOW_MAX_DOM)
                self.arm.executePlan()

                result = True
        return result


    def find(self, entity, timeLim):
        error.checkType(entity, Entity, 'entity', 'Entity')
        if entity == Entity.FLOOR:
            return True

        with PiCamera() as camera:
            camera.resolution = (Head.IMG_WIDTH, Head.IMG_HEIGHT)
            camera.framerate = Head.FRAMERATE
            rawCapture = PiRGBArray(camera, size=(Head.IMG_WIDTH, Head.IMG_HEIGHT))

            inView = False
            searchStart = time.time()

            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                colMask = head.colourMask(hsv, entity)
                objProp = head.findObjProp(colMask)

                if objProp:
                    if (objProp['area'] >= self.MIN_AREA) and (objProp['area'] < self.MAX_AREA):
                        inView = True

                        # Too high
                        if (objProp['y'] > self.CENTER_IMG_Y + (Head.IMG_HEIGHT // self.THRESH_DIV)) and (self.head.view != 0):
                            self.head.view = self.head.view - min(self.VIEW_DIFF, self.head.view)

                        # Too low
                        elif objProp['y'] < self.CENTER_IMG_Y - (Head.IMG_HEIGHT // self.THRESH_DIV):
                            diff = min(self.VIEW_DIFF, Head.VIEW_RNG - self.head.view)
                            self.head.view = self.head.view + diff

                            # If we get closer, the object will get out of view
                            if math.isclose(self.head.view, Head.VIEW_RNG, abs_tol=1):
                                return True


                        # Too left
                        if objProp['x'] > self.CENTER_IMG_X + (Head.IMG_WIDTH // self.THRESH_DIV):
                            self.body.move(self.MOVE_TIME, Direction.RIGHT)

                        # Too right
                        elif objProp['x'] < self.CENTER_IMG_X - (Head.IMG_WIDTH // self.THRESH_DIV):
                            self.body.move(self.MOVE_TIME, Direction.LEFT)

                        # Perfect horizontal view
                        else:
                            self.body.move(self.MOVE_TIME, Direction.FORWARD)


                    elif objProp['area'] < self.MIN_AREA:
                        if inView:
                            # start searching again
                            inView = False
                            searchStart = time.time()
                        elif (time.time() - searchStart > timeLim):
                            return False

                    else:
                        return True

                else:
                    if (not inView) and (time.time() - searchStart > timeLim):
                        return False
                    elif inView:
                        # start searching again
                        inView = False
                        searchStart = time.time()
                    self.body.move(self.MOVE_TIME, Direction.LEFT)
                    
                rawCapture.truncate(0)
