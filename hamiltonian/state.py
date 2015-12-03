#coding=utf8

import copy

class StateMemoryLess(object) :
    def __init__(self , cur_vertex_id , previous_vertex_id , visited_state_copy) :
        self.cur_vertex_id = cur_vertex_id
        self.previous_vertex_id = previous_vertex_id
        self.visited_state = visited_state_copy # we do the copy out of the struct !
    
    def set_visited(self) :
        self.visited_state[self.cur_vertex_id] = True
        
    def get_visited_state(self) :
        return self.visited_state 

    def get_vertex_id(self) :
        return self.cur_vertex_id 

    def get_extendable_vertex_id(self , adj_matrix) :
        extendable_list = []
        adj_vertex_list = adj_matrix[self.cur_vertex_id]
        for vertex_id in range(len(self.visited_state)) :
            # 1. not parent node
            # 2. adjacent
            # 3. haven't been visited .
            if ( vertex_id != self.previous_vertex_id 
                 and adj_vertex_list[vertex_id] == True 
                 and self.visited_state[vertex_id] == False ) :
                extendable_list.append(vertex_id)
        return extendable_list

    def has_hamiltonian(self , root_idx , adj_matrix):
        # 1. all has been visited !
        # 2. has a way to the root vertex
        is_all_visited = reduce(lambda a , b : a and b , self.visited_state)
        if is_all_visited and adj_matrix[self.cur_vertex_id][root_idx] :
            return True
        else :
            return False
    def init_path_recorder_from_parent(self , parent_node=None) :
        if parent_node == None or hasattr(parent_node , 'path') == False :
            self.path = []
        else :
            self.path  = copy.copy(parent_node.get_path())
    def add_path(self , previous_vertex_id) :
        if hasattr(self , 'path') :
            self.path.append(previous_vertex_id)
    def get_path(self) :
        return self.path if hasattr(self , 'path') else None 

    def __str__(self) :
        out_str = [
        '========%d=======' %self.cur_vertex_id ,
        "previous_vertex_id:%d" %self.previous_vertex_id ,
        "visited state :" ,
        str(self.visited_state) ]
        return "\n".join(out_str)

