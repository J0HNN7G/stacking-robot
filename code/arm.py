# -*- coding: utf-8 -*-

import error
from component import Component

from adafruit_servokit import ServoKit

class Arm(Component):
    """A class for controlling the arm of the robot."""


    # The maximum angle in the input domain for any angle.
    MAX_ANGLE = 180

    # Minimum angle in the actual domain for the shoulder angle.
    SHOULDER_MIN_DOM = 5

    # Maximum angle in the actual domain for the shoulder angle.
    SHOULDER_MAX_DOM = 158

    # Initial angle of the shoulder (actually 90 degrees).
    SHOULDER_INIT_ANGLE = 80

    # Minimum angle in the actual domain for the elbow angle.
    ELBOW_MIN_DOM = 5

    # Maximum angle in the actual domain for the elbow angle.
    ELBOW_MAX_DOM = 140

    # Initial angle of the elbow (actually 90 degrees).
    ELBOW_INIT_ANGLE = 105

    # Initial angle of the wrist (actually 90 degrees).
    WRIST_INIT_ANGLE = 95

    # Initial angle of the grabber.
    GRABBER_INIT_ANGLE = 90

    # Angle input domain of the grabber.
    GRABBER_DOM = 90


    def __init__(self, shoulderPin, elbowPin, wristPin, grabberPin):
        """
        Initialise the arm parts.

        :param shoulderPin: PCA9685 numbering of the pin controlling the shoulder
        :param elbowPin: PCA9685 numbering of the pin controlling the elbow
        :param wristPin: PCA9685 numbering of the pin controlling the wrist
        :param grabberPin: PCA9685 numbering of the pin controlling the grabber
        :raise ValueError: if any pin is not given with a PCA9685 numbering
        """
        error.checkPCA9685(shoulderPin)
        error.checkPCA9685(elbowPin)
        error.checkPCA9685(wristPin)
        error.checkPCA9685(grabberPin)

        self.status = False
        kit = ServoKit(channels=16)
        self._shoulder = kit.servo[shoulderPin]
        self._elbow = kit.servo[elbowPin]
        self._wrist = kit.servo[wristPin]
        self._grabber = kit.servo[grabberPin]


    def setup(self):
        """
        Setup the arm in the initial angle for usage.
        """
        self._shoulder.angle = self.SHOULDER_INIT_ANGLE
        self._elbow.angle = self.ELBOW_INIT_ANGLE
        self._wrist.angle = self.WRIST_INIT_ANGLE
        self._grabber.angle = self.GRABBER_INIT_ANGLE
        self.status = True


    def cleanup(self):
        """
        Cleanup the arm when stopping usage.
        """
        self._shoulder.angle = None
        self._elbow.angle = None
        self._wrist.angle = None
        self._grabber.angle = None
        self.status = False


    @property
    def shoulder(self):
        """
        Get the shoulder angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :return: shoulder angle in degrees
        """
        return (1 - self._shoulder.angle / self.MAX_ANGLE) * (self.SHOULDER_MAX_DOM - self.SHOULDER_MIN_DOM) + self.SHOULDER_MIN_DOM


    @property
    def elbow(self):
        """
        Get the elbow angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :return: elbow angle in degrees
        """
        return self._elbow.angle * (self.ELBOW_MAX_DOM - self.ELBOW_MIN_DOM) / self.MAX_ANGLE + self.ELBOW_MIN_DOM

    @property
    def wrist(self):
        """
        Get the wrist angle.

        :return: wrist angle in degrees
        """
        return self._wrist.angle


    @property
    def grabber(self):
        """
        Get the grabber angle.

        :return: grabber angle in degrees
        """
        return self._grabber.angle


    @shoulder.setter
    def shoulder(self, angle):
        """
        Set the shoulder angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :param angle: shoulder angle in degrees
        :raise ValueError: if angle is not between 22 and 175, or the arm is off
        """
        error.checkComponent(self, 'Arm')
        error.checkInRange(angle, self.SHOULDER_MIN_DOM, self.SHOULDER_MAX_DOM)
        self._shoulder.angle = (1 - (angle - self.SHOULDER_MIN_DOM)) * self.MAX_ANGLE / (self.SHOULDER_MAX_DOM - self.SHOULDER_MIN_DOM)


    @elbow.setter
    def elbow(self, angle):
        """
        Set the actual elbow angle. As the actual angle and input angle differ,
        the value must be translated and stretched.

        :param angle: elbow angle in degrees
        :raise ValueError: if the angle is not between 5 and 125, or the arm is off
        """
        error.checkComponent(self, 'Arm')
        error.checkInRange(angle, self.ELBOW_MIN_DOM, self.ELBOW_MAX_DOM)
        self._elbow.angle = (angle - self.ELBOW_MIN_DOM) * self.MAX_ANGLE / (self.ELBOW_MAX_DOM - self.ELBOW_MIN_DOM)


    @wrist.setter
    def wrist(self, angle):
        """
        Set the wrist angle.

        :param angle: wrist angle in degrees
        :raise ValueError: if the arm is off
        """
        error.checkComponent(self, 'Arm')
        self._wrist.angle = angle


    @grabber.setter
    def grabber(self, angle):
        """
        Set the grabber angle.

        :param angle: grabber angle in degrees
        :raise ValueError: if angle is not between 0 and 90, or the arm is off
        """
        error.checkComponent(self, 'Arm')
        error.checkInRange(angle, 0, self.GRABBER_DOM)
        self._grabber.angle = angle
