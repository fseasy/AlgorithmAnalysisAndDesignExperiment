#coding=utf8

def print_2d_array(array_2d) :
    '''
    For adjacent matrix DEBUG 
    if every row or col has one 1 , so the graph is connected !
    And for Undirected Connected Graph , it is a symmetric matrix (对称矩阵) , that is A_{ij} = A{ji}  
    '''
    if len(array_2d) == 0 : return 
    formated_str = "".join( [ "{l[%d]:3}" % i for i in range(len(array_2d[0]))] )
    for l in array_2d :
        print formated_str.format(**locals())

        