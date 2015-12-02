#coding=utf8

from matplotlib import pyplot as plot

plot_config = {
    'width' : MAX_WIDTH + 10 ,
    'height' : MAX_HEIGHT + 10 ,
    'title' : 'Convex Hull Brute-Force' ,
    'x_label' : 'x' ,
    'y_label' : 'y'
}

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





    def draw_figure(self , config={} ) :

        plot_pnts_list = [ self.bruteforce_convex_hull , slef.graham_convex_hull , self.dc_convex_hull ]
        for type_idx , plot_pnts in enumerate(plot_pnts_list) :
            for pnt_idx , 
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

