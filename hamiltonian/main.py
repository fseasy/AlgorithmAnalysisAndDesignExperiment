#coding=utf8

import sys
import logging
from matplotlib import pyplot as plot
from generate_random_connected_graph import ( generate_random_connected_graph ,
                                              generate_random_weighted_complete_graph )
from tools import print_2d_array

from dfs import find_hamiltonian_in_dfs
from bfs import find_hamiltonian_in_bfs 
from hillclimbing import find_hamiltonian_in_hillclimbing
from branch_and_bound import find_min_hamiltonian_in_branch_and_bound

from config import VERTEX_NUM_LIST

from graph_stat import GraphStat
from time_stat import TimeStat 

logging.basicConfig(level=logging.INFO)

def print_path_in_console(path) :
    if path is None :
        print >> sys.stderr , "No hamiltonian "
    else :
        print >> sys.stderr , "\n%s\n" %(" -> ".join(map(str , path)))
        
def main() :
    graph_stater = GraphStat()
    timer = TimeStat()
    for vertex_num in VERTEX_NUM_LIST :
        
        logging.info('random generate connected graph  ( vertex %d)' % vertex_num)
        vertex , adj_matrix = generate_random_connected_graph(vertex_num , False) 
        logging.info('generate graph done .')

        graph_stater.add_stat_graph(vertex , adj_matrix)
        timer.add_stat_vertex_num(vertex_num)

        # dfs
        logging.info('using dfs to find hamiltonian')
        timer.start_time_stat()
        
        hamiltonian_path_in_dfs = find_hamiltonian_in_dfs(vertex , adj_matrix , timer)
        
        timer.end_time_stat()
        timer.add_stat_dfs_timecost(timer.get_time_cost())
        graph_stater.add_stat_dfs_path(hamiltonian_path_in_dfs)
        logging.info('dfs done .')
        print_path_in_console(hamiltonian_path_in_dfs) 

        # bfs
        logging.info('using bfs to find hamiltonian')
        timer.start_time_stat()
        
        hamiltonian_path_in_bfs = find_hamiltonian_in_bfs(vertex , adj_matrix , timer)
        
        timer.end_time_stat()
        timer.add_stat_bfs_timecost(timer.get_time_cost())
        graph_stater.add_stat_bfs_path(hamiltonian_path_in_bfs)
        logging.info('bfs done .')
        print_path_in_console(hamiltonian_path_in_bfs) 

        #hill climbing 
        logging.info('using hillclimbing to find hamiltonian')
        timer.start_time_stat()
        
        hamiltonian_path_in_hillclimbing = find_hamiltonian_in_hillclimbing(vertex , adj_matrix , timer)

        timer.end_time_stat()
        timer.add_stat_hillclimbing_timecost(timer.get_time_cost())
        graph_stater.add_stat_hill_climbing_path(hamiltonian_path_in_hillclimbing)
        logging.info('hillclimbing done .')
        print_path_in_console(hamiltonian_path_in_hillclimbing)
        
        # Min Hamiltonian
        # it is different from previous 
        logging.info('generate a complete random weighted graph')
        vertex , cost_matrix = generate_random_weighted_complete_graph(vertex_num,False)
        logging.info('done .')
        logging.info('using branch and bound to find minimum halmiltonian')
        graph_stater.add_stat_complete_graph(vertex , cost_matrix)
        timer.start_time_stat()

        min_hamiltonian = find_min_hamiltonian_in_branch_and_bound(vertex , cost_matrix)

        timer.end_time_stat()
        timer.add_stat_branch_and_bound_timecout(timer.get_time_cost())
        graph_stater.add_stat_branch_and_bound_path(min_hamiltonian)
        print_path_in_console(min_hamiltonian)
        logging.info('branch and bound done .')

    graph_stater.draw_stat()
    timer.print_time_cost()
    timer.draw_stat()
    plot.show()






if __name__ == "__main__" :
    main()
    