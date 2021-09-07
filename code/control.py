# -*- coding: utf-8 -*-

import error
import time
import math

class Control():
    """A class for controlling all the arm components at the same time."""'


    # Angle to increment each component by per loop in degrees.
    ANGLE_INC = 5

    # Absolute tolerance for difference between desired angle and actual angle of components.
    ABS_TOL = 1

    # Time between each angle increment.
    SLEEPY_TIME = 0.01


    def __init__(self, arm):
        """
        Initialise the arm control.

        :param arm: arm component
        """
        self.arm = arm
        self.shoulderAngle = None
        self.elbowAngle = None
        self.wristAngle = None
        self.grabberAngle = None


    def execute(self):
        """
        Execute angles on arm.

        :raise ValueError: if the arm is off
        """
        error.checkComponent(self.arm, 'Arm')

        while not((self.shoulderAngle is None) and (self.elbowAngle is None) and (self.wristAngle is None) and (self.grabberAngle is None)):

            if self.shoulderAngle is not None:
                angleDiff = self.shoulderAngle - self.arm.shoulder
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.shoulder = self.arm.shoulder + change

                if math.isclose(self.arm.shoulder, self.shoulderAngle, abs_tol=self.ABS_TOL):
                    self.shoulderAngle = None

            if self.elbowAngle is not None:
                angleDiff = self.elbowAngle - self.arm.elbow
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.elbow = self.arm.elbow + change

                if math.isclose(self.arm.elbow, self.elbowAngle, abs_tol=self.ABS_TOL):
                    self.elbowAngle = None

            if self.wristAngle is not None:
                angleDiff = self.wristAngle - self.arm.wrist
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.wrist = self.arm.wrist + change

                if math.isclose(self.arm.wrist, self.wristAngle, abs_tol=self.ABS_TOL):
                    self.wristAngle = None

            if self.grabberAngle is not None:
                angleDiff = self.grabberAngle - self.arm.grabber
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.grabber = self.arm.grabber + change

                if math.isclose(self.arm.grabber, self.grabberAngle, abs_tol=self.ABS_TOL):
                    self.grabberAngle = None

            time.sleep(self.SLEEPY_TIME)


    def shoulder(self, angle):
        """
        Set the shoulder angle to be executed.

        :param angle: shoulder angle in degrees
        :raise ValueError: if angle is not between 22 and 175
        """
        self.shoulderAngle = angle


    def elbow(self, angle):
        """
        Set the elbow angle to be executed.

        :param angle: elbow angle in degrees
        :raise ValueError: if the angle is not between 5 and 125
        """
        self.elbowAngle = angle


    def wrist(self, angle):
        """
        Set the wrist angle to be executed.

        :param angle: wrist angle in degrees
        :raise ValueError: if angle is not between 0 and 180
        """
        self.wristAngle = angle


    def grabber(self, angle):
        """
        Set the grabber angle to be executed.

        :param angle: grabber angle in degrees
        :raise ValueError: if angle is not between 0 and 90
        """
        self.grabberAngle = angle
