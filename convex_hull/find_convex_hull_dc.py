#coding=utf8

from find_convex_hull_grahamscan import ( sort_pnts_by_polar_angle_ccw ,
                                          get_polar_angle_cmp_function ,
                                          find_convex_hull_grahamscan ,
                                          ready_plot_pnts_grahamscan )
from tools import ( randomized_select ,
                    get_min_and_max_value_and_index )
from point import Point 

def generate_inner_pnt(convex_hull_pnts) :
    assert(len(convex_hull_pnts) >= 3)
    # According to the Convex Hull attribute , any point in the convex hull can be represented by 
    # inner_p = alpha * con_hull_pnt_1 + beta * con_hull_pnt_2 + eta * con_hull_pnt_3 , and 
    # alpha + beta + eta = 1
    # because 3 convex points 's area must be in the total convex hull . a linear combination keep the 
    # point in the area 
    # 中文描述： 一个凸包的内点，可以用三个凸包顶点的线性组合来表示。或者，任意3个凸包顶点的线性组合，可以生成一个内点。
    # reference : https://zh.wikipedia.org/wiki/%E5%87%B8%E5%8C%85
    
    # set alpha , beta , eta , and select 3 point .
    alpha = 0.5
    beta = 0.2
    eta = 0.3
    # using this point to make inner pnt more centerd !
    pnt_1 = convex_hull_pnts[0]
    pnt_2 = convex_hull_pnts[len(convex_hull_pnts)/2]
    pnt_3 = convex_hull_pnts[-1]
    return ( pnt_1 * alpha + pnt_2 * beta + pnt_3 * eta )

def merge_sub_convex_hull_pnts(sub_pnts_1 , sub_pnts_2 , origin_pnt) :
    size_1 = len(sub_pnts_1)
    size_2 = len(sub_pnts_2)
    idx_1 = 0 
    idx_2 = 0
    merge_rst = []
    cmp_func = get_polar_angle_cmp_function(origin_pnt)
    while idx_1 < size_1 and idx_2 < size_2 :
        if cmp_func(sub_pnts_1[idx_1] , sub_pnts_2[idx_2]) < 0 :
            merge_rst.append(sub_pnts_1[idx_1])
            idx_1 += 1
        else : 
            merge_rst.append(sub_pnts_2[idx_2])
            idx_2 += 1
    while idx_1 < size_1 :
        merge_rst.append(sub_pnts_1[idx_1])
        idx_1 += 1
    while idx_2 < size_2 :
        merge_rst.append(sub_pnts_2[idx_2])
        idx_2 += 1
    return merge_rst

