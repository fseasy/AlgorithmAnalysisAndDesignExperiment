#coding=utf8

import copy


class StateMemLess(object) :
    def __init__(self , cur_vertex_id , previous_vertex_id , visited_state) :
        self.cur_vertex_id = cur_vertex_id
        self.previous_vertex_id = previous_vertex_id
        self.visited_state = visited_state

    def get_extendable_convex_id(self , adj_matrix) :
        extendable_list = []
        adj_convex_list = adj_matrix[self.cur_vertex_id]
        for convex_id in range(len(self.visited_state)) :
            # 1. not parent node
            # 2. adjacent
            # 3. havent been visited .
            if ( convex_id != self.previous_id and adj_convex_list[convex_id] == True 
                 and self.visited_state[convex_id] == False ) :
                extendable_list.append(convex_id)
        return extendable_list

    def has_hamiltonian(self , root_idx ):
        # 1. all has been visited !
        # 2. has a way to the root convex
        is_all_visited = reduce(lambda a , b : a and b , self.visited_state)

