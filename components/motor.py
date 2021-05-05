# -*- coding: utf-8 -*-

import error
from component
import RPi.GPIO as GPIO


class Motor(component.Component):
    """A class for controlling the wheel motors of the robot."""


    # Standard frequency (Hz) of PWM instance controlling motor engine.
    STD_FREQ = 1000

    # Minimum GPIO numbering value.
    GPIO_PIN_MIN = 4

    # Maximum GPIO numbering value.
    GPIO_PIN_MAX = 26


    def __init__(self, radius, enginePin, backwardPin, forwardPin):
        # type: (float, int, int, int) -> None
        """
        Initialise a motor with the radius of the wheel it spins and the
        GPIO numbered pins that control it.

        :param radius: the radius of the motor's wheel in millimetres
        :param enginePin: GPIO number of pin controlling motor engine
        :param backwardPin: GPIO number of pin controlling backward motion
        :param forwardPin: GPIO number of pin controlling forward motion
        """
        self._status(False)
        self._radius(radius)
        self._enginePin(enginePin)
        self._backwardPin(backwardPin)
        self._forwardPin(forwardPin)


    def setup(self):
        # type: None -> None
        """
        Setup the motor for use.
        """
        GPIO.setwarnings(False)
        # Set to GPIO numbering
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enginePin(), GPIO.OUT)
        GPIO.setup(self.backwardPin(), GPIO.OUT)
        GPIO.setup(self.forwardPin(), GPIO.OUT)

        self.stop()
        try:
            # Create PWM instance and output
            self.pwm(GPIO.PWM(self.enginePin(), STD_FREQ))
            self._status(True)
        except Exception as e:
            print(e)
            self.cleanup()


    def cleanup(self):
        # type: None -> None
        """
        Cleanup the motor.
        """
        self.stop()
        GPIO.cleanup([self.enginePin(), self.backwardPin(), self.forwardPin()])
        self._status(False)


    def stop(self):
        # type: None -> None
        """
        Stop the motor.
        """
        GPIO.output(self.enginePin(), GPIO.LOW)
        GPIO.output(self.backwardPin(), GPIO.LOW)
        GPIO.output(self.forwardPin(), GPIO.LOW)


    def pwm(self):
        # type: None -> GPIO.PWM
        """
        Get the PWM instance controlling the motor engine.

        :return: PWM instance controlling the motor engine
        """
        return self._pwm


    def radius(self):
        # type: None -> bool
        """
        Get the radius of the motor's wheel.

        :return: the radius of the motor's wheel in millimetres
        """
        return self._radius


    def enginePin(self):
        # type: None -> int
        """
        Get the GPIO number of pin controlling the motor engine.

        :return: GPIO number of pin controlling the motor engine
        """
        return self._enginePin


    def backwardPin(self):
        # type: None -> int
        """
        Get the GPIO number of pin controlling the backward motion.

        :return: GPIO number of pin controlling the backward motion
        """
        return self._backwardPin


    def forwardPin(self):
        # type: None -> int
        """
        Get the GPIO number of pin controlling the forward motion.

        :return: GPIO number of pin controlling the forward motion
        """
        return self._forwardPin


    def _pwm(self, val):
        # type: (GPIO.PWM) -> None
        """
        Set the PWM instance controlling the motor engine.

        :param val: the PWM instance controlling the motor engine.
        :raise TypeError: if val is not 'GPIO.PWM'
        """
        error.checkType(val, GPIO.PWM, 'pwm must be of type GPIO.PWM!')
        self._pwm = val


    def _radius(self, val):
        # type: (float) -> None
        """
        Set the radius of the motor's wheel.

        :param val: the radius of the motor's wheel in millimetres
        :raise TypeError: if val is not a float
        :raise ValueError: if val is not positive
        """
        error.checkType(val, float, 'radius must be a float!')
        error.checkPositive(val)
        self._radius = val


    def _enginePin(self, val):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling motor engine.

        :param val: GPIO number of pin controlling motor engine
        :raise TypeError: if val is not an int
        :raise ValueError: if val is outside of GPIO numbering range
        """
        error.checkType(val, int, 'enginePin must be an int!')
        error.checkInRange(val, GPIO_PIN_MIN, GPIO_PIN_MAX)
        self._enginePin = val


    def _backwardPin(self, val):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling backward motion.

        :param val: GPIO number of pin controlling backward motion
        :raise TypeError: if val is not an int
        :raise ValueError: if val is outside of GPIO numbering range
        """
        error.checkType(val, int, 'backwardPin must be an int!')
        error.checkInRange(val, GPIO_PIN_MIN, GPIO_PIN_MAX)
        self._backwardPin = val


    def _forwardPin(self, val):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling forward motion

        :param val: GPIO number of pin controlling forward motion
        :raise TypeError: if val is not an int
        :raise ValueError: if val is outside of GPIO numbering range
        """
        error.checkType(val, int, 'forwardPin must be an int!')
        error.checkInRange(val, GPIO_PIN_MIN, GPIO_PIN_MAX)
        self._forwardPin = val
