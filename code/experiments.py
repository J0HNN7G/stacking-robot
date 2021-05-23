# -*- coding: utf-8 -*-

from move import Move
from motor import Motor

leftMotor = Motor(4, 14, 15)
rightMotor = Motor(17, 18, 27)

robot = Move(Move.MAX_DC, leftMotor, rightMotor)
