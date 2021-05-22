# -*- coding: utf-8 -*-

from move import Move
from components.motor import Motor

leftMotor = Motor(4, 14, 15)
rightMotor = Motor(17, 27, 18)

leftMotor.setup()
rightMotor.setup()

robot = Move(Move.MAX_DC, leftMotor, rightMotor)