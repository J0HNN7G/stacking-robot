# -*- coding: utf-8 -*-

import error
from component import Component
from inverse_kinematics import calcAngles
from arm import Arm

import time

class Robot(Component):
    """A class for controlling the robot."""


    # Time for grabber to open
    OPEN_TIME = 0.5

    # Time for grabber to grab
    CLOSE_TIME = 1


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
                self.arm.control.grabber(0)
                self.arm.control.execute()

                self.arm.control.shoulder(shoulderAngle)
                self.arm.control.shoulder(elbowAngle)
                self.arm.control.execute()

                self.arm.control.grabber(90)
                self.arm.control.execute()

                self.arm.control.shoulder(90)
                self.arm.control.elbow(90)
                self.arm.control.execute()

                result = True
        return result
