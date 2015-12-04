#coding=utf8

from generate_random_connected_graph import ( generate_random_connected_graph ,
                                              generate_random_weighted_complete_graph )
from tools import print_2d_array

from dfs import find_hamiltonian_in_dfs
from bfs import find_hamiltonian_in_bfs 
from hillclimbing import find_hamiltonian_in_hillclimbing
from branch_and_bound import find_min_hamiltonian_in_branch_and_bound

if __name__ == "__main__" :
    # vertex , adj_matrix = generate_random_connected_graph(16 , False) 
    # print_2d_array(adj_matrix)
    # finding_rst = find_hamiltonian_in_dfs(vertex , adj_matrix)
    # if finding_rst :
    #     print "是"
    # else :
    #     print "否"

    # finding_rst = find_hamiltonian_in_bfs(vertex , adj_matrix)
    # if finding_rst :
    #     print "YES"
    # else :
    #     print "NO"

    # finding_rst = find_hamiltonian_in_hillclimbing(vertex , adj_matrix)
    # if finding_rst :
    #     print "是"
    # else :
    #     print "否"
    vertex , cost_matrix = generate_random_weighted_complete_graph(16,True)
    print_2d_array(cost_matrix,4)
    find_min_hamiltonian_in_branch_and_bound(vertex , cost_matrix)