# -*- coding: utf-8 -*-

from move import Move
from motor import Motor

leftMotor = Motor(17, 18, 27)
rightMotor = Motor(4, 14, 15)

robot = Move(99.5, leftMotor, rightMotor)
