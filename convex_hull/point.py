#coding=utf8

class Point(object):
    def __init__(self , x=0 , y=0) :
        self.x = x
        self.y = y

    def __str__(self) :
        return "(" + ','.join([str(self.x) , str(self.y)]) + ")"     

    def __repr__(self) :
        return self.__str__()

    def __add__(self , pnt) :
        return Point(self.x + pnt.x , self.y + pnt.y)

    def __mul__(self , singular) :
        return Point(self.x * singular , self.y * singular)

    def __sub__(self , pnt) :
        return Point(self.x - pnt.x, self.y - pnt.y)