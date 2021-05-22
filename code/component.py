# -*- coding: utf-8 -*-

import error
from abc import ABC, abstractmethod


class Component():
    """An abstract class for the hardware components of the robot."""


    @property
    def status(self):
        # type: None -> bool
        """
        Get the status of the component (on/off).

        :return: true if the component is on, false if if it is off
        """
        return self._status


    def __init__(self):
        # type: (...) -> (...)
        """Initialise the component."""
        pass


    def setup(self):
        # type: (...) -> (...)
        """Setup the component."""
        pass


    def cleanup(self):
        # type: (...) -> (...)
        """Cleanup the component."""
        pass


    @status.setter
    def status(self, status_val):
        # type: bool -> None
        """
        Set the status of the component (on/off).

        :param status_val: true if component is on, false if it is off
        :raise TypeError: if val is not a bool
        """
        error.checkType(status_val, bool, 'status must be a boolean!')
        self._status = status_val
