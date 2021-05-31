# -*- coding: utf-8 -*-

import error
from component import Component
from motor import Motor
from direction import Direction

import time
import RPi.GPIO as GPIO


class Body(Component):
    """A class for controlling the movement of the robot body."""


    # The motors' minimum duty cycle.
    MIN_MOTOR_DC = 20

    # The motors' maximum duty cycle.
    MAX_MOTOR_DC = 100

    # Standard radius  of wheels (0-1). No specific unit.
    # Used for calculating turning speed.
    STD_RADIUS = 0.6


    def __init__(self, dc, leftMotor, rightMotor):
        """
        Initialise the body for movmement

        :param dc: Duty cycle used by motors
        :param leftMotor: left motor of the robot
        :param rightMotor: right motor of the robot
        :raise ValueError: if dc is out of range
        """
        error.checkInRange(dc, self.MIN_MOTOR_DC, self.MAX_MOTOR_DC)

        self.dc = dc
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor


    def setup(self):
        """
        Setup the motors for movement.
        """
        if not self.leftMotor.status:
            self.leftMotor.setup()

        if not self.rightMotor.status:
            self.rightMotor.setup()


    def cleanup(self):
        """
        Cleanup the motors for ending of movement.
        """
        self.leftMotor.cleanup()
        self.rightMotor.cleanup()


    def move(self, duration, direction):
        """
        Move for a given duration in a given direction.

        :param duration: number of seconds of movement
        :param direction: direction of movement
        :raise ValueError: if left or right motor is off, or duration is not
                           positive
        """
        error.checkComponent(self.leftMotor, "Left motor")
        error.checkComponent(self.rightMotor, "Right motor")
        error.checkType(direction, Direction, 'direction', 'Direction')
        error.checkPositive(duration)

        left_dc = self.dc
        right_dc = self.dc

        if direction is Direction.FORWARD:
            GPIO.output([self.leftMotor.backwardPin, self.rightMotor.backwardPin], GPIO.LOW)
            GPIO.output([self.leftMotor.forwardPin, self.rightMotor.forwardPin], GPIO.HIGH)

        elif direction is Direction.BACKWARD:
            GPIO.output([self.leftMotor.forwardPin, self.rightMotor.forwardPin], GPIO.LOW)
            GPIO.output([self.leftMotor.backwardPin, self.rightMotor.backwardPin], GPIO.HIGH)

        elif direction is Direction.LEFT:
            GPIO.output([self.leftMotor.forwardPin, self.rightMotor.backwardPin], GPIO.LOW)
            GPIO.output([self.leftMotor.backwardPin, self.rightMotor.forwardPin], GPIO.HIGH)
            left_dc *= self.STD_RADIUS

        elif direction is Direction.RIGHT:
            GPIO.output([self.leftMotor.backwardPin, self.rightMotor.forwardPin], GPIO.LOW)
            GPIO.output([self.leftMotor.forwardPin, self.rightMotor.backwardPin], GPIO.HIGH)
            right_dc *= self.STD_RADIUS

        try:
            self.leftMotor.pwm.start(left_dc)
            self.rightMotor.pwm.start(right_dc)

            time.sleep(duration)

            self.leftMotor.stop()
            self.rightMotor.stop()
        except Exception as e:
            print(e)
            self.cleanup()
