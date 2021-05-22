# -*- coding: utf-8 -*-

import error
import component
import RPi.GPIO as GPIO


class Motor(component.Component):
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
        GPIO.setup(self._pins(), GPIO.OUT)

        self.stop()
        try:
            # Create PWM instance and output
            self._pwm(GPIO.PWM(self.enginePin(), self.STD_FREQ))
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
        GPIO.cleanup(self._pins())
        self._status(False)


    def stop(self):
        # type: None -> None
        """
        Stop the motor.
        """
        self.pwm().stop()
        GPIO.output(self._pins(), GPIO.LOW)


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


    def _pins(self):
        # type: None -> [int]
        """
        Get a list of the pins

        :return: list of enginePin, forwardPin and backwardPin
        """
        return [self.enginePin(), self.backwardPin(), self.forwardPin()]


    def _pwm(self, pwm):
        # type: (GPIO.PWM) -> None
        """
        Set the PWM instance controlling the motor engine.

        :param pwm: the PWM instance controlling the motor engine.
        :raise TypeError: if val is not 'GPIO.PWM'
        """
        error.checkType(pwm, GPIO.PWM, 'pwm must be of type GPIO.PWM!')
        self._pwm = pwm


    def _radius(self, radius):
        # type: (float) -> None
        """
        Set the radius of the motor's wheel.

        :param radius: the radius of the motor's wheel in millimetres
        :raise TypeError: if val is not a float
        :raise ValueError: if val is not positive
        """
        error.checkType(radius, float, 'radius must be a float!')
        error.checkPositive(radius)
        self._radius = radius


    def _enginePin(self, enginePin):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling motor engine.

        :param enginePin: GPIO number of pin controlling motor engine
        :raise TypeError: if val is not an int
        :raise ValueError: if val is outside of GPIO numbering range
        """
        error.checkType(enginePin, int, 'enginePin must be an int!')
        error.checkInRange(enginePin, self.GPIO_PIN_MIN, self.GPIO_PIN_MAX)
        self._enginePin = enginePin


    def _backwardPin(self, backwardPin):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling backward motion.

        :param backwardPin: GPIO number of pin controlling backward motion
        :raise TypeError: if val is not an int
        :raise ValueError: if val is outside of GPIO numbering range
        """
        error.checkType(backwardPin, int, 'backwardPin must be an int!')
        error.checkInRange(backwardPin, self.GPIO_PIN_MIN, self.GPIO_PIN_MAX)
        self._backwardPin = backwardPin


    def _forwardPin(self, forwardPin):
        # type: (int) -> None
        """
        Set the GPIO number of pin controlling forward motion

        :param forwardPin: GPIO number of pin controlling forward motion
        :raise TypeError: if val is not an int
        :raise ValueError: if val is outside of GPIO numbering range
        """
        error.checkType(forwardPin, int, 'forwardPin must be an int!')
        error.checkInRange(forwardPin, self.GPIO_PIN_MIN, self.GPIO_PIN_MAX)
        self._forwardPin = forwardPin
