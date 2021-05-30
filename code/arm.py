# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Arm(Component):
    """A class for controlling the arm of the robot."""

    INIT_ANGLE = 90

    def __init__(self, shoulderPin, elbowPin, wristPin, grabberPin):
        error.checkPCA9685(shoulderPin)
        error.checkPCA9685(elbowPin)
        error.checkPCA9685(wristPin)
        error.checkPCA9685(grabberPin)

        set.status = False
        self.kit = ServoKit(channels=16)
        self.shoulder = self.kit.servo[shoulderPin]
        self.elbow = self.kit.servo[elbowPin]
        self.wrist = self.kit.servo[wristPin]
        self.grabber = self.kit.servo[grabberPin]


    def setup(self):
        self.shoulder.angle = self.INIT_ANGLE
        self.elbow.angle = self.INIT_ANGLE
        self.wrist.angle = self.INIT_ANGLE
        self.grabber.angle = self.INIT_ANGLE
        self.status = True


    def cleanup(self):
        self.shoulder.angle = self.INIT_ANGLE
        self.elbow.angle = self.INIT_ANGLE
        self.wrist.angle = self.INIT_ANGLE
        self.grabber.angle = self.INIT_ANGLE
        self.status = False
