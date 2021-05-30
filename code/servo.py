# -*- coding: utf-8 -*-


import error
from component import Component

 # A PCA9685 circuit board controls all the servos
import Adafruit_PCA9685
import time


class Servo(Component):
    """A class for controlling the servos of the head and arm of the robot."""


    # Standard Frequency of the servos.
    STD_SERVO_FREQ = 50

    # Minimum duty cycle for the servos.
    MIN_SERVO_DC = 100

    # Maximum duty cycle for the servos.
    MAX_SERVO_DC = 560

    # Initial duty cycle for the servos.
    INIT_SERVO_DC = 330

    # Minimum angle of the servos (when min duty cycle is used).
    MIN_ANGLE = 0

    # Maximum angle of the servos (when max duty cycle is used).
    MAX_ANGLE = 180

    # Initial angle of the servos (when middle of duty cycle range is used).
    INIT_ANGLE = 90


    def __init__(self, pin, pwm):

        self.pin = pin

        self.pwm = pwm
        self.pwm.set_pwm_freq(self.STD_SERVO_FREQ)
        self.pwm.set_pwm(self.pin, 0, self.INIT_SERVO_DC)

        self.angle = self.INIT_ANGLE

    def setup(self):
        pass

    def cleanup(self):
        pass

    def setAngle(self, angle):
        error.checkInRange(angle, MIN_ANGLE, MAX_ANGLE)

        new_dc = self.MIN_SERVO_DC + (angle / self.MAX_ANGLE) * (self.MAX_SERVO_DC - self.MIN_SERVO_DC)
        self.pwm.set_pwm(self.pin, 0, new_dc)
        self.angle = angle

while 1：# Make the servo connected to the No. 3 servo port on the Robot HAT drive board reciprocate
    pwm.set_pwm(3, 0, 300)
    time.sleep(1)

    pwm.set_pwm(3, 0, 400)
    time.sleep(1)
