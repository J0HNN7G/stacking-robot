# -*- coding: utf-8 -*-

from arm import Arm
from body import Body
from motor import Motor

leftMotor = Motor(17, 18, 27)
rightMotor = Motor(4, 14, 15)

body = Body(Body.MAX_MOTOR_DC, leftMotor, rightMotor)
arm = Arm(12,13,14,15)
