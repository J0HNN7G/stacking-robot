# -*- coding: utf-8 -*-

import error
from component import Component

import math
from adafruit_servokit import ServoKit

class Head(Component):
    """A class for controlling the head of the robot."""


    # The domain of the function which controls the view angle.
    VIEW_DOM = 100

    # The actual range of the view angle.
    VIEW_RNG = 60

    # The number of times we measure the distance to an object.
    NUM_TRIES = 10

    # Distance from axis of rotation for the head and the ultrasonic sensor
    AX_TO_SEN = math.sqrt(2 * (0.025 ** 2))

    # difference between x values of the shoulder axis to axis of rotation for the head
    X_ORIG_TO_AX = -0.035

    # difference between y values of the shoulder axis to axis of rotation for the head
    Y_ORIG_TO_AX = -0.05

    # Conversion factor from radians to degrees.
    DEG_TO_RAD = math.pi / 180

    # Precision of object coordinates calculated with ultrasonic sensor
    PRECISION = 3


    def __init__(self, viewPin, ultra):
        """
        Initialise the head view movement.

        :param viewPin: PCA9685 numbering of the pin controlling the head
        :raise ValueError: if viewPin is not a PCA9685 numbering
        """
        error.checkPCA9685(viewPin)

        self.status = False
        kit = ServoKit(channels=16)
        self._view = kit.servo[viewPin]
        self.ultra = ultra


    def setup(self):
        """
        Setup the view to be at the standard angle.
        """
        self._view.angle = self.VIEW_DOM

        if not self.ultra.status:
            self.ultra.setup()

        self.status = True


    def cleanup(self):
        """
        Cleanup the view by turning off the servo.
        """
        self._view.angle = None
        self.ultra.cleanup()
        self.status = False


    @property
    def view(self):
        """
        Get the actual view angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :return: view angle in degrees
        """
        return round(self.VIEW_RNG * (1 - self._view.angle / self.VIEW_DOM), 0)


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


    def objPos(self):
        """
        Calculate the cartesian coordinates of an object with the ultrasonic
        sensor relative to the axis of the shoulder.

        :return: the cartesian position of the object in metres relative to the
                 axis of the shoulder
        :raise ValueError: if the ultrasonic sensor is off
        """
        error.checkComponent(self.ultra, 'Ultrasonic sensor')

        senToObj = self.ultra.meanAdjDist(self.NUM_TRIES)

        print(senToObj)
        x = self.X_ORIG_TO_AX + self.AX_TO_SEN * math.cos(self.view * self.DEG_TO_RAD + (3/4)*math.pi) \
            - senToObj * math.cos(self.view * self.DEG_TO_RAD)
        y = self.Y_ORIG_TO_AX + self.AX_TO_SEN * math.sin(self.view * self.DEG_TO_RAD - (1/4)*math.pi) \
            + senToObj * math.sin(self.view * self.DEG_TO_RAD)

        return round(x, self.PRECISION), round(y, self.PRECISION)
