#coding=utf8

import math
import random
from config import EPSILON

def is_float_num_equal(a, b , epsilon=EPSILON) :
    if abs(a - b) <= epsilon :
        return True
    else :
        return False

def calc_distance(pnt1 , pnt2) :
    return math.sqrt( (pnt1.x - pnt2.x)**2 + (pnt1.y - pnt2.y)**2 )

def cross_product_2d(pnt1 , pnt2) :
    return pnt1.x * pnt2.y - pnt1.y *pnt2.x

def randomized_select(l , i_th , key=None) :
    '''
    Implementation from <Introduction  to Algorithm> chapter 9 .
    Seletct i-th element in expected linear time ( O(N) ) .
    Main thought is using the quick-sort method . but we do slect instead of sort . 
    And random ensure that the algorithm has the expected time cost !
    l : list , 
    i_th , the i-th order , to element with the  i-th order should be selected . COUNTER FROM 1 !
    '''
    if not key :
        key = lambda e : e 
    l = l[:] # make a copy
    while True :
        pivot_idx = random.randrange(0, len(l))
        pivot = l[pivot_idx]
        ## partition 
        # 2n
        # first , swap the pivot element to the end !
        l[pivot_idx] , l[-1] = l[-1] , l[pivot_idx]
        # partition using the pivot element
        # left part is the elements less  than or equal to pivot , right is the bigger
        left_part = [ e for e in l[:-1] if key(e) <= key(pivot) ]
        right_part = [ e for e in l[:-1] if key(e) > key(pivot) ]
        pivot_order = len(left_part) + 1
        if pivot_order == i_th :
            return pivot
        elif pivot_order < i_th :
            # i-th element is at THE RIGHT PART !
            l = right_part
            # change the i-th value ! bacause we have ignore the pivot_order elements !
            i_th = i_th - pivot_order
        else :
            # i-th element is at THE LEFT PART !
            l = left_part


def get_min_and_max_value_and_index(l , cmp=cmp , key=None) :
    '''
    Implementation from <Introduction to Algorithm> . 
    -> cosing : 3n / 2 
    '''
    if not key :
        key = lambda x : x
    size = len(l)
    if size == 0 : return None , None , None , None
    if size == 1 : return l[0] , l[0] , 0, 0
    if size % 2 == 0 :
        if cmp(key(l[0]) , key(l[1])) < 0 :
            min_value = l[0]
            max_value = l[1]
            min_index = 0
            max_index = 1
        else :
            min_value = l[1]
            max_value = l[0]
            min_index , max_index = 1 , 0
        start_idx = 2
    else :
        min_value = l[0]
        max_value = l[0]
        min_index , max_index = 0 , 0
        start_idx = 1
    while start_idx < size :
        ele_1 = l[start_idx]
        ele_2 = l[start_idx+1]
        start_idx += 2
        if cmp(key(ele_1) , key(ele_2)) < 0 :
            local_min_value = ele_1 
            local_max_value = ele_2
            local_min_index = start_idx -2
            local_max_index = start_idx -1 
        else :
            local_min_value = ele_2
            local_max_value = ele_1
            local_min_index = start_idx -1
            local_max_index = start_idx -2
        if cmp(key(local_min_value) , key(min_value)) < 0 :
            min_value = local_min_value
            min_index = local_min_index
        if cmp(key(local_max_value) , key(max_value)) > 0 :
            max_value = local_max_value
            max_index = local_max_index
    return min_value , max_value , min_index , max_index


if __name__ == "__main__" :
    l = [ random.randint(1,4000) for i in range(300) ]
    print randomized_select(l , 15)
    print ( min(l) , max(l) )
    print get_min_and_max_value_and_index(l)