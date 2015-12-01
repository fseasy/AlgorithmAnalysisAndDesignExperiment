#coding=utf8

import math

def calc_distance(pnt1 , pnt2) :
    return math.sqrt( (pnt1.x - pnt2.x)**2 + (pnt1.y - pnt2.y)**2 )

def sort_pnts_by_polar_angle_ccw_in_place(origin_pnt , other_pnts) :
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

                        What's more , according to `right hand rule` , if the polar angle of vector p2 is bigger than 
                        p1 , the direction of corss product is to inner(down) , which means a negative number of 
                        `x1y2 - y1x2` , so the sign of `x1y2 - y1x2` can be used to jude which polar angle is bigger
                        for p1 , p2  

                        formally :
                        p1 x p2 =  x1y2 - y1x2 
                        sign(p1 x p2) > 0 : angle of p1 is bigger  , return 1
                        sign(p1 x p2) < 0 : angle of p1 is smaller , return -1 
                        sign(p1 x p2) = 0 : equals 
        if cross result equals to zero , we using the distance to give the compare the point
        '''
        vector_p1 = ( p1.x - origin_pnt.x , p1.y - origin_pnt.y )
        vector_p2 = ( p2.x - origin_pnt.x , p2.y - origin_pnt.y )
        cross_result = vector_p1[0] * vector_p2[1] - vector_p1[1] * vector_p2[0] 
        if corss_result > 0 :
            return 1
        elif corss_result < 0 :
            return -1 
        else :
            return cmp(calc_distance(origin_pnt , p1) , calc_distance(origin_pnt , p2))

    def polar_angle_cmp_func_using_cosine(p1 , p2) :
        '''
        This directly calc the cosine result of vector p1 , p2 (in fact , it should be based on the origin point)
        because cosine is decreasing at the range (0 , PI) , so if cosine(p1 , origin_pnt) if bigger than cosine(p2 , origin_pnt)
        the angle of p1 is less than p2 .

        It may be necessary to normalize the ponit(vector) , as the origin point to the origin_pnt instead of (0,0)
        so , p1 = p1 - origin_pnt 
             p2 = p2 - origin_pnt

        define the 0-degree point (1,0) , the cosine func can be defined like follow :

        cos(p1) = \frac{ p1.x - 1 }{ \sqrt( (p1.x -1 ))^2 + (p1.y - 0 )^2 } 

        formally :

            normalize p1 , p2

            cos(p1) > cos(p2) : angle of p1 is smaller , return -1
            cos(p1) < cos(p2) : angle of p1 is bigger , return 1
            cos(p1) = cos(p2) : equals 

        Like previous , if equals in degree , using distance to sort
        '''
        norm_p1 = (p1.x - origin_pnt.x , p1.y - origin_pnt.y)
        norm_p2 = (p2.x - origin_pnt.x , p2.y - origin_pnt.y)
        calc_cos_to_0_degree = lambda pt : (pt[0] -1) / ( math.sqrt( (pt[0]-1)**2 + pt[1]**2  ) )
        cos_p1 = calc_cos_to_0_degree(norm_p1)
        cos_p2 = calc_cos_to_0_degree(norm_p2)
        if cos_p1 > cos_p2 :
            return -1
        elif cos_p1 < cos_p2 :
            return 1
        else :
            return cmp(calc_distance(origin_pnt , p1 ) , calc_distance(origin_pnt , p2))


def find_convex_hull_graham_scan(pnts) :
    pnt_num = len(pnts)
    if pnt_num < 3 : return []
    convex_stack = []
