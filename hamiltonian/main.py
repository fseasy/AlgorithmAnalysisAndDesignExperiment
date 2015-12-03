#coding=utf8

from generate_random_connected_graph import generate_random_connected_graph
from tools import print_2d_array

if __name__ == "__main__" :
    vertex , adj_matrix = generate_random_connected_graph(6) 
    print vertex 
    print_2d_array(adj_matrix)