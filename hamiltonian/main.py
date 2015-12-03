#coding=utf8

from generate_random_connected_graph import generate_random_connected_graph
from tools import print_2d_array

from dfs import find_hamiltonian_in_dfs
from bfs import find_hamiltonian_in_bfs 
from hillclimbing import find_hamiltonian_in_hillclimbing

if __name__ == "__main__" :
    vertex , adj_matrix = generate_random_connected_graph(10 , False) 
    print_2d_array(adj_matrix)
    finding_rst = find_hamiltonian_in_dfs(vertex , adj_matrix)
    if finding_rst :
        print "是"
    else :
        print "否"

    finding_rst = find_hamiltonian_in_bfs(vertex , adj_matrix)
    if finding_rst :
        print "是"
    else :
        print "否"

    finding_rst = find_hamiltonian_in_hillclimbing(vertex , adj_matrix)
    if finding_rst :
        print "是"
    else :
        print "否"