# -*- coding: utf-8 -*-

from move import Move
from motor import Motor

leftMotor = Motor(4, 14, 15)
leftMotor.setup()

rightMotor = Motor(17, 27, 18)
rightMotor.setup()

robot = Move(Move.MAX_DC, leftMotor, rightMotor)
