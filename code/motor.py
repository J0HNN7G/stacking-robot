# -*- coding: utf-8 -*-

import error
from component import Component

import RPi.GPIO as GPIO

class Motor(Component):
    """A class for controlling the wheel motors of the robot."""


    # Standard frequency (Hz) of PWM instance controlling motor engine.
    STD_MOTOR_FREQ = 1000


    def __init__(self, enginePin, backwardPin, forwardPin):
        """
        Initialise a motor with the GPIO numbered pins that control it.

        :param enginePin: GPIO number of pin controlling motor engine
        :param backwardPin: GPIO number of pin controlling backward motion
        :param forwardPin: GPIO number of pin controlling forward motion
        :raise ValueError: if enginePin, backwardPin, forwardPin is outside of
                           GPIO numbering
        """
        error.checkGPIO(enginePin)
        error.checkGPIO(backwardPin)
        error.checkGPIO(forwardPin)

        self.status = False
        self.enginePin = enginePin
        self.backwardPin = backwardPin
        self.forwardPin = forwardPin


    def setup(self):
        """
        Setup the motor for use.
        """
        GPIO.setwarnings(False)
        # Set to GPIO numbering
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins(), GPIO.OUT, initial=GPIO.LOW)
        try:
            # Create PWM instance and output
            self.pwm = GPIO.PWM(self.enginePin, self.STD_MOTOR_FREQ)
            self.status = True
        except Exception as e:
            print(e)
            self.cleanup()


    def cleanup(self):
        """
        Cleanup the motor.
        """
        self.stop()
        GPIO.cleanup(self.pins())
        self.status = False


    def stop(self):
        """
        Stop the motor.
        """
        self.pwm.stop()
        GPIO.output(self.pins(), GPIO.LOW)


    def pins(self):
        """
        Get a list of the pins

        :return: list of enginePin, forwardPin and backwardPin
        """
        return [self.enginePin, self.backwardPin, self.forwardPin]