def find_convex_hull_dc(pnts) :
    pnt_num = len(pnts)
    if pnt_num <= 3 :
        # the function `sort_pnts_by_polar_angle_ccw` is a O(n lgn) , but because the pnts is just less than 4 , so
        # time costing is O(1) !!
        return sort_pnts_by_polar_angle_ccw(Point(0,0) , pnts) # using (0,0) to as the origin point(polar point)
    ## DIVIDE

    # to find a x=m line to binary partition all the points ! 
    # using randomized_select , O(n)
    pnt_to_partition =  randomized_select(pnts , pnt_num / 2 + 1 , key=lambda p : p.x )
    left_part_pnts = [pnt for pnt in pnts if pnt.x <= pnt_to_partition.x ] # hence , pnt_to_partition is included in left part
    right_part_pnts = [pnt for pnt in pnts if pnt.x > pnt_to_partition.x ]
    ## BIG BUG !!
    # 考虑特殊情况：
    #   1. 当pnt_to_partition中的横坐标全部相同时，左边的集合将始终不变！！这将导致无穷递归！！
    #   2. 当pnt_to_partition是其中横坐标最大的点！此时，同样将造成左边集合不变。
    #   最终爆栈！！
    # ！！如果将left_part_pnts的条件改为 < ， 而right_part_pnt改为 >= ， 情况2是否就好了？
    #     不是，因为这会在pnt_to_partition为横坐标最小的点时造成右边集合不变。所以这不是问题的关键！
    # 所以，首先需要特别检测一下，pnt_to_partition 的大小 以及 原始的点集 pnts的大小！
    # 如果没有改变，则说明遇到特殊情况，不能再递归！！（否则爆栈！）
    # 这时，有必要分开讨论这两种情况！
    # 1. 横坐标全部相同
    #   必然有 ===> y值最大和最小点为为该点集下的凸包！！
    #   故 直接返回y-min的最大点和最小点。（按照逆时针排序，应该先最小，再最大！）
    # 2. 选择的中位数横坐标是横坐标的最大值
    #   可以入上面思考中那样，将left_part_pnts改为 < ， 将right_part_ptn 改为 >= 
    if len(left_part_pnts) == len(pnts) : 
        #print pnts
        x = pnts[0].x
        is_x_all_same = True
        for pnt in pnts[1:] :
            if x != pnt.x :
                is_x_all_same = False
                break
        if is_x_all_same :
            min_y_pnt = min(pnts , key=lambda p : p.y )
            max_y_pnt = max(pnts , key=lambda p : p.y )
            return [min_y_pnt , max_y_pnt]
        else :
            left_part_pnts =  [pnt for pnt in pnts if pnt.x < pnt_to_partition.x ]
            right_part_pnts = [pnt for pnt in pnts if pnt.x >= pnt_to_partition.x ]


    ## CONQUER
    left_part_convex_hull_pnts = find_convex_hull_dc(left_part_pnts)
    right_part_convex_hull_pnts = find_convex_hull_dc(right_part_pnts)
    
    ## MERGE

    # first , split all the covex hull points to 3 points sequence , every one has a order of `increasing of polar angle`
    # 为了说得更加明白，这里使用中文论述：
    # 左部分的凸包点、和右部分的凸包点，可以看做是各自是相对于自己的极点按照逆时针排序的。
    # 我们现在想要利用这种本身的有序性，使其在 共同的极点 下按照逆时针排序！
    # 按照PPT的内容，我们将共同的极点选作左边凸包的内点！
    # 这样，相对于该极点，左边的凸包肯定是按逆时针有序的了。但是右边的点却不是这样！
    # 我们将右边的凸包点分为两个部分，保证这两个部分内部是逆时针排序的！
    # 具体做法是，找到右边凸包中以左极点为原点极角最大和最小的点,记为 R_max , R_min 
    # 以此两点为界，可以将右凸包分为两个部分 ——> 逆时针 R_min -> R_min ，且包含此两点；
    #                                           顺时针， R_min -> R_max , 不包含此两点。
    # 由于右边的凸包已经是相对于自身极点逆时针排序的，所以上述分割是O(n)的。

    # 此外，还有特别的情况——
    # 当左边不够3个时，就没有内点！ 此时我们以右边凸包的内点为准点。（此时，我们可以保证右边凸包必然至少3个顶点）
    # 以右边凸包内点为极点，则只需将左边的原来相对于自身极点逆时针的凸包点逆序，即能保证其相对于右边极点是逆时针有序的。
    # 这个可以通过右手定则直观的得到。

    # 以上，就定义了对左右凸包点的划分逻辑。
    # 我们定义 sub_convex_hull_1 , sub_convex_hull_2 , sub_convex_hull_3来表示3个序列。
    # 这样可使代码更加简洁。但是逻辑可能梢混乱，所以以此作为说明。

    if len(left_part_convex_hull_pnts) < 3 :
        if len(right_part_convex_hull_pnts) < 3 :
            # 此情况下，左右都只有少于3个点。
            # 这时，可以以（0，0）为极点，左右凸包相对原点都是逆时针的！
            polar_pnt = Point(0,0)
            sub_convex_hull_1 = left_part_convex_hull_pnts
            sub_convex_hull_2 = right_part_convex_hull_pnts
            sub_convex_hull_3 = []
        else :
            polar_pnt = generate_inner_pnt(right_part_convex_hull_pnts)
            # right 
            sub_convex_hull_1 = right_part_convex_hull_pnts
            # left
            sub_convex_hull_2 = left_part_convex_hull_pnts
            sub_convex_hull_2.reverse()
            # just for the program struct
            sub_convex_hull_3 = []
    else :
        polar_pnt = generate_inner_pnt(left_part_convex_hull_pnts)
        # left 
        sub_convex_hull_1 = left_part_convex_hull_pnts
        ## part right convex hull
        # first , find the min and max polar angle point according to the polar_pnt
        if len(right_part_convex_hull_pnts) < 3 :
            # when right part convex hull just has less than 3 points , the are CCW according to the
            # left polar point 
            sub_convex_hull_2 = right_part_convex_hull_pnts
            sub_convex_hull_3 = []
        else :
            angle_min_pnt , angle_max_pnt , angle_min_pnt_idx , angle_max_pnt_idx  = ( 
                                          get_min_and_max_value_and_index(right_part_convex_hull_pnts) )
            # right 1 , right 2
            if angle_max_pnt_idx > angle_min_pnt_idx :
                sub_convex_hull_2 = right_part_convex_hull_pnts[angle_min_pnt_idx : angle_max_pnt_idx + 1]
                sub_convex_hull_3 = ( right_part_convex_hull_pnts[angle_max_pnt_idx + 1 :] + 
                                      right_part_convex_hull_pnts[0 : angle_min_pnt_idx] )
                sub_convex_hull_3.reverse()
            else :
                sub_convex_hull_2 = ( right_part_convex_hull_pnts[angle_min_pnt_idx :] + 
                                      right_part_convex_hull_pnts[:angle_max_pnt_idx +1 ] )
                sub_convex_hull_3 = right_part_convex_hull_pnts[angle_max_pnt_idx + 1 : angle_min_pnt_idx]
                sub_convex_hull_3.reverse()
    # merge convex hull points
    merge_rst = merge_sub_convex_hull_pnts(sub_convex_hull_1 , sub_convex_hull_2 , polar_pnt)
    merge_rst = merge_sub_convex_hull_pnts(merge_rst , sub_convex_hull_3 , polar_pnt)
    #print merge_rst
    #exit(1)
    return find_convex_hull_grahamscan(merge_rst)


def ready_plot_pnts_dc(dc_convex_hull_pnts) :
    '''
    Just use graham scan result !
    '''
    return ready_plot_pnts_grahamscan(dc_convex_hull_pnts)