# -*- coding: utf-8 -*-

import math


def origToPosAngle(pos):
    x, y = pos
    inQuad3 = x < 0 and y < 0
    inQuad4 = x > 0 and y < 0
    origin = x == 0 and y == 0

    if inQuad3 or inQuad4 or origin:
        pass
    else:
        return math.atan2(y, x)
