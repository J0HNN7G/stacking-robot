# -*- coding: utf-8 -*-


import error
from component import Component

from adafruit_servokit import ServoKit


class Head(Component):
    """A class for controlling the head of the robot."""

    VIEW_ACTUAL_RNG = 60

    VIEW_ACT_RNG = 32


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
        return self.VIEW_ACTUAL_RNG * (1 - self._view.angle / self.VIEW_ACT_RNG)

    @view.setter
    def view(self,angle):
        error.checkInRange(angle, 0, self.VIEW_ACTUAL_RNG)
        self._view.angle = self.VIEW_ACT_RNG * (1 - angle / VIEW_ACTUAL_RNG)
