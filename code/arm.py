# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Arm(Component):
    """A class for controlling the arm of the robot."""
    # TODO explain the angles here

    SHOULDER_INIT_ANGLE = 80

    ELBOW_INIT_ANGLE = 105

    WRIST_INIT_ANGLE = 95

    GRABBER_INIT_ANGLE = 90

    GRABBER_DOM = 90


    def __init__(self, shoulderPin, elbowPin, wristPin, grabberPin):
        error.checkPCA9685(shoulderPin)
        error.checkPCA9685(elbowPin)
        error.checkPCA9685(wristPin)
        error.checkPCA9685(grabberPin)

        self.status = False
        self.kit = ServoKit(channels=16)
        self._shoulder = self.kit.servo[shoulderPin]
        self._elbow = self.kit.servo[elbowPin]
        self._wrist = self.kit.servo[wristPin]
        self._grabber = self.kit.servo[grabberPin]


    def setup(self):
        self._shoulder.angle = self.SHOULDER_INIT_ANGLE
        self._elbow.angle = self.ELBOW_INIT_ANGLE
        self._wrist.angle = self.WRIST_INIT_ANGLE
        self._grabber.angle = self.GRABBER_INIT_ANGLE
        self.status = True


    def cleanup(self):
        self._shoulder.angle = None
        self._elbow.angle = None
        self._wrist.angle = None
        self._grabber.angle = None
        self.status = False

    @property
    def shoulder(self):
        return self._shoulder.angle


    @property
    def elbow(self):
        return self._elbow.angle


    @property
    def wrist(self):
        return self._wrist.angle


    @property
    def grabber(self):
        return self._grabber.angle


    @shoulder.setter
    def shoulder(self, angle):
        # actual range is 175
        error.checkInRange(angle, 22, 175)
        self._shoulder.angle = (angle - 22) * 180/153


    @elbow.setter
    def elbow(self, angle):
        self._elbow.angle = angle


    @wrist.setter
    def wrist(self, angle):
        self._wrist.angle = angle


    @grabber.setter
    def grabber(self, angle):
        error.checkInRange(angle, 0, self.GRABBER_DOM)
        self._grabber.angle = angle
