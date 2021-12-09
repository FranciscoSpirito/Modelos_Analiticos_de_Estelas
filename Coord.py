from __future__ import division
import numpy as np
# coding=utf-8

class Coord(object):

    def __repr__(self):
        return str(self.x)

    def __init__(self, arreglo):
        self.x = arreglo[0]
        self.y = arreglo[1]
        self.z = arreglo[2]

    def rotar(self, angulo_viento):
        theta = -(180 + (90 - angulo_viento))
        theta_rad = (np.pi / 180) * theta
        R = np.matrix([[np.cos(theta_rad), -np.sin(theta_rad)], [np.sin(theta_rad), np.cos(theta_rad)]])
        vector_coord = np.array([self.x, self.y])
        vector_coord_rotado = np.dot(R, vector_coord)
        self.x = vector_coord_rotado.getA1()[0]
        self.y = vector_coord_rotado.getA1()[1]


