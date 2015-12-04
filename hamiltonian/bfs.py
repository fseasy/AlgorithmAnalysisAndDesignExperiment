#coding=utf8

import Queue
import copy
from state import StateMemoryLess as State
## 当图的连通度很高（边密集）、节点很大时，BFS需要指数递增的内存消耗！
## 经过本机测试，当将边生产的概率阈值设为0.5 ， 且节点数为16时，电脑出现卡死、黑屏现象，硬盘狂转，打开任务管理器，
## 出现巨大的内存消耗， 8G内存下此程序最多消耗2G ， 当内存达到99%时，磁盘访问达到100% （应该是在内存转储），IO操作导致
## 机器卡死。然而整个过程CPU消耗都是稳定且不高的。测试了大概半个小时，没有任何结果输出，由于还有代码要写，就关闭了程序。
## 为了防止上述现象出现，在节点数不可变情况下，减小图的连通度，即正大边生成的权值，可以减少可扩展节点的个数。
##  
## 所以为了该程序在PC上运行，需要增大边生成的概率，即config.py中GENERATE_EDGE_PROBABILITY_THRESHOLD值
## 设为0.8时时间尚可，哈密顿环形成概率也可。
##
def find_hamiltonian_in_bfs(vertex , adj_matrix) :
    adj_matrix = copy.copy(adj_matrix) # copy , to avoid change the origin data
    queue = Queue.Queue()
    vertex_num = len(vertex)
    # Build Root State
    # just using convex idx 0 for the root 
    root_vertex_id = 0
    previous_vertex_id = -1 
    visited_state = [False] * vertex_num
    root = State(root_vertex_id , previous_vertex_id , visited_state)
    root.init_path_recorder_from_parent(None)
    queue.put(root)
    while not queue.empty() :
        # visit queue head
        cur_node = queue.get()
        cur_node.set_visited()
        cur_node.add_path(cur_node.get_vertex_id())
        ## ready to extend the childs !
        extendable_convex_id_list = cur_node.get_extendable_vertex_id(adj_matrix)
        # check whether extendable
        if len(extendable_convex_id_list) == 0 :
            if cur_node.has_hamiltonian(root_vertex_id,adj_matrix) :
                # print the path
                print cur_node.get_path()
                return True 
            else :
                continue # no node to be extended ! 
        # extend child
        cur_visited_state = cur_node.get_visited_state()
        previous_vertex_id = cur_node.get_vertex_id()
        for extend_convex_id in extendable_convex_id_list :
            extend_state = State(extend_convex_id ,previous_vertex_id , 
                                 copy.copy(cur_visited_state)) # make a copy .
                           # the copy is necessary . if No Copy , all node share one list
            extend_state.init_path_recorder_from_parent(cur_node)

            queue.put(extend_state)
    return False