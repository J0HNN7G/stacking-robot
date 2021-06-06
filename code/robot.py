
import error
from component import Component
from inverse_kinematics import calcAngles
from arm import Arm

import time

class Robot(Component):

    # Time for grabber to open
    OPEN_TIME = 0.5

    # Time for grabber to grab
    CLOSE_TIME = 1

    def __init__(self, head, body, arm):
        self.status = False
        self.head = head
        self.body = body
        self.arm = arm


    def setup(self):
        if not self.head.status:
            self.head.setup()
        if not self.arm.status:
            self.arm.setup()
        self.body.setup()
        self.status = True


    def cleanup(self):
        head.cleanup()
        body.cleanup()
        arm.cleanup()
        self.status = False


    def pickup(self):
        error.checkComponent(self, 'Robot')

        result = False
        objPos = self.head.objPos()
        print(objPos)
        angles = calcAngles(objPos)
        print(angles)

        if angles is not None:
            shoulderAngle, elbowAngle = angles

            if (Arm.SHOULDER_MIN_DOM <= shoulderAngle <= Arm.SHOULDER_MAX_DOM) and (Arm.ELBOW_MIN_DOM <= elbowAngle <= Arm.ELBOW_MAX_DOM):
                self.arm.grabber = 0
                time.sleep(self.OPEN_TIME)
                self.arm.shoulder = shoulderAngle
                self.arm.elbowAngle = elbowAngle
                time.sleep(self.CLOSE_TIME)
                self.arm.grabber = 90
                time.sleep(self.CLOSE_TIME)
                self.arm.setup()
                result = True
        return result
