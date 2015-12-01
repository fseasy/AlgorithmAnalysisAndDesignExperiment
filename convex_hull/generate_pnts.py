#coding=utf8

import random
import time

from config import MAX_WIDTH , MAX_HEIGHT , STATIC_RANDOM_SEED
from point import Point


def generate_pnts_in_random(pnt_num , max_width=MAX_WIDTH , max_height=MAX_HEIGHT , is_static_random=True) :
    '''
    Randomly generate points in selected area
    不能有重复点！！
    NO POINT IS SAME !!
    '''
    if is_static_random : random.seed(STATIC_RANDOM_SEED)
    else : random.seed(time.time())
    all_pnts = [(x,y) for x in range(max_width) for y in range(max_height)]
    select_pnts = random.sample(all_pnts , pnt_num)
    pnts = [Point(x,y) for (x, y) in select_pnts ]
    
    return pnts

