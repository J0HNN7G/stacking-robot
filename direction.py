# -*- coding: utf-8 -*-

from enum import Enum, auto


class Direction(Enum):
    """An enum class for representing the direction of the robot."""
    FORWARD = auto()
    BACKWARD = auto()
