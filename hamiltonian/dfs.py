#coding=utf8

import copy

def dfs(vertex , adj_matrix) :
    adj_matrix = copy.copy(adj_matrix) # copy , to avoid change the origin data
    stack = []
    vertex_num = len(vertex)
    

