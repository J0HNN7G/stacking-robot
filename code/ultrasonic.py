# -*- coding: utf-8 -*-

import error
from component import Component

import time
import RPi.GPIO as GPIO

class Ultrasonic(Component):
    """A class for controlling the ultrasonic sensor of the robot."""


    # Speed of sound in metres per second assuming standard conditions.
    SOUND_SPEED = 343

    # Duration that the ultrasonic sensor emits sound waves in seconds.
    EMIT_TIME = 0.000015

    # Refactory period, so that sensor does not pick up old emissions
    # when used repeatedly.
    REF_TIME = 0.000005

    # Error correction for ultrasonic sensor in metres.
    ERR_CORR = 0.016


    def __init__(self, trigPin, echoPin):
        error.checkGPIO(trigPin)
        error.checkGPIO(echoPin)

        self.status = False
        self.trigPin = trigPin
        self.echoPin = echoPin


    def setup(self):
        """
        Setup the ultrasonic sensor for use.
        """
        GPIO.setwarnings(False)
        # Set to GPIO numbering
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echoPin, GPIO.IN)
        self.status = True


    def cleanup(self):
        """
        Cleanup the ultrasonic sensor.
        """
        GPIO.cleanup([self.trigPin, self.echoPin])
        self.status = False


    def distance(self):
        """
        Get the distance from an object to the front of the robot.

        :return: the recorded distance of an object in front of the ultrasonic
                 sensor in metres
        :raise ValueError: if the ultrasonic sensor is off
        """
        error.checkComponent(self, 'Ultrasonic sensor')

        GPIO.output(self.trigPin, GPIO.LOW)
        time.sleep(self.REF_TIME)
        GPIO.output(self.trigPin, GPIO.HIGH)
        time.sleep(self.EMIT_TIME)
        GPIO.output(self.trigPin, GPIO.LOW)

        while not GPIO.input(self.echoPin):
            pass
        startTime = time.time()
        while GPIO.input(self.echoPin):
            pass
        endTime = time.time()

        return (endTime - startTime) * self.SOUND_SPEED / 2


    def meanAdjDist(self, numOfChecks):
        """
        Get the mean error-adjusted distance of an object to the front
        of the robot.

        :param numOfChecks: number of times that the distance is recorded for the
                            mean
        :return: mean error-adjusted distance of an object in metres
        :raise ValueError: if the ultrasonic sensor is off
        """
        data = []
        for i in range(numOfChecks):
            data.append(self.distance())
        return sum(data) / numOfChecks + self.ERR_CORR
