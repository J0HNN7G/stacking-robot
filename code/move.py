# -*- coding: utf-8 -*-

import error
from motor import Motor
from direction import Direction

import time
import RPi.GPIO as GPIO


class Move:
    """A class for controlling the movement of the robot."""

    # DC_TO_SPEED = None

    # The motors' minimum duty cycle.
    MIN_DC = 20

    # The motors' maximum duty cycle.
    MAX_DC = 100


    @property
    def dc(self):
        # type: None -> float
        """
        Get the duty cycle.
        """
        return self.dc


    @property
    def leftMotor(self):
        # type: None -> Motor
        """
        Get the left motor.
        """
        return self.leftMotor


    @property
    def rightMotor(self):
        # type: None -> Motor
        """
        Get the right motor.
        """
        return self.rightMotor


    def __init__(self, dc, leftMotor, rightMotor):
        # type: (float, Motor, Motor) -> None
        """
        Initialise both motors with a given duty cycle.

        :param dc: GPIO number of pin controlling motor engine
        :param leftMotor: GPIO number of pin controlling backward motion
        :param rightMotor: GPIO number of pin controlling forward motion
        """
        self.dc(dc)
        self.leftMotor(leftMotor)
        self.rightMotor(rightMotor)


    def moveDuration(self, duration, direction):
        # type: (float, Direction) -> None
        """
        Move for a given duration in a given direction.

        :param duration: number of seconds of movement
        :param direction: direction of movement
        :raise ValueError: if left or right motor is off
        """
        error.checkComponent(self.leftMotor(), "Left motor")
        error.checkComponent(self.rightMotor(), "Right motor")

        if direction is Direction.FORWARD:
            GPIO.output([self.leftMotor().backwardPin(), self.rightMotor().backwardPin()], GPIO.LOW)
            GPIO.output([self.leftMotor().forwardPin(), self.rightMotor().forwardPin()], GPIO.HIGH)
        elif direction is Direction.BACKWARD:
            GPIO.output([self.leftMotor().forwardPin(), self.rightMotor().forwardPin()], GPIO.LOW)
            GPIO.output([self.leftMotor().backwardPin(), self.rightMotor().backwardPin()], GPIO.HIGH)

        self.leftMotor().pwm().start(self.dc())
        self.rightMotor().pwm().start(self.dc())

        time.sleep(duration)

        self.leftMotor().stop()
        self.rightMotor().stop()


    @dc.setter
    def dc(self, dc_val):
        # type: float -> None
        """
        Set the duty cycle.

        :param dc_val: duty cycle
        :raise TypeError: if dc_val is not a float
        :raise ValueError: if dc_val is out of range
        """
        error.checkType(dc_val, float, 'dc must be a float!')
        error.checkInRange(dc_val, self.MIN_DC, self.MAX_DC)
        self.dc = dc_val


    @leftMotor.setter
    def leftMotor(self, leftMotor):
        # type: Motor -> None
        """
        Set the left motor.

        :param leftMotor: left motor
        :raise TypeError: if leftMotor is not a motor
        """
        error.checkType(leftMotor, Motor, 'leftMotor must be a motor!')

        if not leftMotor.status():
            leftMotor.setup()
        self.leftMotor = leftMotor


    @rightMotor.setter
    def rightMotor(self, rightMotor):
        # type: Motor -> None
        """
        Set the right motor.

        :param rightMotor: right motor
        :raise TypeError: if rightMotor is not a motor
        """
        error.checkType(rightMotor, Motor, 'rightMotor must be a motor!')

        if not rightMotor.status():
            rightMotor.setup()
        self.rightMotor = rightMotor
