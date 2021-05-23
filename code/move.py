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


    def __init__(self, dc, leftMotor, rightMotor):
        """
        Initialise both motors with a given duty cycle.

        :param dc: GPIO number of pin controlling motor engine
        :param leftMotor: GPIO number of pin controlling backward motion
        :param rightMotor: GPIO number of pin controlling forward motion
        :raise ValueError: if dc is out of range
        """
        error.checkInRange(dc, self.MIN_DC, self.MAX_DC)

        if not leftMotor.status():
            leftMotor.setup()

        if not rightMotor.status():
            rightMotor.setup()

        self.dc = dc
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor


    def moveDuration(self, duration, direction):
        """
        Move for a given duration in a given direction.

        :param duration: number of seconds of movement
        :param direction: direction of movement
        :raise ValueError: if left or right motor is off
        """
        error.checkComponent(self.leftMotor, "Left motor")
        error.checkComponent(self.rightMotor, "Right motor")

        if direction is Direction.FORWARD:
            GPIO.output([self.leftMotor.backwardPin, self.rightMotor.backwardPin], GPIO.LOW)
            GPIO.output([self.leftMotor.forwardPin, self.rightMotor.forwardPin], GPIO.HIGH)
        elif direction is Direction.BACKWARD:
            GPIO.output([self.leftMotor.forwardPin, self.rightMotor.forwardPin], GPIO.LOW)
            GPIO.output([self.leftMotor.backwardPin, self.rightMotor.backwardPin], GPIO.HIGH)

        self.leftMotor.pwm.start(self.dc)
        self.rightMotor.pwm.start(self.dc)

        time.sleep(duration)

        self.leftMotor.stop()
        self.rightMotor.stop()
