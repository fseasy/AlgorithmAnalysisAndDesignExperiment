#coding=utf8

from matplotlib import pyplot as plot
from config import MAX_WIDTH , MAX_HEIGHT
from generate_pnts import generate_pnts_in_random
from find_convex_hull_bruteforce import find_convex_hull_bruteforce

def draw_figure(all_pnts , convex_hull_pnts) :
    x_values = [ p.x for p in all_pnts ]
    y_values = [ p.y for p in all_pnts ]
    plot.plot(x_values , y_values , 'ro')
    plot.show()

if __name__ == "__main__" :
    pnt_nums = 4
    pnts = generate_pnts_in_random(pnt_nums , is_static_random=True)
    convex_hull_pnts = find_convex_hull_bruteforce(pnts)
    print convex_hull_pnts
    draw_figure(pnts , convex_hull_pnts)
