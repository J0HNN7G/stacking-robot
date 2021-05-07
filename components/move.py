# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO


class Move:
    """A class for controlling the movement of the robot."""


    DC_TO_SPEED

    # The motors' minimum duty cycle.
    MIN_DC = 20

    # The motors' maximum duty cycle.
    MAX_DC = 100


    def __init__(self, dc, leftMotor, rightMotor):
        # type: (float, Motor, Motor) -> None
        """
        Initialise both motors with a given duty cycle.

        :param self: the radius of the motor's wheel in millimetres
        :param dc: GPIO number of pin controlling motor engine
        :param leftMotor: GPIO number of pin controlling backward motion
        :param rightMotor: GPIO number of pin controlling forward motion
        """
        self.dc(dc)
        self._leftMotor(leftMotor)
        self._rightMotor(rightMotor)


    def moveDuration(self, duration):
        if dist > 0:
            GPIO.output([self.leftMotor.backwardPin(), self.rightMotor.backwardPin()], GPIO.LOW)
            GPIO.output([self.leftMotor.forwardPin(), self.rightMotor.forwardPin()], GPIO.HIGH)
            self.leftMotor.pwm().start(self.dc())
            self.rightMotor.pwm().start(self.dc())
        elif dist < 0:
            GPIO.output([self.leftMotor.forwardPin(), self.rightMotor.forwardPin()], GPIO.LOW)
            GPIO.output([self.leftMotor.backwardPin(), self.rightMotor.backwardPin()], GPIO.HIGH)

        self.leftMotor.pwm().start(self.dc())
        self.rightMotor.pwm().start(self.dc())

        time.sleep(duration)

        self.leftMotor.stop()
        self.rightMotor.stop()


    @property
    def dc(self):
        return self._dc


    @dc.setter
    def dc(self, val):
        error.checkType(val, float, 'dc must be a float!')
        error.checkInRange(val, MIN_DC, MAX_DC)
        self._dc = val


    def leftMotor(self):
        return self._leftMotor


    def rightMotor(self):
        return self._rightMotor


    def _leftMotor(self, val):
        self._leftMotor = val


    def _rightMotor(self, val):
        self._rightMotor = val
