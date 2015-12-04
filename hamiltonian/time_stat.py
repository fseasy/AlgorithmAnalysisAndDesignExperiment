#coding=utf8

import time
from matplotlib import pyplot as plot

class TimeStat(object) :
    def __init__(self) :
        self.vertex_nums = []
        self.bfs_time_cost = []
        self.dfs_time_cost = []
        self.hillclimbing_time_cost = []
        self.branch_and_bound_time_cost = []
        self.start_time = 0
        self.end_time = 0

    def add_stat_vertex_num(self , vertex_num) :
        self.vertex_nums.append(vertex_num)

    def add_stat_bfs_timecost(self , t) :
        self.bfs_time_cost.append(t)

    def add_stat_dfs_timecost(self , t) :
        self.dfs_time_cost.append(t)

    def add_stat_hillclimbing_timecost(self , t) :
        self.hillclimbing_time_cost.append(t)

    def add_stat_branch_and_bound_timecout(self , t) :
        self.branch_and_bound_time_cost.append(t)

    def start_time_stat(self) :
        self.start_time =  time.time()
        return self.start_time 

    def end_time_stat(self) :
        self.end_time = time.time()
        return self.end_time

    def get_time_cost(self) :
        return self.end_time - self.start_time

    def clear_time_stat(self) :
        self.start_time = 0 
        self.end_time = 0
        self.bfs_time_cost = []
        self.dfs_time_cost = []
        self.hillclimbing_time_cost = []
        self.branch_and_bound_time_cost = []
        self.vertex_nums = []

    def print_time_cost(self) :
        stat_cnt = len(self.pnt_nums)
        header_line = " ".join([ "{method_name:20}" ] + [ "| {pnt_nums_str[%d]:20}" %i for i in range(stat_cnt) ])
        formated_line = " ".join([ "{left_header:20}" ] + [ "| {time_cost[%d]:20.2f}" %i for i in range(stat_cnt) ])
        method_name = "method-name"
        pnt_nums_str = ["pnt-nums=%d" %(d) for d in self.pnt_nums ]
        print header_line.format(**locals())
        left_header = "brute-force"
        time_cost = self.bruteforce_time_cost
        print formated_line.format(**locals())

        left_header = "graham scan"
        time_cost = self.grahamscan_time_cost
        print formated_line.format(**locals())

        left_header = "divide conquer"
        time_cost = self.dc_time_cost
        print formated_line.format(**locals())

    def draw_stat(self) :
        ## Figure 1 . time cost about 3 methods finding a hamiltonian in different vertex size 
        figure_1_title = "Time Cost Statistics in different vertex size with different algorithm"
        plot.figure(figure_1_title)  
        plot.suptitle(figure_1_title , fontsize=16)

        # x-axis is the pnt-nums
        x_values = self.vertex_nums 

        # y-aixs is the time cost of different algorithm
        plot.plot(x_values , self.dfs_time_cost , 'mo-' , label="DFS")
        plot.plot(x_values , self.bfs_time_cost , 'gx-' , label="BFS")
        plot.plot(x_values , self.hillclimbing_time_cost , 'k+-' , 
                                                 label="HillClimbing")

        x_label = 'Vertex Size'
        y_label = 'Time Cost / (secondes)'
        plot.xlabel(x_label)
        plot.ylabel(y_label)
        plot.legend()
    
    ## Figure 2 : Time cost about using branch and bound in different vertex size
        figure_2_title = "Time Cost Statistics using Branch and Bound in different vertex size"
        plot.figure(figure_2_title)  
        plot.suptitle(figure_2_title , fontsize=16)

        plot.plot(x_values , self.branch_and_bound_time_cost , 'mo-' , 
                                                label="Branch and Bound")
        x_label = 'Vertex Size'
        y_label = 'Time Cost / (secondes)'
        plot.xlabel(x_label)
        plot.ylabel(y_label)
        plot.legend()
