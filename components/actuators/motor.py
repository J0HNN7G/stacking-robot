# -*- coding: utf-8 -*-

import error
import component
import RPi.GPIO as GPIO

class Motor(component.Component):

    STD_FREQ = 1000

    @property
    def pwm(self):
        return self._pwm

    @property
    def radius(self):
        return self._radius

    @property
    def enginePin(self):
        return self._enginePin

    @property
    def backwardPin(self):
        return self._backwardPin

    @property
    def forwardPin(self):
        return self._forwardPin

    def __init__(self, radius, enginePin, backwardPin, forwardPin):
        status(False)
        radius(radius)
        enginePin(enginePin)
        backwardPin(backwardPin)
        forwardPin(forwardPin)

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(enginePin(), GPIO.OUT)
    	GPIO.setup(backwardPin(), GPIO.OUT)
    	GPIO.setup(forwardPin(), GPIO.OUT)

        stop()
        try:
            pwm(GPIO.PWM(enginePin(), STD_FREQ))
        except Exception as e:
            print(e)
            cleanup()

    def cleanup(self):
        stop()
        GPIO.cleanup([enginePin(), backwardPin(), forwardPin()])

    def stop(self):
        GPIO.output(enginePin(), GPIO.LOW)
        GPIO.output(backwardPin(), GPIO.LOW)
        GPIO.output(forwardPin(), GPIO.LOW)

    @pwm.setter
    def pwm(self, val):
        error.checkType(val, GPIO.PWM)
        self._pwm = val

    @radius.setter
    def radius(self, val):
        error.checkType(val, float, 'radius must be a float!')
        self._radius = val

    @enginePin.setter
    def enginePin(self, val):
        error.checkType(val, float, 'enginePin must be an int!')
        self._enginePin = val

    @backwardPin.setter
    def backwardPin(self, val):
        error.checkType(val, float, 'backwardPin must be a float!')
        self._backwardPin = val

    @forwardPin.setter
    def forwardPin(self, val):
        error.checkType(val, float, 'forwardPin must be a float!')
        self._forwardPin = val
