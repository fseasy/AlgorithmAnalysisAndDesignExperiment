#coding=utf8

def calc_line_params(line_pnt_a , line_pnt_b ) :
    w_1 = -(line_pnt_b.y - line_pnt_a.y)
    w_2 = line_pnt_a.x - line_pnt_b.x
    norm_factor = max(abs(w_1) , abs(w_2))
    w_1 = w_1 / float(norm_factor)
    w_2 = w_2 / float(norm_factor)
    b = - (w_1 * line_pnt_a.x + w_2 * line_pnt_a.y)
    return w_1 , w_2 , b

def is_in_same_side(line_pnt_a , line_pnt_b , test_pnt_a , test_pnt_b) :
    w_1 , w_2 , b = calc_line_params(line_pnt_a , line_pnt_b) 
    y_1 = w_1 * test_pnt_a.x + w_2 * test_pnt_a.y + b
    y_2 = w_1 * test_pnt_b.x + w_2 * test_pnt_b.y + b
    if y_1*y_2 >= 0 : return True 
    else : return False

def find_convex_hull_bruteforce(pnts) :
    pnt_num = len(pnts)
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



