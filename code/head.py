# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Head(Component):
    """A class for controlling the head of the robot."""

    INIT_ANGLE = 90

    def __init__(self, headPin):
        error.checkPCA9685(headPin)

        self.status = False
        self.kit = ServoKit(channels=16)
        self.head = self.kit.servo[headPin]

        self.setup()


    def setup(self):
        self.head.angle = self.INIT_ANGLE
        self.status = True


    def cleanup(self):
        self.head.angle = self.INIT_ANGLE
        self.status = False
