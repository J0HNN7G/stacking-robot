# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Head(Component):
    """A class for controlling the head of the robot."""


    MIN_REAL_VIEW_ANGLE = 0

    MAX_REAL_VIEW_ANGLE = 60

    INIT_VIEW_ANGLE = 100

    VIEW_ACT_RNG = 100


    def __init__(self, viewPin):
        error.checkPCA9685(viewPin)

        self.status = False
        self.kit = ServoKit(channels=16)
        self._view = self.kit.servo[viewPin]
        self._view.actuation_range = self.INIT_VIEW_ANGLE

        self.setup()


    def setup(self):
        self._view.angle = self.INIT_VIEW_ANGLE
        self.status = True


    def cleanup(self):
        self._view.angle = self.INIT_VIEW_ANGLE
        self.status = False

    @property
    def view(self):
        return self.MAX_REAL_VIEW_ANGLE * (1 - (self._view.angle / self.VIEW_ACT_RNG))

    @view.setter
    def view(self,angle):
        error.checkInRange(angle, self.MIN_REAL_VIEW_ANGLE, self.MAX_REAL_VIEW_ANGLE)
        self._view.angle = self.VIEW_ACT_RNG * (1 - (angle / self.MAX_REAL_VIEW_ANGLE))
