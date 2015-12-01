#coding=utf8

def calc_line_params(line_pnt_a , line_pnt_b ) :
    w_1 = -(line_pnt_a.y - line_pnt_b.y)
    w_2 = line_pnt_a.x - line_pnt_b.x
    norm_factor = max(abs(w_1) , abs(w_2))
    w_1 = w_1 / float(norm_factor)
    w_2 = w_2 / float(norm_factor)
    b = - (w_1 * line_pnt_a.x + w_2 * line_pnt_a.y)
    return ( w_1 , w_2 , b )

def is_in_same_side(line_pnt_a , line_pnt_b , test_pnt_a , test_pnt_b) :
    w_1 , w_2 , b = calc_line_params(line_pnt_a , line_pnt_b) 
    y_1 = w_1 * test_pnt_a.x + w_2 * test_pnt_a.y + b
    y_2 = w_1 * test_pnt_b.x + w_2 * test_pnt_b.y + b
    if y_1*y_2 >= 0 : return True 
    else : return False

def find_convex_hull_bruteforce(pnts) :
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
                    if( is_in_same_side(pnt_a , pnt_b , pnt_c , pnt_test) and 
                        is_in_same_side(pnt_a , pnt_c , pnt_b , pnt_test) and 
                        is_in_same_side(pnt_b , pnt_c , pnt_a , pnt_test)) :
                        is_convex_hull[pnt_test_idx] = False
    convex_hull_pnts = []
    for pnt_idx , pnt_is_convex_hull in enumerate(is_convex_hull) :
        if pnt_is_convex_hull :
            convex_hull_pnts.append(pnts[pnt_idx])
    return convex_hull_pnts

def ready_plot_pnts(convex_hull_pnts) :
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




