#coding=utf8

from state import State
from tools import print_2d_array
from config import INF

def find_min_hamiltonian_in_branch_and_bound(vertex , cost_matrix) :
    vertex_num = len(vertex)
    # to record the result 
    global_low_bound = INF
    cor_hamiltonian = None
    # init root state
    root_vertex_id = 0 
    out_mask = [ False ] * vertex_num
    in_mask = [ False ] * vertex_num
    low_bound = 0
    path_pair = [ -1 ] * vertex_num
    root = State(cost_matrix , low_bound , in_mask , out_mask,path_pair)
    root.normalize_cost_matrix_and_update_low_bound()
    stack = [ root ]

    while len(stack) > 0 :

        # visit current element 
        cur_graph = stack.pop()
        # check graph state
        graph_state = cur_graph.check_graph_state()
        if graph_state == -1 :
            # has local circle ! abandon
            continue
        elif graph_state == 1 :
            # has hamiltonian 
            # check low bound 
            cur_graph_cost = cur_graph.get_low_bound()
            #print "FIND !!"
            #print cur_graph_cost
            if cur_graph_cost < global_low_bound :
                global_low_bound = cur_graph_cost
                cor_hamiltonian = cur_graph.get_path()
                #print "UPDATE GLOBAL GRAPH LOW BOUND"
            continue # here , using continue , because i do not want to indent in the next part !
        # else , it is normal state , should be extend continues .
        ## divide the sub space
        # calc f(i,j) and find the (i,j)
        edge = cur_graph.select_one_edge_to_minimize_left_subtree_and_maximum_right_subtrue()
        
        if edge is None : continue 
        #print_2d_array(cur_graph.get_cost_matrix())
        #print "select row and col "
        #print edge
        
        # init left_tree , right_tree
        cost_matrix = cur_graph.get_cost_matrix()
        low_bound = cur_graph.get_low_bound()
        in_mask = cur_graph.get_in_mask()
        out_mask = cur_graph.get_out_mask()
        path_pair = cur_graph.get_path_pair()
        left_tree = State(cost_matrix,low_bound,in_mask,out_mask,path_pair)
        right_tree = State(cost_matrix,low_bound,in_mask,out_mask,path_pair)
        
        #print "--left tree matrix--"
        #print_2d_array(left_tree.get_cost_matrix())
        #print "--right tree matrix--"
        #print_2d_array(right_tree.get_cost_matrix())

        # build the left tree
        left_tree.add_new_mask(edge[0] , edge[1]) # delete row i , col j
        left_tree.disable_edge(edge[1] , edge[0]) # set cost_matrix[j][i] = INF
        left_tree.normalize_cost_matrix_and_update_low_bound() # normalize 
        left_tree.add_path_pair(edge[0],edge[1])
        # build the right tree
        right_tree.disable_edge(edge[0] , edge[1]) # set cost_matrix[i][j] = INF
        right_tree.normalize_cost_matrix_and_update_low_bound_row(edge[0]) # only update the row i
        right_tree.normalize_cost_matrix_and_update_low_bound_col(edge[1]) # only update the col j
        # according to the current global low boud , decide wheather push sub trees stack 
        # if push , left tree should on the top
        if right_tree.get_low_bound() < global_low_bound :
            stack.append(right_tree)
        if left_tree.get_low_bound() < global_low_bound :
            stack.append(left_tree)
        
        # print "\n\n====left tree matrix===="
        # print_2d_array(left_tree.get_cost_matrix())
        # print left_tree.get_path_pair() 
        # print "====right tree matrix===="
        # print_2d_array(right_tree.get_cost_matrix())

    #print global_low_bound
    #print cor_hamiltonian
    return cor_hamiltonian
