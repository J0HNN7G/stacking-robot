# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Head(Component):
    """A class for controlling the head of the robot."""


    VIEW_ACT_RNG = 60


    def __init__(self, viewPin):
        error.checkPCA9685(viewPin)

        self.status = False
        self.kit = ServoKit(channels=16)
        self._view = self.kit.servo[viewPin]
        self._view.actuation_range = self.VIEW_ACT_RNG

        self.setup()


    def setup(self):
        self._view.angle = self.VIEW_ACT_RNG
        self.status = True


    def cleanup(self):
        self._view.angle = self.VIEW_ACT_RNG
        self.status = False

    @property
    def view(self):
        return self._view.angle

    @view.setter
    def view(self,angle):
        error.checkInRange(angle, 0, self.VIEW_ACT_RNG)
        self._view.angle = angle
