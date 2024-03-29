# -*- coding: utf-8 -*-

from arm import Arm
from head import Head
from ultrasonic import Ultrasonic
from body import Body
from motor import Motor
from robot import Robot

body = Body(Body.MAX_MOTOR_DC, Motor(17, 18, 27), Motor(4, 14, 15))
arm = Arm(12,13,14,15)
head = Head(11, Ultrasonic(11,8))
robot = Robot(head, body, arm)

robot.setup()
