# -*- coding: utf-8 -*-

import error
import component
import RPi.GPIO as GPIO

class Motor(component.Component):
    """A class for controlling the wheel motors of the robot."""

    # Standard frequency (Hz) of PWM instance controlling motor engine.
    STD_FREQ = 1000

    @property
    def pwm(self):
        # type: None -> GPIO.PWM
        """
        Get the PWM instance controlling the motor engine.

        :return: PWM instance controlling the motor engine
        """
        return self._pwm

    @property
    def radius(self):
        # type: None -> bool
        """
        Get the radius of the motor's wheel.

        :return: the radius of the motor's wheel in millimetres
        """
        return self._radius

    @property
    def enginePin(self):
        # type: None -> int
        """
        Get the GPIO number of pin controlling the motor engine.

        :return: GPIO number of pin controlling the motor engine
        """
        return self._enginePin

    @property
    def backwardPin(self):
        # type: None -> int
        """
        Get the GPIO number of pin controlling the backward motion.

        :return: GPIO number of pin controlling the backward motion
        """
        return self._backwardPin

    @property
    def forwardPin(self):
        # type: None -> int
        """
        Get the GPIO number of pin controlling the forward motion.

        :return: GPIO number of pin controlling the forward motion
        """
        return self._forwardPin

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
        status(False)
        radius(radius)
        enginePin(enginePin)
        backwardPin(backwardPin)
        forwardPin(forwardPin)

    def setup(self):
        # type: None -> None
        """
        Setup the motor for use.
        """
        GPIO.setwarnings(False)
        # Set to GPIO numbering
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(enginePin(), GPIO.OUT)
    	GPIO.setup(backwardPin(), GPIO.OUT)
    	GPIO.setup(forwardPin(), GPIO.OUT)

        stop()
        try:
            # Create PWM instance and output
            pwm(GPIO.PWM(enginePin(), STD_FREQ))
            status(True)
        except Exception as e:
            print(e)
            cleanup()

    def cleanup(self):
        # type: None -> None
        """
        Cleanup the motor.
        """
        stop()
        GPIO.cleanup([enginePin(), backwardPin(), forwardPin()])
        status(False)

    def stop(self):
        # type: None -> None
        """
        Stop the motor.
        """
        GPIO.output(enginePin(), GPIO.LOW)
        GPIO.output(backwardPin(), GPIO.LOW)
        GPIO.output(forwardPin(), GPIO.LOW)

    @pwm.setter
    def pwm(self, val):
        # type: (GPIO.PWM) -> None
        """
        Set the PWM instance controlling the motor engine.

        :param val: the PWM instance controlling the motor engine.
        :raise TypeError: if val is not 'GPIO.PWM'
        """
        error.checkType(val, GPIO.PWM, 'pwm must be of type GPIO.PWM!')
        self._pwm = val

    @radius.setter
    def radius(self, val):
        # type: (float) -> None
        """
        Set the radius of the motor's wheel.

        :param val: the radius of the motor's wheel in millimetres
        :raise TypeError: if val is not a float
        """
        error.checkType(val, float, 'radius must be a float!')
        self._radius = val

    @enginePin.setter
    def enginePin(self, val):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling motor engine.

        :param val: GPIO number of pin controlling motor engine
        :raise TypeError: if val is not an int
        """
        error.checkType(val, float, 'enginePin must be an int!')
        self._enginePin = val

    @backwardPin.setter
    def backwardPin(self, val):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling backward motion.

        :param val: GPIO number of pin controlling backward motion
        :raise TypeError: if val is not an int
        """
        error.checkType(val, float, 'backwardPin must be a float!')
        self._backwardPin = val

    @forwardPin.setter
    def forwardPin(self, val):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling forward motion

        :param val: GPIO number of pin controlling forward motion
        :raise TypeError: if val is not an int
        """
        error.checkType(val, float, 'forwardPin must be a float!')
        self._forwardPin = val
