#coding=utf8

STATIC_RANDOM_SEED = 1314

VERTEX_NUM_LIST = [8,10,12,14,16,18,20]
VERTEX_NUM_LIST = [8,10,12,14,16] # because the limit of PC , 18 and 20 vertex can't be processing easily in BFS 
                                  # so I have to abandon it !
GENERATE_EDGE_PROBABILITY_THRESHOLD = 0.8 # Also for the limit of PC . make it big to avoid huge memory allocation in BFS

MAX_WEIGHT = 10
MIN_WEIGHT = 1
INF = float('inf')

GRAPH_DRAWING_NUM_LIMIT = 3