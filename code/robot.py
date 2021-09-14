# -*- coding: utf-8 -*-

import error
from component import Component
import inverse_kinematics as ik
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
    MIN_AREA = 100

    # Maximum area of object in image.
    MAX_AREA = 1.5 * (10 ** 4)

    # Horizontal center of camera images in pixels.
    CENTER_IMG_X = Head.IMG_WIDTH // 2

    # Vertical center of camera images in pixels.
    CENTER_IMG_Y = Head.IMG_HEIGHT // 2

    # The divisor of image width or height in pixels to determine
    # if object is within center view for faraway find.
    FAR_THRESH_DIV = 5

    # Duration of movement per camera frame in faraway entity search.
    FAR_MOVE_TIME = 0.2

    # Angle change per camera frame if object is outside of vertical
    # center view for faraway search.
    FAR_VIEW_DIFF = 5

    # Readjustment period for camera after search movement for faraway search.
    FAR_REF_TIME = 0.25

    # The divisor of image width or height in pixels to determine
    # if object is within center view for faraway find.
    CLOSE_THRESH_DIV = 7

    # Duration of movement per camera frame in faraway entity search.
    CLOSE_MOVE_TIME = 0.05

    # Angle change per camera frame if object is outside of vertical
    # center view for faraway search.
    CLOSE_VIEW_DIFF = 3

    # Readjustment period for camera after search movement for faraway search.
    CLOSE_REF_TIME = 0.5


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
        angles = ik.calcAngles(objPos)

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
                self.arm.planShoulder(Arm.SHOULDER_MIN_DOM)
                self.arm.planElbow(90)
                self.arm.executePlan()
                
                self.arm.planElbow(Arm.ELBOW_MAX_DOM)
                self.arm.executePlan()

                result = True
        return result


    def farFind(self, entity, timeLim):
        error.checkType(entity, Entity, 'entity', 'Entity')
        if entity == Entity.FLOOR:
            return True

        self.head.view = 0

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
                    print(objProp)
                    if (objProp['area'] >= self.MIN_AREA) and (objProp['area'] < self.MAX_AREA):
                        if not inView:
                            print('found it')
                        inView = True

                        # Too high
                        if (objProp['y'] > self.CENTER_IMG_Y + (Head.IMG_HEIGHT // self.FAR_THRESH_DIV)) and (self.head.view != 0):
                            self.head.view = self.head.view - min(self.FAR_VIEW_DIFF, self.head.view)
                            print('down')

                        # Too low
                        elif objProp['y'] < self.CENTER_IMG_Y - (Head.IMG_HEIGHT // self.FAR_THRESH_DIV):
                            diff = min(self.FAR_VIEW_DIFF, Head.VIEW_RNG - self.head.view)
                            self.head.view = self.head.view + diff
                            print('up')

                            # If we get closer, the object will get out of view
                            if math.isclose(self.head.view, Head.VIEW_RNG, abs_tol=1):
                                return True


                        # Too left
                        if objProp['x'] > self.CENTER_IMG_X + (Head.IMG_WIDTH // self.FAR_THRESH_DIV):
                            self.body.move(self.FAR_MOVE_TIME, Direction.RIGHT)
                            print('left')

                        # Too right
                        elif objProp['x'] < self.CENTER_IMG_X - (Head.IMG_WIDTH // self.FAR_THRESH_DIV):
                            self.body.move(self.FAR_MOVE_TIME, Direction.LEFT)
                            print('right')

                        # Perfect horizontal view
                        else:
                            self.body.move(self.FAR_MOVE_TIME, Direction.FORWARD)
                            print('forward')


                    elif objProp['area'] < self.MIN_AREA:
                        print('searching')
                        if inView:
                            # start searching again
                            inView = False
                            searchStart = time.time()
                            print('lost it')
                        elif (time.time() - searchStart > timeLim):
                            return False
                        self.body.move(self.FAR_MOVE_TIME, Direction.LEFT)

                    else:
                        return True

                else:
                    print('searching')
                    if (not inView) and (time.time() - searchStart > timeLim):
                        return False
                    elif inView:
                        # start searching again
                        inView = False
                        searchStart = time.time()
                    self.body.move(self.FAR_MOVE_TIME, Direction.LEFT)

                # readjust the camera
                time.sleep(self.FAR_REF_TIME)
                rawCapture.truncate(0)


    def closeFind(self, entity):
        error.checkType(entity, Entity, 'entity', 'Entity')
        if entity == Entity.FLOOR:
            return True

        with PiCamera() as camera:
            camera.resolution = (Head.IMG_WIDTH, Head.IMG_HEIGHT)
            camera.framerate = Head.FRAMERATE
            rawCapture = PiRGBArray(camera, size=(Head.IMG_WIDTH, Head.IMG_HEIGHT))

            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                colMask = head.colourMask(hsv, entity)
                objProp = head.findObjProp(colMask)

                if objProp:
                    print(objProp)
                    if objProp['area'] < self.MIN_AREA:
                        print('way too small')
                        return False


                        # Too high
                    if (objProp['y'] > self.CENTER_IMG_Y + (Head.IMG_HEIGHT // self.CLOSE_THRESH_DIV)) and (self.head.view != 0):
                        self.head.view = self.head.view - min(self.CLOSE_VIEW_DIFF, self.head.view)
                        print('down')
                        # Too low
                    elif objProp['y'] < self.CENTER_IMG_Y - (Head.IMG_HEIGHT // self.CLOSE_THRESH_DIV):
                        diff = min(self.CLOSE_VIEW_DIFF, Head.VIEW_RNG - self.head.view)
                        self.head.view = self.head.view + diff
                        print('up')
                        # If we get closer, the object will get out of view
                        if math.isclose(self.head.view, Head.VIEW_RNG, abs_tol=1):
                            return True

                    # Too left
                    if objProp['x'] > self.CENTER_IMG_X + (Head.IMG_WIDTH // self.CLOSE_THRESH_DIV):
                        self.body.move(self.CLOSE_MOVE_TIME, Direction.RIGHT)
                        print('left')
                    # Too right
                    elif objProp['x'] < self.CENTER_IMG_X - (Head.IMG_WIDTH // self.CLOSE_THRESH_DIV):
                        self.body.move(self.CLOSE_MOVE_TIME, Direction.LEFT)
                        print('right')
                    else:
                        objPos = self.head.objPos()
                        # distance between shoulder axis and target
                        tDist = round( math.sqrt(objPos[0]**2 + objPos[1]**2), ik.PRECISION)

                        if tDist > ik.S_LEN + ik.E_LEN:
                            self.body.move(self.CLOSE_MOVE_TIME, Direction.FORWARD)
                            print('too far')
                        elif tDist < ik.E_LEN - ik.S_LEN:
                            self.body.move(self.CLOSE_MOVE_TIME, Direction.BACKWARD)
                            print('too close')
                        else:
                            shoulderAngle, elbowAngle = ik.calcAngles(objPos)
                            if (Arm.SHOULDER_MIN_DOM <= shoulderAngle <= Arm.SHOULDER_MAX_DOM) and (Arm.ELBOW_MIN_DOM <= elbowAngle <= Arm.ELBOW_MAX_DOM):
                                return True
                            else:
                                self.body.move(self.CLOSE_MOVE_TIME, Direction.FORWARD)
                                print('dunno, move closer')

                else:
                    print('lost')
                    return False

                # readjust the camera
                time.sleep(self.CLOSE_REF_TIME)
                rawCapture.truncate(0)
