# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Arm(Component):
    """A class for controlling the arm of the robot."""

    SHOULDER_INIT_ANGLE = 85

    ELBOW_INIT_ANGLE = 100

    WRIST_INIT_ANGLE = 95

    GRABBER_INIT_ANGLE = 90

    GRABBER_ACT_RNG = 90


    def __init__(self, shoulderPin, elbowPin, wristPin, grabberPin):
        error.checkPCA9685(shoulderPin)
        error.checkPCA9685(elbowPin)
        error.checkPCA9685(wristPin)
        error.checkPCA9685(grabberPin)

        self.status = False
        self.kit = ServoKit(channels=16)
        self.shoulder = self.kit.servo[shoulderPin]
        self.elbow = self.kit.servo[elbowPin]
        self.wrist = self.kit.servo[wristPin]

        self.grabber = self.kit.servo[grabberPin]
        self.grabber.actuation_range = self.GRABBER_ACT_RNG

        self.setup()


    def setup(self):
        self.shoulder.angle = self.SHOULDER_INIT_ANGLE
        self.elbow.angle = self.ELBOW_INIT_ANGLE
        self.wrist.angle = self.WRIST_INIT_ANGLE
        self.grabber.angle = self.GRABBER_INIT_ANGLE
        self.status = True


    def cleanup(self):
        self.shoulder.angle = self.SHOULDER_INIT_ANGLE
        self.elbow.angle = self.ELBOW_INIT_ANGLE
        self.wrist.angle = self.WRIST_INIT_ANGLE
        self.grabber.angle = self.GRABBER_INIT_ANGLE
        self.status = False


    @shoulder.setter
    def shoulder(self,angle):
        error.checkComponent(self, 'Arm')
        self.shoulder.angle = angle


    @elbow.setter
    def elbow(self,angle):
        error.checkComponent(self, 'Arm')
        self.elbow.angle = angle


    @wrist.setter
    def wrist(self,angle):
        error.checkComponent(self, 'Arm')
        self.wrist.angle = angle


    @grabber.setter
    def grabber(self,angle):
        error.checkComponent(self, 'Arm')
        self.grabber.angle = angle
