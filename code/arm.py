# -*- coding: utf-8 -*-


import error


class Arm:
    """A class for controlling the arm of the robot."""


    def __init__(self, shoulderPin, elbowPin, wristPin, grabberPin):
        error.checkPCA9685(shoulderPin)
        error.checkPCA9685(elbowPin)
        error.checkPCA9685(wristPin)
        error.checkPCA9685(grabberPin)

        self.shoulderPin = shoulderPin
        self.elbowPin = elbowPin
        self.wristPin = wristPin
        self.grabberPin = grabberPin
