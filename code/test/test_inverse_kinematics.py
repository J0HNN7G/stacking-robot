# -*- coding: utf-8 -*-

from code import inverse_kinematics
import pytest


TEST_SET_1 = [((-0.175,-0.035), (150.69, 58.898)),
              ((-0.099,0.143), (81.119, 62.947)),
              ((0.042,-0.167), (-122.471, 66.98)),
              ((-0.207,0.047), None), # Too far
              ((0,0),None)] # Too close

TEST_SET_2 = [(((-3.3,5.6), (-16.8,4.6)), (5.992307692307693, 12.138461538461542)),
              (((-4.7,4.5), (-8.9,-8.3)), (-5.818421545980189, 12.150142826867242))]


def test_calcAngles():
    for (test, sol) in TEST_SET_1:
        assert inverse_kinematics.calcAngles(test) == sol


def test_transPos():
    for ((param1, param2), sol) in TEST_SET_2:
        assert inverse_kinematics.transPos(param1, param2) == sol
