#coding=utf8

from matplotlib import pyplot as plot
from config import MAX_WIDTH , MAX_HEIGHT , PNT_NUM_LIST

class PointStat(object) :
    def __init__(self) :
        self.pnts_list = []
        self.bruteforce_convex_hull = []
        self.graham_convex_hull = []
        self.dc_convex_hull = []

    def add_stat_pnts(self , pnts) :
        self.pnts_list.append(pnts)

    def add_stat_bruteforce_convex_hull(self,bf_conhul) :
        self.bruteforce_convex_hull.append(bf_conhul)

    def add_stat_graham_convex_hull(self , graham_conhull) :
        self.graham_convex_hull.append(graham_conhull)

    def add_stat_dc_convex_hull(self , dc_conhull) :
        self.dc_convex_hull.append(dc_conhull)

    def draw_stat(self , config={} ) :

        plot_pnts_list = [ self.bruteforce_convex_hull , self.graham_convex_hull , self.dc_convex_hull ]
        plot_pnts_description = ["brute force" , "graham scan" , "divide conquer"]
        method_num = len(plot_pnts_list)
        pnts_set_num = len(self.pnts_list)
        figure_title = config.get('title' , "Convex Hull Samples in different dataset with different algorithm")
        plot.figure(figure_title)
        plot.suptitle(figure_title , fontsize=16)
        for type_idx , one_type_plot_pnts in enumerate(plot_pnts_list) :
            for pnt_idx , plot_pnts in enumerate(one_type_plot_pnts) : 
                plot.subplot(method_num , pnts_set_num , type_idx  * pnts_set_num + pnt_idx + 1 )
                all_pnts = self.pnts_list[pnt_idx]
                x_values = [ p.x for p in all_pnts ]
                y_values = [ p.y for p in all_pnts ]
                # 绘制所有的散点
                #plot.plot(x_values , y_values , 'ro') # 'o'表示绘制散点图，'r'=> 'red',红色的点
                plot.scatter(x_values , y_values , c='green' , s=[1]) # 使用更加强大的绘制点的函数，c是颜色，
                                                                      # s是点大小缩放，100为原始大小，放小因为点太多了...
                # 绘制凸包的折线
                x_values = [ p.x for p in plot_pnts ]
                y_values = [ p.y for p in plot_pnts ]
                plot.plot(x_values , y_values , 'm' , linewidth=2) # m 品红

                # plot config
                width = config.get('width' , MAX_WIDTH)
                height = config.get('height' , MAX_HEIGHT)
                plot.axis([-10 , width , -10 , height])
                title = "{method_name}-{pnt_size} pnts".format( method_name=plot_pnts_description[type_idx] ,
                                                           pnt_size=len(all_pnts) )
                x_label = config.get('x_label' , 'x-axis')
                y_label = config.get('y_label' , 'y-label')
                plot.title(title)
                plot.xlabel(x_label)
                plot.ylabel(y_label)
        #plot.show() # avoid blocking !

