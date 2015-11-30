#coding=utf8

def calc_line_params(line_pnt_a , line_pnt_b ) :
    

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



