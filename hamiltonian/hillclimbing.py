#coding=utf8

import copy
from state import StateMemoryLess as State

def heuristic_eval_function(sub_vertex_id , adj_matrix , visited_state_list ) :
    '''
    Heuristic evaluation function , score a vertex at the visited_state_list
    使用中文来说明：
    能够想到的启发式规则实在有限。
    待扩展的子节点，拥有的属性只有： 
    1. 有多少节点与此节点连通
    2. 连通的节点中有多少还没有被访问（在当前访问状态下，即visited_state_list）
    一个很直观的想法：
    若一个子节点，有最多的连通、未被访问的节点数，那么有更大的可能由父节点（前一个节点）到此子节点
    的路径在此哈密顿环上！
    如果存在 有相同连通、未被访问的节点数 的多个子节点，那么选择有最大连通数的子节点。

    总结一下，有两个规则（两个规则有重叠部分）：
    1. 选 有最多的连通、未被访问的节点数 的子节点
    2. 在1的基础上，若相同，则选择有最多连通数的子节点
    由于是打分函数，我们需要考虑将上述两个规则变为分数。
    由于上述有两个规则有重叠部分——连通数，我们设计一个无重叠的启发式打分函数：
    
    分数 = 连通且未被访问的节点数 * 节点数 + 连通但已经被访问过的节点数

    前一个量乘上节点数，是为了强制使得第一个量为 关键因子！ 在此条件下，应该只有在第一个量
    相同时，才会考虑第二量。
    因为前一个量每次增量是大于等于后一个分量的最大值的，直观的可以证明，只要第一个量大，
    那么它的分数一定大，而与第二个量无关！
    
    #### 反转了！！！####
    经过打印操作次数，与普通dfs比较，发现上述规则很大概率使得其遍历数增大！！
    于是给上述值去反！ 结果大部分情况下果然其遍历次数比dfs小！
    
    确认了上述排序以及压栈操作没有反！

    # 想到一个可能的解释 —— 连接的点越少，可能有较大概率事一条关键路径。
    '''
    convex_num = len(visited_state_list)
    connected_not_visited_num = 0
    connected_visited_num = 0
    child_convex_adj_list = adj_matrix[sub_vertex_id]
    for i in range(convex_num) :
        if child_convex_adj_list[i] == False :
            continue
        if visited_state_list[i] == True :
            connected_visited_num += 1 
        else :
            connected_not_visited_num += 1
    # get the negative value , and has a good perfomance in decreasing traversal time
    # It is amazing ... and confusing ... 
    return - ( connected_not_visited_num * convex_num + connected_visited_num )

def sort_sub_convex_in_heuristic_rule_with_increasing_order(sub_vertex_list , adj_matrix , visited_state_list ) :
    '''
    sort sub convex under the heruistic evalution function .
    in increasing order ! The bigger , the ealier to be visit .
    but stack is auto reversed -> the ealier push , the later visit .
    so we just need to push the return list to stack in order !! and the bigest item is
    on the stack top .  
    '''
    scores = [ heuristic_eval_function(sub_vertex_id , adj_matrix , visited_state_list) 
               for sub_vertex_id in sub_vertex_list ]
    sorted_rst = sorted(zip( sub_vertex_list , scores ) , key=lambda t : t[1] )
    return [ t[0] for t in  sorted_rst ]

def find_hamiltonian_in_hillclimbing(vertex , adj_matrix , timer) :
    adj_matrix = copy.copy(adj_matrix) # copy , to avoid change the origin data
    stack = []
    vertex_num = len(vertex)
    # Build Root State
    # just using convex idx 0 for the root 
    root_vertex_id = 0
    previous_vertex_id = -1 
    visited_state = [False] * vertex_num
    path = [ ]
    root = State(root_vertex_id , previous_vertex_id , visited_state , path)
    stack.append(root)
    op_nums = 0

    while len(stack) > 0 :
        # visit stack top
        cur_node = stack.pop()
        cur_node.set_visited()
        cur_node.add_path(cur_node.get_vertex_id())
        
        op_nums += 1

        ## ready to extend the childs !
        extendable_convex_id_list = cur_node.get_extendable_vertex_id(adj_matrix)
        # check whether extendable
        if len(extendable_convex_id_list) == 0 :
            if cur_node.has_hamiltonian(root_vertex_id,adj_matrix) :
                path = cur_node.get_path()
                return path + path[:1]   
            else :
                continue # no node to be extended ! 
                # extend child
        cur_visited_state = cur_node.get_visited_state()
        previous_vertex_id = cur_node.get_vertex_id()
        previous_path = cur_node.get_path()
        # sort the child under the herustic evalution function
        extendable_convex_id_list = ( 
                sort_sub_convex_in_heuristic_rule_with_increasing_order(
                                    extendable_convex_id_list , adj_matrix ,
                                    cur_visited_state )
                                    )
        for extend_convex_id in extendable_convex_id_list :
            extend_state = State(extend_convex_id ,previous_vertex_id , 
                                 copy.copy(cur_visited_state) , copy.copy(previous_path)) 
            stack.append(extend_state)
    return None

        

