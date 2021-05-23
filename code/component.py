# -*- coding: utf-8 -*-

import error
from abc import ABC, abstractmethod


class Component(ABC):
    """An abstract class for the hardware components of the robot."""


    @abstractmethod
    def setup(self):
        """Setup the component."""
        pass


    @abstractmethod
    def cleanup(self):
        """Cleanup the component."""
        pass
