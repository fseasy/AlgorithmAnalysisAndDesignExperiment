#coding=utf8

import copy
from state import StateMemoryLess as State

def dfs(vertex , adj_matrix) :
    adj_matrix = copy.copy(adj_matrix) # copy , to avoid change the origin data
    stack = []
    vertex_num = len(vertex)
    # Build Root State
    # just using convex idx 0 for the root 
    cur_vertex_id = 0
    previous_vertex_id = -1 
    visited_state = [False] * vertex_num
    root = State(cur_vertex_id , previous_vertex_id , visited_state)
    stack.append(root)
    while len(stack) > 0 :
        

