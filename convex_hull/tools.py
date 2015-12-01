#coding=utf8

import math
from config import EPSILON

def is_float_num_equal(a, b , epsilon=EPSILON) :
    if abs(a - b) <= epsilon :
        return True
    else :
        return False

def calc_distance(pnt1 , pnt2) :
    return math.sqrt( (pnt1.x - pnt2.x)**2 + (pnt1.y - pnt2.y)**2 )
