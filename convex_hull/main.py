#coding=utf8

#from matplotlib import pyplot as plot
from config import MAX_WIDTH , MAX_HEIGHT , PNT_NUM_LIST
from generate_pnts import generate_pnts_in_random
from find_convex_hull_bruteforce import ( find_convex_hull_bruteforce ,
                                          ready_plot_pnts_bruteforce )
from find_convex_hull_grahamscan import ( find_convex_hull_grahamscan ,
                                          ready_plot_pnts_grahamscan
                                         )
from find_convex_hull_dc import ( find_convex_hull_dc )
from time_stat import TimeStat

plot_config = {
    'width' : MAX_WIDTH + 10 ,
    'height' : MAX_HEIGHT + 10 ,
    'title' : 'Convex Hull Brute-Force' ,
    'x_label' : 'x' ,
    'y_label' : 'y'
}



def draw_figure(all_pnts , plot_pnts , config={} ) :
    x_values = [ p.x for p in all_pnts ]
    y_values = [ p.y for p in all_pnts ]
    # 绘制所有的散点
    plot.plot(x_values , y_values , 'ro') # 'o'表示绘制散点图，'r'=> 'red',红色的点
    # 绘制凸包的折线
    x_values = [ p.x for p in plot_pnts ]
    y_values = [ p.y for p in plot_pnts ]
    plot.plot(x_values , y_values , 'b')

    # plot config
    width = config.get('width' , MAX_WIDTH)
    height = config.get('height' , MAX_HEIGHT)
    plot.axis([0 , width , 0 , height])
    title = config.get('title' , '')
    x_label = config.get('x_label' , 'x-axis')
    y_label = config.get('y_label' , 'y-label')
    plot.title(title)
    plot.xlabel(x_label)
    plot.ylabel(y_label)
    plot.show()
def main() :
    timer = TimeStat()
    pnt_nums = PNT_NUM_LIST
    for pnt_num in pnt_nums :
        pnts = generate_pnts_in_random(pnt_num , is_static_random=True)
        
        timer.add_stat_pnt_num(pnt_num)
        timer.start_time_stat()
        
        convex_hull_pnts = find_convex_hull_bruteforce(pnts)
        #print convex_hull_pnts
        plot_pnts = ready_plot_pnts_bruteforce(convex_hull_pnts)
        
        timer.end_time_stat()
        timer.add_stat_brute_force_timecost(timer.get_time_cost())

        #draw_figure(pnts , plot_pnts , plot_config)
    timer.print_time_cost()

if __name__ == "__main__" :
    pnt_num = 100
    
    pnts = generate_pnts_in_random(pnt_num , is_static_random=False)
    #print pnts 
    convex_hull_pnts = find_convex_hull_bruteforce(pnts)
    #sorted_convex_hull_pnts = ready_plot_pnts_bruteforce(convex_hull_pnts)
    #draw_figure(pnts , sorted_convex_hull_pnts , plot_config)
    #print convex_hull_pnts
    convex_hull_pnts_gh = find_convex_hull_grahamscan(pnts)
    #plot_pnts = ready_plot_pnts_grahamscan(convex_hull_pnts_gh)
    #draw_figure(pnts , plot_pnts , plot_config)
    convex_hull_pnts_dc = find_convex_hull_dc(pnts)
    print convex_hull_pnts
    print convex_hull_pnts_gh
    print convex_hull_pnts_dc
    