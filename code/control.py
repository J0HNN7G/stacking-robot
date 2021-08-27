# -*- coding: utf-8 -*-

import error

class Control():
    def __init__(self, arm):
        self.arm = arm
        self.shoulderAngle = None
        self.elbowAngle = None
        self.wristAngle = None
        self.grabberAngle = None

    def execute(self):
        

    def shoulder(self, angle):
        error.checkInRange(angle, self.arm.SHOULDER_MIN_DOM, self.arm.SHOULDER_MAX_DOM)
        self.shoulderAngle = angle

    def elbow(self, angle):
        error.checkInRange(angle, self.arm.ELBOW_MIN_DOM, self.arm.ELBOW_MAX_DOM)
        self.elbowAngle = angle

    def wrist(self, angle):
        error.checkInRange(angle, self.arm.MIN_ANGLE, self.arm.MAX_ANGLE)
        self.wristAngle = angle

    def grabber(self, angle):
        error.checkInRange(angle, self.arm.MIN_ANGLE, self.arm.GRABBER_DOM)
        self.grabberAngle = angle