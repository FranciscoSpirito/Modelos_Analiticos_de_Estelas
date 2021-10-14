from __future__ import division
# coding=utf-8

class Coord(object):

    def __repr__(self):
        return str(self.x)

    def __init__(self, arreglo):
        self.x = arreglo[0]
        self.y = arreglo[1]
        self.z = arreglo[2]


