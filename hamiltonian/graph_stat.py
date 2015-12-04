#coding=utf8

from matplotlib import pyplot as plot
import networkx as nx
import copy
from config import GRAPH_DRAWING_NUM_LIMIT as LIMIT

class GraphStat(object) :
    def __init__(self) :
        self.vertex_list = []
        self.adj_matrix_list = []
        self.bfs_path = []
        self.dfs_path = []
        self.hill_climbing_path = []
        self.branch_and_bound_path = []
        # for complete graph (branch and bound)
        self.com_vertex_list = []
        self.com_cost_matrix_list = []

    def add_stat_graph(self , vertex , adj_matrix) :
        self.vertex_list.append(copy.copy(vertex))
        self.adj_matrix_list.append(copy.deepcopy(adj_matrix))

    def add_stat_complete_graph(self , vertex , cost_matrix) :
        self.com_vertex_list.append(copy.copy(vertex))
        self.com_cost_matrix_list.append(copy.deepcopy(cost_matrix))

    def add_stat_bfs_path(self,bfs_path) :
        self.bfs_path.append(copy.copy(bfs_path))

    def add_stat_dfs_path(self , dfs_path) :
        self.dfs_path.append(copy.copy(dfs_path))

    def add_stat_hill_climbing_path(self , hill_climbing_path) :
        self.hill_climbing_path.append(copy.copy(hill_climbing_path))

    def add_stat_branch_and_bound_path(self , branch_and_bound_path) :
        self.branch_and_bound_path.append(copy.copy(branch_and_bound_path))

    def draw_stat(self) :
        
        ## fiure 1 : draw hamiltonian in 3 different method in different number of vertex
        #  for different size of vertex , we'll draw BFS , DFS , HillClimbing result
        #  in the same graph .
        #  if no hamilton , no path will be paint ! 
        figure_1_title = "Hamiltonian in 3 different number in different size or vertex"
        plot.figure(figure_1_title)
        plot.suptitle(figure_1_title)
        generate_edges_from_path = lambda path : [ (path[i] , path[i+1]) 
                                                  for i in range(len(path)-1) ]
        sub_graph_num = min(LIMIT , len(self.vertex_list))
        for sub_graph_idx in range(sub_graph_num) :
            plot.subplot(1 , sub_graph_num , sub_graph_idx + 1)
            vertex = self.vertex_list[sub_graph_idx]
            adj_matrix = self.adj_matrix_list[sub_graph_idx]
            vertex_num = len(vertex)
            
            # draw graph

            g = nx.Graph()
            for from_vertex_idx in range(vertex_num-1) :
                for to_vertex_idx in range(from_vertex_idx +1 , vertex_num) :
                    if adj_matrix[from_vertex_idx][to_vertex_idx] :
                        g.add_edge(from_vertex_idx , to_vertex_idx)
            g.add_nodes_from(vertex)
            pos = nx.spring_layout(g)
            
            nx.draw_networkx_nodes(g,pos,node_color='r')
            nx.draw_networkx_edges(g,pos,style="dashdot",width=1.)
            nx.draw_networkx_labels(g,pos)
            # draw path 
            paths = [self.dfs_path[sub_graph_idx] , self.bfs_path[sub_graph_idx] ,
                     self.hill_climbing_path[sub_graph_idx]]
            labels = ["BFS" , "DFS" , "HillClimbing"]
            colors = ['r' , 'g' , 'c']
            styles = ['dashed','dotted','dashed']
            for path_idx , path in enumerate(paths) :
                g_path = nx.Graph().to_directed()
                label = labels[path_idx]
                color = colors[path_idx]
                style = styles[path_idx]
                g_path.add_nodes_from(vertex)
                if path is not None :
                    path_edges = generate_edges_from_path(path)
                else :
                    path_edges = []
                g_path.add_edges_from(path_edges)
                nx.draw_networkx_edges(g_path , pos , style=style , 
                                       edge_color=color , label=label,
                                       alpha=0.6 , width=2.) 
            plot.title("Graph (convex %d)" %vertex_num)
            plot.legend()

        ## figure 2 : Min hamiltonian
        figure_2_title = "Find Minimum Hamiltonian using branch and bound in different vertex size"
        plot.figure(figure_2_title)
        plot.suptitle(figure_2_title)
        sub_graph_num = min(LIMIT , len(self.com_vertex_list))
        for sub_graph_idx in range(sub_graph_num) :
            plot.subplot(1 , sub_graph_num , sub_graph_idx + 1)
            vertex = self.com_vertex_list[sub_graph_idx]
            cost_matrix = self.com_cost_matrix_list[sub_graph_idx]
            vertex_num = len(vertex)
            
            # draw graph

            g = nx.Graph()
            for from_vertex_idx in range(vertex_num-1) :
                for to_vertex_idx in range(from_vertex_idx +1 , vertex_num) :
                    g.add_edge(from_vertex_idx , to_vertex_idx , 
                               weight=cost_matrix[from_vertex_idx][to_vertex_idx])
            g.add_nodes_from(vertex)
            pos = nx.spring_layout(g)
            
            nx.draw_networkx_nodes(g,pos,node_color='r')
            nx.draw_networkx_edges(g,pos,style="dashdot",width=1.)
            nx.draw_networkx_labels(g,pos)
      
            g_path = nx.Graph().to_directed()
            g_path.add_nodes_from(vertex)
            path = self.branch_and_bound_path[sub_graph_idx]
            if path is not None :
                path_edges = generate_edges_from_path(path)
            else :
                path_edges = []
            g_path.add_edges_from(path_edges)
            nx.draw_networkx_edges(g_path , pos , 
                                   edge_color='r' ,
                                   alpha=0.6 , width=2.) 
            plot.title("Complete Graph (convex %d)" %vertex_num)









