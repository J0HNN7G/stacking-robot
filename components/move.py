# -*- coding: utf-8 -*-

from motor import Motor
import RPi.GPIO as GPIO
import time

class Move:
    """A class for controlling the movement of the robot."""


    SPEED_TO_FREQ = 1


    @property
    def speed(self):
        return self._speed


    @property
    def leftMotor(self):
        return self._leftMotor


    @property
    def rightMotor(self):
        return self._rightMotor


    def __init__(self, speed, leftMotor, rightMotor):
        self.speed(speed)
        self.leftMotor(leftMotor)
        self.rightMotor(rightMotor)


    def move(self, dist):
        duration = abs(dist)/self.speed()
        if dist > 0:
            GPIO.output(self.leftMotor.backwardPin(), GPIO.LOW)
            GPIO.output(self.leftMotor.forwardPin(), GPIO.HIGH)
            self.leftMotor.pwm().start(0)
            self.leftMotor.pwm().ChangeDutyCycle(self.speed())

            GPIO.output(self.rightMotor.backwardPin(), GPIO.LOW)
            GPIO.output(self.rightMotor.forwardPin(), GPIO.HIGH)
            self.rightMotor.pwm().start(0)
            self.rightMotor.pwm().ChangeDutyCycle(self.speed())
        elif dist < 0:
            GPIO.output(self.leftMotor.forwardPin(), GPIO.LOW)
            GPIO.output(self.leftMotor.backwardPin(), GPIO.HIGH)
            self.leftMotor.pwm().start(100)
            self.leftMotor.pwm().ChangeDutyCycle(self.speed())

            GPIO.output(self.rightMotor.forwardPin(), GPIO.LOW)
            GPIO.output(self.rightMotor.backwardPin(), GPIO.HIGH)
            self.rightMotor.pwm().start(100)
            self.rightMotor.pwm().ChangeDutyCycle(self.speed())
        else:
            pass

        time.sleep(duration)
        self.leftMotor.stop()
        self.rightMotor.stop()


    @speed.setter
    def speed(self, val):
        self._speed = val


    @leftMotor.setter
    def leftMotor(self, val):
        self._leftMotor = val


    @rightMotor.setter
    def rightMotor(self, val):
        self._rightMotor = val
