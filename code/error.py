# -*- coding: utf-8 -*-

# Minimum GPIO numbering.
GPIO_PIN_MIN = 1

# Maximum GPIO numbering.
GPIO_PIN_MAX = 27

# List of GPIO numberings
GPIO_PIN_LIST = [i for i in range(GPIO_PIN_MIN, GPIO_PIN_MAX+1)]

# Minimum PCA9685 numbering
PCA9685_PIN_MIN = 1

# Minimum PCA9685 numbering
PCA9685_PIN_MAX = 15

# List of PCA9685 numberings
PCA9685_PIN_LIST = [i for i in range(PCA9685_PIN_MIN, PCA9685_PIN_MAX+1)]


def checkType(val, classy, valName, className):
    """
    Check if the given value is the correct type. Use sparingly (this is python)
    after all.

    :param val: an object
    :param classy: a class
    :param valName: the name of the object
    :param className: the name of the class
    :raise TypeError: if given value is not a class instance
    """
    if not isinstance(val, classy):
        raise TypeError(f'Given {valName} is not a {className} instance')


def checkPositive(val):
    """
    Check if the given number is positive.

    :param val: a number
    :raise ValueError: if val is not larger than 0
    """
    if val <= 0:
        raise ValueError(f'Expected positive value but is: {val}')


def checkInRange(val, minVal, maxVal):
    """
    Check if the given value is between a minimum and maximum value (inclusive).

    :param val: a number
    :param minVal: minimum allowed value
    :param maxVal: maximum allowed value
    :raise ValueError: if val less than minVal or larger than maxVal
    """
    if (minVal > val) or (val > maxVal):
        raise ValueError(f'Expected {minVal} <= value <= {maxVal}, but value: {val}')


def checkGPIO(val):
    """
    Check if the given number is in the GPIO numbering

    :param val: a number
    :raise ValueError: if the val is not in the GPIO numbering
    """
    if val not in GPIO_PIN_LIST:
        raise ValueError(f"Expected GPIO pin numbering (1-27), but value: {val}")


def checkPCA9685(val):
    """
    Check if the given number is in the PCA9685 numbering

    :param val: a number
    :raise ValueError: if the val is not in the PCA9685 numbering
    """
    if val not in PCA9685_PIN_LIST:
        raise ValueError(f"Expected PCA9685 pin numbering (1-15), but value: {val}")


def checkComponent(component, component_name):
    """
    Check if the component is on.

    :param component: component
    :param component_name: name of the component
    :raise ValueError: if status is False
    """
    if not component.status:
        raise ValueError(component_name + ' is off')
