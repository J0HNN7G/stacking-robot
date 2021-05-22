# -*- coding: utf-8 -*-


def checkType(val, type, msg):
    # (<Type instance>, <Type>, str) -> (None || TypeError)
    """
    Check if the given value has the correct type.

    :param val: a type instance
    :param type: a type/class
    :param msg: message to be raised with TypeError
    :raise TypeError: if val is not of type
    """
    if not isinstance(val, type):
        raise TypeError(msg)


def checkPositive(val):
    # (number) -> (None || ValueError)
    """
    Check if the given number is positive.

    :param val: a number
    :raise ValueError: if val is not larger than 0
    """
    if val <= 0:
        raise ValueError(f'Expected positive value but is: {val}')


def checkInRange(val, minVal, maxVal):
    # (number, number, number) -> (None || ValueError)
    """
    Check if the given value is between a minimum and maximum value (inclusive).

    :param val: a number
    :param minVal: minimum allowed value
    :param maxVal: maximum allowed value
    :raise ValueError: if val less than minVal or larger than maxVal
    """
    if (minVal > val) or (val > maxVal):
        raise ValueError(f'Expected {minVal} <= value <= {maxVal}, but value: {val}')


def checkComponent(component, component_name):
    # (bool, string) -> (None || ValueError)
    """
    Check if the component is on.

    :param component: component
    :param component_name: name of the component
    :raise ValueError: if status is False
    """
    if not component.status():
        raise ValueError(component_name + ' is off')