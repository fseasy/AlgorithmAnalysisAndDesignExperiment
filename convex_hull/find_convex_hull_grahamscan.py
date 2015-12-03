#coding=utf8

import math
from config import EPSILON
from tools import ( is_float_num_equal ,
                    calc_distance )

def get_polar_angle_cmp_function(origin_pnt , cmp_func_using_cosine=False) :
    '''
    define the compare function for sort by polar angle
    '''
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
    if cmp_func_using_cosine :
        return polar_angle_cmp_func_using_cosine
    else :
        return polar_angle_cmp_func_using_cross_product


def sort_pnts_by_polar_angle_ccw(origin_pnt , other_pnts , cmp_func_using_cosine=False) :
    other_pnts = other_pnts[:] # make a copy to avoid change the origin data !
    
    # sort 
    cmp_func = get_polar_angle_cmp_function(origin_pnt , cmp_func_using_cosine)
    sorted_pnts = sorted(other_pnts , cmp=cmp_func)
    return sorted_pnts


def init_convex_hull_stack_with_3_convex_hull( sorted_pnts , empty_convex_hull_stack , polar_point) :
    '''
    init convex hull stack 
    param : empty_convex_hull_stack [in|out] , it is Empty , polar point is not added yet 
            polar_point [in] , polar point 
            sorted_pnts [in] , sorted points in polar angle 
    Return : init_state , next_finding_idx -> ( True|False , int )
    '''
    # 先找到与极点y值不相同的点！
    idx = 0
    pnt_num = len(sorted_pnts)
    while(idx < pnt_num) :
        if sorted_pnts[idx].y != polar_point.y :
            break
        idx += 1
    else :
        return False , 0 # 即，所有点都是与极点y值相同！！此时没有凸包，初始失败！
    # 有两种情况——
    # 1. 这两个点之间没有其他点! 即没有平行于极轴的边，那么加入此点，然后再只需要再加入后继的一个点即可。肯定构成凸包。
    # 2. 这两个点中包含至少一个与极点y值相同的点，那么我们只需要将最后一个（x值最大）的点，以及该点加入到栈中，就完成了任务！
    # 通过判断idx的大小来检测！
    if idx > 0 :
        # 对应情况2！
        empty_convex_hull_stack.append(polar_point)
        empty_convex_hull_stack.append(sorted_pnts[idx-1])
        empty_convex_hull_stack.append(sorted_pnts[idx])
        return True , idx+1
    else :
        # 对应情况1
        if pnt_num < 2 :
            return False , 0
        empty_convex_hull_stack.append(polar_point)
        empty_convex_hull_stack.append(sorted_pnts[0])
        empty_convex_hull_stack.append(sorted_pnts[1])
        return True , 2 

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
    ## !! we change this follow init code !
    ##convex_hull_stack.append(lowest_pnt)
    ##convex_hull_stack.append(sorted_pnts[0])
    ##convex_hull_stack.append(sorted_pnts[1])
    
    init_state , next_finding_idx = init_convex_hull_stack_with_3_convex_hull( sorted_pnts , convex_hull_stack ,
                                                                               lowest_pnt)
    if not init_state : return [] # init failed , no convex hull
    # circle
    for p_idx , test_pnt in enumerate(sorted_pnts[next_finding_idx:]) :
        while True :
            try :
                stack_top_pnt = convex_hull_stack[-1]
                stack_undertop_pnt = convex_hull_stack[-2]
            except :
                print lowest_pnt
                print convex_hull_stack
                print sorted_pnts[:p_idx+2]
                exit(1)

            vector_undertop2top = (stack_top_pnt.x - stack_undertop_pnt.x , stack_top_pnt.y - stack_undertop_pnt.y)
            vector_top2test = (test_pnt.x - stack_top_pnt.x , test_pnt.y - stack_top_pnt.y)
            # using cross product to distinguish wheather 'TO LEFT' 
            # if 'TO LEFT' , vector_undertop2top x vector_top2test > 0 ! 
            # if < 0 , then 'TO RIGHT' , pop stack top and continue ~ 
            # if = 0 ? As written in PPT , we think it is also not the convex hull !
            #          But it may cause ERROR !
            #          使用中文来说明存在的问题：
            #          PPT中说“非左转点”都不算凸包，所以如果待测点与栈顶、次栈顶在一条直线上（即两个向量极角相同），
            #          则待测点不是凸包上的点。
            #          这时，就有了一个问题——如果与我们初始化有相同y值，且x大于该初始点的个数大于等于2，那么则些点
            #          的极角是0 ， 所以上面初始化时就出现了错误！ 因为加入的三个点不构成凸包！即违反了 循环不变量 的初始条件！
            #          解决办法——两种 
            #          1. 维持此规则，但是找基准点时，使得该点不仅y值最小，且x值最大，那么加入的点必然是凸包！
            #          2. 修改此规则，将`左转点`以及'待测点与栈顶、次栈顶元素在一条直线'上均作为是凸包的规则
            #          权衡利弊，还是按照PPT的要求来修改！所以需要修改上述找起始点（极点）的规则！
            #          我想这样更加满足凸包的定义吧。凸包毕竟还是是极点（此极点非极坐标系中的极点，而是凸多边形中的极点 - -），
            #          两个极点连线之间的点，虽然在凸包的边上，但是不是极点了。
            #
            #          此外，还需要注意！ 如果上述情况确实存在，即多个点在与极点y值相同，那么根据 gramham scan 的处理流程，
            #          最后一个点必然也是与极点的y值相同，且此点在极轴上离极点最近。
            #          根据上述规则，我们应该将该点去掉！ 因为在上述规则下它不是凸包点！
            #          上述操作在最后判断！
            #
            #update :  上述想法又有问题！！！
            #          按照想法1的规则，上面的极点是没有问题的，可是考虑——如果极点上方又有超过
            #          两个与此点x坐标相同的点——那么初始加入的三个点又不是凸包！！！
            #          我觉得有必要放弃上述想法，完整的写一个初始栈中三个顶点的算法！！！
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
