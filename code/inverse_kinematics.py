# -*- coding: utf-8 -*-

import math


# The length of the shoulder in metres.
S_LEN = 0.065

# The length of the elbow in metres.
E_LEN = 0.13

# The precision of the angles returned.
PRECISION = 3

# Conversion factor from radians to degrees.
RAD_TO_DEG = 180 / math.pi


def calcAngles(objPos):
    """
    Calculate the angle of the shoulder and the elbow so that
    the grabber is positioned to pickup the object (assuming
    the object shape is simple).

    :param objPos: the cartesian coordinates of the object position
                   relative to the shoulder axis in metres
    :return: the shoulder angle and elbow angle for the arm to reach
             the object, or None is the object is not reachable
    """
    result = None
    xObj, yObj = objPos
    # distance between shoulder axis and target
    tDist = round( math.sqrt(xObj**2 + yObj**2), PRECISION)

    if not ((tDist > S_LEN + E_LEN) or (tDist < E_LEN - S_LEN)):
        # distance from shoulder axis to chord between potential elbow positions
        sDist = (S_LEN**2 - E_LEN**2 + tDist**2) / (2*tDist)
        # distance from chord between potential elbow positions to elbow positions
        hlfChdDist = round( math.sqrt(S_LEN ** 2 - sDist**2), PRECISION)

        # coordinates for the middle of the chord between the potential elbow positions
        xHlfMdPt = sDist * xObj / tDist
        yHlfMdPt = sDist * yObj / tDist

        elbowPos = ( round(xHlfMdPt + (hlfChdDist * yObj) / tDist, PRECISION),
                     round(yHlfMdPt - (hlfChdDist * xObj) / tDist, PRECISION))
        shoulderAngle = round( math.atan2(elbowPos[1], elbowPos[0]) * RAD_TO_DEG, PRECISION)

        xTrans, yTrans = transPos(elbowPos, objPos)
        elbowAngle =  round( math.atan2(yTrans, xTrans) * RAD_TO_DEG, PRECISION)

        result = shoulderAngle, elbowAngle

    print(objPos)
    print(math.sqrt(xObj**2 + yObj**2))
    print((tDist > S_LEN + E_LEN))
    print((tDist < E_LEN - S_LEN))
    print(result)

    return result


def transPos(elbowPos, objPos):
    """
    Change the orientation of the axis and origin to the elbow position so
    that we can calculate the angle of the elbow to reach the object position.

    :param elbowPos: the cartesian coordinates of the elbow position
                     relative to the shoulder axis in metres
    :param objPos: the cartesian coordinates of the object position
                   relative to the shoulder axis in metres
    :return: the cartesian coordinates of the object position relative
             to the elbow position with orientation of the vector
             from origin to the elbow position in metres
    """
    x1, y1 = elbowPos
    x2, y2 = objPos

    mag1 = math.sqrt(x1**2 + y1**2)
    xTrans = (x1*x2 + y1*y2 - mag1**2) / mag1
    yTrans = (x1*y2 - y1*x2) / mag1

    return xTrans, yTrans
