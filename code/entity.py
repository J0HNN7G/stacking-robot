# -*- coding: utf-8 -*-

from enum import Enum, auto

class Entity(Enum):
    """An enum class for representing the direction of the robot."""
    FLOOR = auto()
    YELLOW = auto()
    BLUE = auto()
    RED = auto()
