#coding=utf8

from matplotlib import pyplot as plot
import networkx
import copy
from config import GRAPH_DRAWING_NUM_LIMIT as LIMIT

class GraphStat(object) :
    def __init__(self) :
        self.vertex_list = []
        self.adj_matrix_list = []
        self.bfs_path = []
        self.dfs_path = []
        self.hill_climbing_path = []
        self.branch_and_bound_path = []

    def add_stat_graph(self , vertex , adj_matrix) :
        self.vertex_list.append(copy.copy(vertex))
        self.adj_matrix_list.append(copy.deepcopy(adj_matrix))

    def add_stat_bfs_path(self,bfs_path) :
        self.bfs_path.append(copy.copy(bfs_path))

    def add_stat_dfs_path(self , dfs_path) :
        self.dfs_path.append(dfs_path)

    def add_stat_hill_climbing_path(self , hill_climbing_path) :
        self.hill_climbing_path.append(hill_climbing_path)

    def add_stat_branch_and_bound_path(self , branch_and_bound_path) :
        self.branch_and_bound_path.append(branch_and_bound_path)

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
    def draw_stat(self) :
        
        hamiltom_path_descriptions = ['DFS' , 'BFS' , 'Hill Climbing']
        hamilton_path_list = [self.dfs_path[:LIMIT] , self.bfs[:LIMIT] , self.hill_climbing_path[:LIMIT]]
        graph_vertex_list = self.vertex_list[:LIMIT]
        graph_adj_matrix_list = self.adj_matrix_list[LIMIT]
        for type_idx , one_type_path in enumerate(hamilton_path_list) :
            method_num = len(hamilton_path_list)
            for graph_idx in range(LIMIT) :
                plot.subplot(method_num , LIMIT , type_idx * LIMIT + graph_idx + 1)
                vertex = graph_vertex_list[graph_idx]
                adj_matrix = graph_adj_matrix_list[graph_idx]

                g = networkx.Graph()
                for from_vertex_idx in 



