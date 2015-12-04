#coding=utf8

import random
import time 
from config import ( GENERATE_EDGE_PROBABILITY_THRESHOLD as THRESHOLD ,
                     STATIC_RANDOM_SEED , 
                     MAX_WEIGHT , MIN_WEIGHT , INF )

def generate_random_connected_graph(vertex_num , is_static_random=True) :
    if is_static_random : random.seed(STATIC_RANDOM_SEED)
    else : random.seed(time.time())
    vertex = [i for i in range(vertex_num)] # using 0, 1 , 2 .. vertex_num-1 as the vertex name
    # random generate the edge !
    # Just to generate a adjancent matrix to stand for the edge
    # what's more , for an Undirected Connected Graph , some rule should be contented !
    # 1. the adjacent matrix must be a symmetric matrix(对称矩阵) , that is , A_{ij} = A_{ji}
    # 2. no edge to the node self . so diangle element is zero
    # we build the up rectangle ajdacent matrix , and at last to build the full adjacent matrix 
    adj_matrix = [ [False] * vertex_num for i in range(vertex_num) ]
    for from_node in range(vertex_num - 1) :
        for to_node in range(from_node + 1 , vertex_num) :
            adj_matrix[from_node][to_node] = ( random.random() > THRESHOLD )

    # to avoid there is no connected path , we build a random path !
    node = vertex[:]
    random.shuffle(node)
    for i in range(len(node)-1) :
        from_node = min(node[i] , node[i+1])
        to_node = max(node[i] , node[i+1])
        adj_matrix[from_node][to_node] = True

    # build the full adjacent matrix , to let it be a symmetric matrix
    for i in range(vertex_num - 1) :
        for j in range(i+1 , vertex_num) :
            adj_matrix[j][i] = adj_matrix[i][j]
    return (vertex , adj_matrix)

def generate_random_weighted_complete_graph(vertex_num , is_static_random) :
    if is_static_random : random.seed(STATIC_RANDOM_SEED)
    else : random.seed(time.time())
    vertex = [ i for i in range(vertex_num)] # also use 0 , 1 , 2 to stand for the vertex name
    # It is also a Undirected graph , so it is a symmetrix matrix
    # init up triangle matrix , and copy A_{ij} to A_{ji}
    cost_matrix = [ [ INF ] * vertex_num for i in range(vertex_num) ]
    for i in range(vertex_num-1) :
        for j in range(i+1 , vertex_num) :
            cost_matrix[i][j] = random.randint(MIN_WEIGHT , MAX_WEIGHT) # including the MAX_WEIGHT
            cost_matrix[j][i] = cost_matrix[i][j]
    return vertex , cost_matrix

