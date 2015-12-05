#coding=utf8

import logging
from matplotlib import pyplot as plot
from config import ( MAX_WIDTH , MAX_HEIGHT , PNT_NUM_LIST , 
                     convex_hull_pnt_plot_config )
from generate_pnts import generate_pnts_in_random
from find_convex_hull_bruteforce import ( find_convex_hull_bruteforce ,
                                          ready_plot_pnts_bruteforce )
from find_convex_hull_grahamscan import ( find_convex_hull_grahamscan ,
                                          ready_plot_pnts_grahamscan
                                         )
from find_convex_hull_dc import ( find_convex_hull_dc ,
                                  ready_plot_pnts_dc )
from time_stat import TimeStat
from point_stat import PointStat

logging.basicConfig(level=logging.INFO)


def main() :
    timer = TimeStat()
    pntStater = PointStat()
    pnt_nums = PNT_NUM_LIST
    logging_format = "{method_name}-{pnt_num} done ."
    for pnt_num in pnt_nums :
        pnts = generate_pnts_in_random(pnt_num , is_static_random=False)
        pntStater.add_stat_pnts(pnts)
        timer.add_stat_pnt_num(pnt_num)

        # brute force 
        method_name = "brute force"
        timer.start_time_stat()
        convex_hull_pnts = find_convex_hull_bruteforce(pnts)
        #print convex_hull_pnts
        plot_pnts = ready_plot_pnts_bruteforce(convex_hull_pnts)
        timer.end_time_stat()
        timer.add_stat_brute_force_timecost(timer.get_time_cost())
        pntStater.add_stat_bruteforce_convex_hull(plot_pnts)
        logging.info(logging_format.format(**locals()) )

        # graham scan
        method_name = "gramham scan"
        timer.start_time_stat()
        convex_hull_pnts = find_convex_hull_grahamscan(pnts)
        plot_pnts = ready_plot_pnts_grahamscan(convex_hull_pnts)
        timer.end_time_stat()
        timer.add_stat_graham_scan_timecost(timer.get_time_cost())
        pntStater.add_stat_graham_convex_hull(plot_pnts)
        logging.info(logging_format.format(**locals()) )

        # divide conquer
        method_name = "divide conquer"
        timer.start_time_stat()
        convex_hull_pnts = find_convex_hull_dc(pnts)
        plot_pnts = ready_plot_pnts_dc(convex_hull_pnts)
        timer.end_time_stat()
        timer.add_stat_dc_timecost(timer.get_time_cost())
        pntStater.add_stat_dc_convex_hull(plot_pnts)
        logging.info(logging_format.format(**locals()) )

    timer.print_time_cost()
    pntStater.draw_stat(convex_hull_pnt_plot_config)
    timer.draw_stat()
    plot.show()

if __name__ == "__main__" :
    main() 
    