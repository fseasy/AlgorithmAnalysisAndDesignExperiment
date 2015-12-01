#coding=utf8

import math
from config import EPSILON
from tools import ( is_float_num_equal ,
                    calc_distance )

def sort_pnts_by_polar_angle_ccw(origin_pnt , other_pnts , cmp_func_using_cosine=False) :
    other_pnts = other_pnts[:] # make a copy to avoid change the origin data !
    # First , define the compare function for sort by polar angle
    def polar_angle_cmp_func_using_cross_product(p1 , p2) :
        '''
        According to the `cross product result` of two vector to decide which polar angle is big  
        Cross product : the result is also a vector , for a 2-d vector , the result may be hard to explain directly
                        We can expand the vector of 2-d to 3-d , add a zero to the z-index .
                        For example :
                        p1 = (x1 , y1) , p2 = (x2 , y2)
                        => expand the 2-d vector to 3-d 
                        p1 = (x1 , y1 , z1=0) , p2 = (x2 , y2 , z2 = 0)

                        Corss product for 3-d vector :

                        p1 x p2 = ( y1z2 - z1y2 , z1x2 - x1z2 , x1y2 - y1x2 )
                                = (0 , 0 , x1y2 - y1x2 )

                        So , we just need to calc the result of `x1 * y2 - y1 * x2` , the corss product result 
                        is get ! 

                        What's more , according to `right hand rule` , if the polar angle of vector p1 is bigger than 
                        p2 , the direction of corss product is to inner(down) , which means a nagative number of 
                        `x1y2 - y1x2` . so the sign of `x1y2 - y1x2` can be used to jude which polar angle is bigger
                        for p1 , p2  

                        formally :
                        p1 x p2 =  x1y2 - y1x2 
                        sign(p1 x p2) > 0 : angle of p1 is smaller  , return -1
                        sign(p1 x p2) < 0 : angle of p1 is bigger , return 1 
                        sign(p1 x p2) = 0 : equals 
        if cross result equals to zero , we using the distance to give the compare the point
        '''
        vector_p1 = ( p1.x - origin_pnt.x , p1.y - origin_pnt.y )
        vector_p2 = ( p2.x - origin_pnt.x , p2.y - origin_pnt.y )
        cross_result = vector_p1[0] * vector_p2[1] - vector_p1[1] * vector_p2[0] 
        ## !! if it is float , the equal may be dangerous ! so using |a -b | < epsilon instead !
        if abs(cross_result) < EPSILON :
            return cmp(calc_distance(origin_pnt , p1) , calc_distance(origin_pnt , p2))
        elif cross_result > 0 :
            return -1
        else :
            return 1 
            

    def polar_angle_cmp_func_using_cosine(p1 , p2) :
        '''
        This directly calc the cosine result of vector p1 , p2 (in fact , it should be based on the origin point)
        because cosine is decreasing at the range (0 , PI) , so if cosine(p1 , origin_pnt) if bigger than cosine(p2 , origin_pnt)
        the angle of p1 is less than p2 .

        It may be necessary to normalize the ponit(vector) , as the origin point to the origin_pnt instead of (0,0)
        so , p1 = p1 - origin_pnt 
             p2 = p2 - origin_pnt

        define the 0-degree point (1,0) , the cosine func can be defined like follow :

        0-degree : (1,0) , let p0 to be the 0-degree 

        cost<p0 , p1> = \frac{p0 \cdot p1 }{|p0| * |p1|}
                      = \frac{ p0.x }{ |p0| }

        formally :

            normalize p1 , p2

            cos(p1) > cos(p2) : angle of p1 is smaller , return -1
            cos(p1) < cos(p2) : angle of p1 is bigger , return 1
            cos(p1) = cos(p2) : equals 

        Like previous , if equals in degree , using distance to sort
        '''
        norm_p1 = (p1.x - origin_pnt.x , p1.y - origin_pnt.y)
        norm_p2 = (p2.x - origin_pnt.x , p2.y - origin_pnt.y)
        if norm_p1 == (0,0) : # In fact , it can not be (0,0) if NO SAME POINT 
            return 1  # origin point is thought has the maximum polar angle ! 
        elif norm_p2 == (0,0) :
            return -1
        calc_cos_to_0_degree = lambda pt : (pt[0]) / ( math.sqrt( pt[0]**2 + pt[1]**2  ) )
        cos_p1 = calc_cos_to_0_degree(norm_p1)
        cos_p2 = calc_cos_to_0_degree(norm_p2)
        ## !! Attation ! because using math.sqrt , it is a float ! so equal should be judgement 
        ## ~~ using abs(a - b) < epsilon ! 
        if is_float_num_equal(cos_p1 , cos_p2) :
            return  cmp(calc_distance(origin_pnt , p1 ) , calc_distance(origin_pnt , p2))
        elif cos_p1 > cos_p2 :
            return -1
        else :
            return 1
    # sort 
    if cmp_func_using_cosine :
        cmp_func = polar_angle_cmp_func_using_cosine
    else :
        cmp_func = polar_angle_cmp_func_using_cross_product
    sorted_pnts = sorted(other_pnts , cmp=cmp_func)
    return sorted_pnts



def find_convex_hull_grahamscan(pnts) :
    pnts_copy = pnts[:] # we have some operation that will change the array . so copy it !
    pnt_num = len(pnts_copy)
    if pnt_num < 3 : return []
    convex_hull_stack = []
    # find the points with the minimal y-value
    lowest_pnt = min(pnts_copy , key=lambda p : p.y)
    # get other points except the lowest point
    pnts_copy.remove(lowest_pnt) # because There is NO SAME POINTS in the pnt ! so we can just remove it !
    other_pnts = pnts_copy
    # sort points in decreasing counterclockwise order . 
    sorted_pnts = sort_pnts_by_polar_angle_ccw(lowest_pnt , other_pnts)
    ## graham-scan
    # init
    convex_hull_stack.append(lowest_pnt)
    convex_hull_stack.append(sorted_pnts[0])
    convex_hull_stack.append(sorted_pnts[1])
    # circle
    for test_pnt in sorted_pnts[2:] :
        while True :
            stack_top_pnt = convex_hull_stack[-1]
            stack_undertop_pnt = convex_hull_stack[-2]
            vector_undertop2top = (stack_top_pnt.x - stack_undertop_pnt.x , stack_top_pnt.y - stack_undertop_pnt.y)
            vector_top2test = (test_pnt.x - stack_top_pnt.x , test_pnt.y - stack_top_pnt.y)
            # using cross product to distinguish wheather 'TO LEFT' 
            # if 'TO LEFT' , vector_undertop2top x vector_top2test > 0 ! 
            # if < 0 , then 'TO RIGHT' , pop stack top and continue ~ 
            # if = 0 ? As written in PPT , we think it is also not the convex hull !
            cross_product_rst = vector_undertop2top[0]*vector_top2test[1] - vector_undertop2top[1]*vector_top2test[0]
            if abs(cross_product_rst) <= EPSILON : # equal
                convex_hull_stack.pop() # pop and continue
            elif cross_product_rst < 0 : # It may be redundant . But it is MORE CLEARLY !
                convex_hull_stack.pop()
            else :
                convex_hull_stack.append(test_pnt)
                break
    
    return convex_hull_stack

def ready_plot_pnts_grahamscan(convex_hull_stack) :
    return convex_hull_stack + convex_hull_stack[:2] # just append the lowest point (origin point ) 
