#coding=utf8

import time

class TimeStat(object) :
    def __init__(self) :
        self.pnt_nums = []
        self.bruteforce_time_cost = []
        self.start_time = 0
        self.end_time = 0

    def add_stat_pnt_num(self , pnt_num) :
        self.pnt_nums.append(pnt_num)

    def add_stat_brute_force_timecost(self , t) :
        self.bruteforce_time_cost.append(t)

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
        self.bruteforce_time_cost = []
        self.pnt_nums = []

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
