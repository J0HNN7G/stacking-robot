# -*- coding: utf-8 -*-

import error
import time
import math

class Control():

    ANGLE_INC = 5
    SLEEPY_TIME = 0.1

    def __init__(self, arm):
        self.arm = arm
        self.shoulderAngle = None
        self.elbowAngle = None
        self.wristAngle = None
        self.grabberAngle = None

    def execute(self):
        error.checkComponent(self.arm, 'Arm')

        while not((self.shoulderAngle is None) and (self.elbowAngle is None) and (self.wristAngle is None) and (self.grabberAngle is None)):

            print(self.shoulderAngle, self.arm.shoulder)
            print(self.elbowAngle, self.arm.elbow)
            print(self.wristAngle, self.arm.wrist)
            print(self.grabberAngle, self.arm.grabber)      

            if self.shoulderAngle is not None:
                angleDiff = self.shoulderAngle - self.arm.shoulder
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.shoulder = self.arm.shoulder + change

                if self.arm.shoulder == self.shoulderAngle:
                    self.shoulderAngle = None

            if self.elbowAngle is not None:
                angleDiff = self.elbowAngle - self.arm.elbow
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.elbow = self.arm.elbow + change

                if self.arm.elbow == self.elbowAngle:
                    self.elbowAngle = None

            if self.wristAngle is not None:
                angleDiff = self.wristAngle - self.arm.wrist
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.wrist = self.arm.wrist + change

                if self.arm.wrist == self.wristAngle:
                    self.wristAngle = None

            if self.grabberAngle is not None:
                angleDiff = self.grabberAngle - self.arm.grabber
                change = min(abs(angleDiff), self.ANGLE_INC)*math.copysign(1, angleDiff)
                self.arm.grabber = self.arm.grabber + change

                if self.arm.grabber == self.grabberAngle:
                    self.grabberAngle = None

            time.sleep(self.SLEEPY_TIME)

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
