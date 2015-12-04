#coding=utf8

import copy
from config import INF

class StateMemoryLess(object) :
    '''
    If no need to record adjacent matrix , this class is optimized !
    Else , using Stae below .
    '''
    def __init__(self , cur_vertex_id , previous_vertex_id , visited_state_copy , path_copy) :
        self.cur_vertex_id = cur_vertex_id
        self.previous_vertex_id = previous_vertex_id
        self.visited_state = visited_state_copy # we do the copy out of the struct !
        self.path = path_copy

    
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

    def add_path(self , vertex_id) :
        self.path.append(vertex_id)

    def get_path(self) :
        return self.path

    def __str__(self) :
        out_str = [
        '========%d=======' %self.cur_vertex_id ,
        "previous_vertex_id:%d" %self.previous_vertex_id ,
        "visited state :" ,
        str(self.visited_state) ]
        return "\n".join(out_str)


class State(object) :
    def __init__(self , cost_matrix , init_low_bound , init_in_mask , init_out_mask , path_pair) :
        ## mask : using this to do the operation Delete the row and col from the cost_matrix
        ## 使用中文来说明：
        ## 在PPT上，如果扩展左子树，就需要将对应i行j列从cost_matrix中删去，然而这在代码实现时代价大 ——
        ## 主要是使操作更加复杂（需要索引删除后节点和矩阵的下标对应关系，复制更加麻烦。然而空间代价的确是优化的！）
        ## 这里就简单的使用一个True、False的mask列表，来标识行列的删除情况。
        ## 如果被删，则mask对应位置的值为True ！ 否则为False ！
        ## 使用Mask后删除更加简单，不过查找有效扩展点时更加复杂了，需要谨慎处理！

        ## 对于减去的行列值的理解：
        ## 每行减去的值，认为是从这个行索引对应的顶点出去需要的最小代价，定义为出度(out)代价，这里out_mask对应行是否被删除。
        ## 对每列减去的值，认为是到达该列索引对应的最小代价，定义为入度(in)代价，这里用in_mask对应列是否被删除。
        self.low_bound = init_low_bound
        self.cost_matrix = copy.deepcopy(cost_matrix) # using copy !
        self.in_mask = copy.copy(init_in_mask)
        self.out_mask = copy.copy(init_out_mask)
        self.vertex_num = len(self.cost_matrix)
        self.path_pair = copy.copy(path_pair)
    
    def get_low_bound(self) :
        return self.low_bound 
    def get_cost_matrix(self) :
        return self.cost_matrix 
    def get_in_mask(self) :
        return self.in_mask
    def get_out_mask(self) :
        return self.out_mask
    def get_path_pair(self) :
        return self.path_pair
    def get_deleted_cost_matrix(self) :
        rst = []
        for row in range(self.vertex_num) :
            if self.out_mask[row] : continue
            row_cost = []
            for col in range(self.vertex_num) :
                if self.in_mask[col] : continue
                row_cost.append(self.cost_matrix[row][col])
            rst.append(row_cost)
        return rst
    def get_path(self) :
        root_id = 0
        from_id = self.path_pair[root_id]
        path = [ root_id ]
        while from_id != root_id :
            path.append(from_id)
            from_id = self.path_pair[from_id]
        path.append(root_id)
        return path

    def check_graph_state(self) :
        '''
        multi state to be returned !
        1 : get the hamiltonnian 
        0 : normal state , no circle 
        -1 : valid state , has a circle , but not a hamiltonian !
        '''
        is_visited = [ False ] * self.vertex_num
        from_node = 0 
        is_visited[from_node] = True # set from node visited state 
        while True :
            next_node = self.path_pair[from_node]
            if next_node == -1 :
                return 0
            if is_visited[next_node] == False :
                is_visited[next_node] = True
                from_node = next_node 
            else :
                # has circle 
                # hamiltoniam or local circle
                all_visited = reduce(lambda a , b : a and b , is_visited)
                if all_visited :
                    return 1
                else :
                    return -1

    def normalize_cost_matrix_and_update_low_bound_row(self , row_idx) :
        if self.out_mask[row_idx] :
            return # this row has been masked (deleted)
        ## find min cost of row 
        # get all the col vlaue which has not been masked !
        valid_cost = [ self.cost_matrix[row_idx][j] for j in range(self.vertex_num) if not self.in_mask[j] ]  
        if len(valid_cost) == 0 : return # no cols !
        min_value = min(valid_cost)
        if min_value == INF : 
            # 就是说，这一行除了被删除的元素外，全部为INF
            # 这说明已经不连通了！！ 将low_bound置为INF，期望在分支界限中将其剪枝
            self.low_bound = INF
            return 
        for j in range(self.vertex_num) :
            if not self.in_mask[j] and self.cost_matrix[row_idx][j] != INF :
                self.cost_matrix[row_idx][j] -= min_value
        self.low_bound += min_value

    def normalize_cost_matrix_and_update_low_bound_col(self , col_idx) :
        if self.in_mask[col_idx] : return # this col has been masked !
        # find all cost
        valid_cost = [ self.cost_matrix[i][col_idx] for i in range(self.vertex_num) if not self.out_mask[i] ]  
        if len(valid_cost) == 0 : return 
        min_value = min(valid_cost)
        if min_value == INF : 
            self.low_bound = INF
            return 
        for i in range(self.vertex_num) :
            if not self.out_mask[i] and self.cost_matrix[i][col_idx] != INF :
                self.cost_matrix[i][col_idx] -= min_value
        self.low_bound += min_value


    def normalize_cost_matrix_and_update_low_bound(self) :
        '''
        except the masked row and col ,
        we need one row has at least one zero , one col has at least one zero !
        call the operation as "Normalize"!! 
        after do it , we'll update the low bound ! just add the deleted value !
        we just call the sub function to do it !
        '''
        for row_idx in range(self.vertex_num) :
            if not self.out_mask[row_idx] :
                self.normalize_cost_matrix_and_update_low_bound_row(row_idx)

        for col_idx in range(self.vertex_num) :
            if not self.in_mask[col_idx] :
                self.normalize_cost_matrix_and_update_low_bound_col(col_idx)
    def add_path_pair(self , from_vertex_id , to_vertex_id) :
        self.path_pair[from_vertex_id] = to_vertex_id

    def add_new_mask(self , row , col) :
        self.out_mask[row] = True
        self.in_mask[col] = True

    def disable_edge(self , row , col) :
        self.cost_matrix[row][col] = INF

    def select_one_edge_to_minimize_left_subtree_and_maximum_right_subtrue(self) :
        '''
        As the function name , To select one edge (i , j) to minimize the left tree including the (i,j)
        has the min low bound and right tree without the edge to get the max low bound .
        As to the PPT , it is the `arg_f max f(i,j)`
        Assert ! 
            the cost matrix is normalized ! 
                that is , every row and col has at least one zero except for the masked row and cols .
            the cost matrix is valid !
                no circle in the seletec path . No mater the circle is hamiltonian or others .
        This function is implemented confusion !!
        It may be dangerous !

        Return :
            (row_idx , col_idx)
        '''
        # assert( this cost matrix is normalized and valid) !
        max_min_addtion = 0
        max_cor_row_idx = -1 # corresponding row idx 
        max_cor_col_idx = -1
        has_finded = False 
        for row_idx in range(self.vertex_num) :
            if self.out_mask[row_idx] : continue
            for col_idx in range(self.vertex_num) :
                if self.in_mask[col_idx] : continue
                if self.cost_matrix[row_idx][col_idx] == 0 :
                    # candidate result , get the min cost addtion if set the (row , col) = INF

                    # get the row addtion !
                    # 1. not mask(deleted) 2. not equal to the INF 
                    # using `!= col_idx` to make a operation trans (row ,col) = INF  
                    valid_cost = [ self.cost_matrix[row_idx][j] for j in range(self.vertex_num) 
                                       if not self.in_mask[j] and j != col_idx 
                                          and self.cost_matrix[row_idx][j] != INF ]
                    if len(valid_cost) == 0 :
                        # ? how to deal with ?
                        # 分析 ： mask是一列一列删的，如果因为mask而为空，那么其余行也必然为空。故此行的该列就是
                        #         目标值。
                        #        如果是因为INF而为空，反过来想，INF只可能在不连通时存在。故此时选择该路将使得
                        #        右子树结束。也符合使右子树代价增加最大的原则！！
                        # 总结以上，在此情况下，可以直接返回该值
                        return (row_idx , col_idx)
                    min_out_cost = min(valid_cost)

                    valid_cost = [self.cost_matrix[i][col_idx] for i in range(self.vertex_num) 
                                       if not self.out_mask[i] and i != row_idx 
                                       and self.cost_matrix[i][col_idx] != INF]
                    if len(valid_cost) == 0 :
                        return (row_idx , col_idx) 
                    min_in_cost = min(valid_cost)
                    cur_min_addtion = min_out_cost + min_in_cost
                    if cur_min_addtion > max_min_addtion :
                        max_min_addtion = cur_min_addtion
                        max_cor_row_idx = row_idx
                        max_cor_col_idx = col_idx
                        has_finded = True 
                        break # if is normalized , no other col has value 0 !
        return ( ( max_cor_row_idx , max_cor_col_idx ) if has_finded else None )
  


