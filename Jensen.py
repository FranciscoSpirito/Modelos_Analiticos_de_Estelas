from __future__ import division
import numpy as np
# coding=utf-8

from Modelo import Modelo
# Jensen used:
# k_wake = 0.1
#
# suggested values for k wake in the literature are
# k_wake = 0.075 =====> on-shore
# k_wake = 0.04 / 0.05 =====> off-shore ones

class Jensen(Modelo):

    def __init__(self):
        super(Jensen, self).__init__()
        self.k_wake = 0.075

    def evaluar_deficit_normalizado(self, turbina, coord_selec):
        r_w = (turbina.d_0/2) + self.k_wake * coord_selec.x
        if (abs(coord_selec.y) <= (r_w)) & (abs(coord_selec.z - turbina.coord.z) <= (r_w)):
            return (1 - (1 - turbina.c_T)**0.5 ) / (1 + (2*(self.k_wake)*coord_selec.x)/turbina.d_0)**2
        else:
            return 0

    def __repr__(self):
        return "Jenssen"