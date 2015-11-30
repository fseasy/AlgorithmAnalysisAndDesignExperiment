#coding=utf8

import random
import time

from config import MAX_WIDTH , MAX_HEIGHT , STATIC_RANDOM_SEED
from point import Point


def generate_pnts_in_random(pnt_nums , max_width=MAX_WIDTH , max_height=MAX_HEIGHT , is_static_random=True) :
    if is_static_random : random.seed(STATIC_RANDOM_SEED)
    else random.seed(time.time())
    pnts = []
    for i in range(pnt_nums) :
        x = int(random.random() * max_width )
        y = int(random.random() * max_height )
        p = Point(x , y)
        pnts.append(p)
    return pnts

