#coding=utf8

from tools import cross_product_2d
from config import EPSILON

def calc_line_params(line_pnt_a , line_pnt_b ) :
    w_1 = -(line_pnt_a.y - line_pnt_b.y)
    w_2 = line_pnt_a.x - line_pnt_b.x
    norm_factor = max(abs(w_1) , abs(w_2))
    if norm_factor >= 1000 : # IF |w_1| or |w_2| is too big , to normalize it !
        w_1 = w_1 / float(norm_factor)
        w_2 = w_2 / float(norm_factor)
    b = - (w_1 * line_pnt_a.x + w_2 * line_pnt_a.y)
    return ( w_1 , w_2 , b )

def is_in_same_side(line_pnt_a , line_pnt_b , test_pnt_a , test_pnt_b) :
    w_1 , w_2 , b = calc_line_params(line_pnt_a , line_pnt_b) 
    y_1 = w_1 * test_pnt_a.x + w_2 * test_pnt_a.y + b
    y_2 = w_1 * test_pnt_b.x + w_2 * test_pnt_b.y + b
    if y_1 * y_2 >= 0 :
        return True
    else :
        return False

def is_3pnts_in_one_line(pnt_a , pnt_b , pnt_c) :
    '''
    To know wheather 3 points are in one line 
    using cross product of 2 vector to judge . 
    if cross product of the 2 vector is zero , they are in one line !
    '''
    if abs(cross_product_2d(pnt_b - pnt_a , pnt_c - pnt_b) ) < EPSILON :
        return True
    else :
        return False

def is_in_rectangle(endpoint_a , endpoint_b , endpoint_c , p) :
    '''
    Return :
            -1 : endpoint  a , b , c is not a rectangle !!
            1  : p is in rectangle
            0  : p is not in rectangle 
    '''
    ##使用中文来说明：
    # 当多余三个点在一条直线上时，判断凸包的会出现问题！ 
    # 考虑一种特殊情况，凸包的一条边上，有4个点属于点集合，按照凸包的定义，只有端点的两个才是凸包点，中间的两个点不是！
    # 但是，在此情况下，如果按照暴力算法来判断凸包，即一个点是否在其余三个点围成的三角形内部。取三个点为两个中间点，
    # 再加一个端点，易知——如果我们以 点到直线距离的乘积 大于等于 0 作为在一边的判断依据，那么就会了另一个端点判断为
    # 在三角形内部，而将其认为非凸包 ！！
    # 这样就错了！
    # 错误的关键就在于，当如果有一个点到直线距离为0，即3点共线时，其根本构不成三角形！
    # 所以，我们必须先判断端点a，b，c能否构成三角形，然后才能判断p是否在三角形内部！
    if is_3pnts_in_one_line(endpoint_a , endpoint_b , endpoint_c) :
        return -1
    if ( is_in_same_side(endpoint_a , endpoint_b , endpoint_c , p) and 
         is_in_same_side(endpoint_a , endpoint_c , endpoint_b , p) and 
         is_in_same_side(endpoint_b , endpoint_c , endpoint_a , p) ) :
        return 1
    else :
        return 0


def find_convex_hull_bruteforce(pnts) :
    ## without the skip of every upper circulation , we get a long time cost :
    ## method-name          | pnt-nums=1000        | pnt-nums=2000        | pnt-nums=3000
    ## brute-force          |                10.93 |               145.42 |              1012.40
    # so we add the skip operation .
    pnt_num = len(pnts)
    if pnt_num < 3 : return []
    is_convex_hull = [True] * pnt_num
    for pnt_a_idx , pnt_a in enumerate(pnts) :
        # point A
        if not is_convex_hull[pnt_a_idx] : continue
        for pnt_b_idx , pnt_b in enumerate(pnts) :
            # point B
            if not is_convex_hull[pnt_b_idx] :continue
            if pnt_b_idx == pnt_a_idx : continue
            for pnt_c_idx , pnt_c in enumerate(pnts) :
                # point C
                if not is_convex_hull[pnt_c_idx] : continue
                if pnt_c_idx == pnt_b_idx or pnt_c_idx == pnt_a_idx : continue
                for pnt_test_idx , pnt_test in enumerate(pnts) :
                    # tesing point
                    if not is_convex_hull[pnt_test_idx] : continue
                    if pnt_test_idx in (pnt_a_idx , pnt_b_idx , pnt_c_idx) : continue
                    inner_rectangle_rst =  is_in_rectangle(pnt_a , pnt_b , pnt_c , pnt_test) 
                    if inner_rectangle_rst == 1 :
                        is_convex_hull[pnt_test_idx] = False
                    elif inner_rectangle_rst == -1 :
                        # a , b , c is in one line ! 
                        # we can abanon the inner pointer of line ( a , b , c )
                        inner_pnt , inner_pnt_idx = sorted(
                            [(pnt_a , pnt_a_idx) , (pnt_b , pnt_b_idx) , (pnt_c , pnt_c_idx)] ,
                            key=lambda t : ( t[0].x , t[0].y ) # in x , y increasing order 
                            )[1]
                        is_convex_hull[inner_pnt_idx] = False

    convex_hull_pnts = []
    for pnt_idx , pnt_is_convex_hull in enumerate(is_convex_hull) :
        if pnt_is_convex_hull :
            convex_hull_pnts.append(pnts[pnt_idx])
    return convex_hull_pnts

def ready_plot_pnts_bruteforce(convex_hull_pnts) :
    left_most_pnt = min(convex_hull_pnts , key=lambda p : p.x)
    right_most_pnt = max(convex_hull_pnts , key=lambda p : p.x)
    boundary_line = calc_line_params(left_most_pnt , right_most_pnt) # line = ( w_1 , w_2 , b )
    functional_margin = lambda p : boundary_line[0] * p.x + boundary_line[1] * p.y + boundary_line[2]
    pnts_up = [ p for p in convex_hull_pnts if functional_margin(p) >= 0 and p not in (left_most_pnt , right_most_pnt)]
    pnts_low = [ p for p in convex_hull_pnts if functional_margin(p) < 0 and p not in (left_most_pnt , right_most_pnt)]
    plot_pnts = []
    # first , push left most point
    plot_pnts.append(left_most_pnt)
    # then , push all the pointers below the boundary line .  the pnts shoule be sorted by the x-axis increasing
    sorted_pnts_low = sorted(pnts_low , key=lambda p : p.x)
    plot_pnts.extend(sorted_pnts_low)
    # then , push right most point
    plot_pnts.append(right_most_pnt) 
    # push higher points as the boundary line . sorted as x-axis decreasing !
    sorted_pnts_up = sorted(pnts_up , key=lambda p : p.x , reverse=True)
    plot_pnts.extend(sorted_pnts_up)
    # At last , push the left most point again to close the convex hull
    plot_pnts.append(left_most_pnt)
    return plot_pnts




