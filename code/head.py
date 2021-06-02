# -*- coding: utf-8 -*-

import error
from component import Component

from adafruit_servokit import ServoKit

class Head(Component):
    """A class for controlling the head of the robot."""


    # The domain of the function which controls the view angle.
    VIEW_DOM = 100

    # The actual range of the view angle.
    VIEW_RNG = 60


    def __init__(self, viewPin):
        """
        Initialise the head view movement.

        :param viewPin: PCA9685 numbering of the pin controlling the head
        :raise ValueError: if viewPin is not a PCA9685 numbering
        """
        error.checkPCA9685(viewPin)

        self.status = False
        self.kit = ServoKit(channels=16)
        self._view = self.kit.servo[viewPin]


    def setup(self):
        """
        Setup the view to be at the standard angle.
        """
        self._view.angle = self.VIEW_DOM
        self.status = True


    def cleanup(self):
        """
        Cleanup the view by turning off the servo.
        """
        self._view.angle = None
        self.status = False


    @property
    def view(self):
        """
        Get the actual view angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :return: view angle in degrees
        """
        return self.VIEW_RNG * (1 - self._view.angle / self.VIEW_DOM)


    @view.setter
    def view(self, angle):
        """
        Set the view angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :param angle: view angle in degrees
        :raise ValueError: if the angle is not between 0 to 60, or
                           the head is off
        """
        error.checkComponent(self, 'Head')
        error.checkInRange(angle, 0, self.VIEW_RNG)
        self._view.angle = self.VIEW_DOM * (1 - angle / self.VIEW_RNG)


# TODO def xyDist(self):
