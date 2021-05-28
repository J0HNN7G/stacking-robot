# -*- coding: utf-8 -*-

from move import Move
from motor import Motor

leftMotor = Motor(4, 14, 15)
rightMotor = Motor(17, 18, 27)

robot = Move(99.5, leftMotor, rightMotor)
