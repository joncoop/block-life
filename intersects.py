#  Copyright (c) 2016 Jon Cooper
#   
#  This file is part of py-collide.
#  Documentation, related files, and licensing can be found at
# 
#      <https://github.com/joncoop/py-collide>.

"""
Parameter definitions for the intersects module:

A point is defined by a list or tuple in the form [x, y] or (x, y).

A circle is defined as a list or tuple in the form [x, y, r] 
where (x, y) represents the center of the circle and r is its radius.

A rect is defined as a list or tuple in the form [x, y, width, height] 
where (x, y) represents the coordinates of the upper left corner of 
the rectangle.
"""

import math

def point_circle(point, circle):
    a = point[0] - circle[0]
    b = point[1] - circle[1]
    r = circle[2]

    return a**2 + b**2 <= r**2


def point_rect(point, rect):
    x = point[0]
    y = point[1]

    left = rect[0]
    right = rect[0] + rect[2] - 1
    top = rect[1]
    bottom = rect[1] + rect[3] - 1

    return left <= x <= right and top <= y <= bottom


def circle_circle(circle1, circle2):
    a = circle1[0] - circle2[0] 
    b = circle1[1] - circle2[1]
    r_sum = circle1[2] + circle2[2]

    return a**2 + b**2 <= r_sum**2


def rect_rect(rect1, rect2):
    left1 = rect1[0]
    right1 = rect1[0] + rect1[2] - 1
    top1 = rect1[1]
    bottom1 = rect1[1] + rect1[3] - 1

    left2 = rect2[0]
    right2 = rect2[0] + rect2[2] - 1
    top2 = rect2[1]
    bottom2 = rect2[1] + rect2[3] - 1

    return not (right1 < left2 or right2 < left1 or
                bottom1 < top2 or bottom2 < top1)











