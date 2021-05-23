# -*- coding: utf-8 -*-

import error
from component import Component

import RPi.GPIO as GPIO


class Motor(Component):
    """A class for controlling the wheel motors of the robot."""


    # Standard frequency (Hz) of PWM instance controlling motor engine.
    STD_FREQ = 1000

    # Minimum GPIO numbering value.
    GPIO_PIN_MIN = 1

    # Maximum GPIO numbering value.
    GPIO_PIN_MAX = 27

    # Standard radius (?)
    STD_RADIUS = 0.6


    def __init__(self, enginePin, backwardPin, forwardPin, radius = STD_RADIUS):
        """
        Initialise a motor with the radius of the wheel it spins and the
        GPIO numbered pins that control it.

        :param radius: the radius of the motor's wheel in millimetres
        :param enginePin: GPIO number of pin controlling motor engine
        :param backwardPin: GPIO number of pin controlling backward motion
        :param forwardPin: GPIO number of pin controlling forward motion
        :raise ValueError: if enginePin, backwardPin, forwardPin is outside of
                           GPIO numbering, or radius is not positive
        """
        error.checkGPIO(enginePin, self.GPIO_PIN_MIN, self.GPIO_PIN_MAX)
        error.checkGPIO(backwardPin, self.GPIO_PIN_MIN, self.GPIO_PIN_MAX)
        error.checkGPIO(forwardPin, self.GPIO_PIN_MIN, self.GPIO_PIN_MAX)
        error.checkPositive(radius)

        super().__init__()
        self.enginePin = enginePin
        self.backwardPin = backwardPin
        self.forwardPin = forwardPin
        self.radius = radius


    def setup(self):
        """
        Setup the motor for use.
        """
        GPIO.setwarnings(False)
        # Set to GPIO numbering
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins(), GPIO.OUT)

        self.stop()
        try:
            # Create PWM instance and output
            self.pwm = GPIO.PWM(self.enginePin, self.STD_FREQ)
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
        GPIO.output(self.pins(), GPIO.LOW)


    def pins(self):
        """
        Get a list of the pins

        :return: list of enginePin, forwardPin and backwardPin
        """
        return [self.enginePin, self.backwardPin, self.forwardPin]
