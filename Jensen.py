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

#Terreno plano
    # def evaluar_deficit_normalizado(self, turbina, coord_selec):
    #     r_w = (turbina.d_0/2) + self.k_wake * coord_selec.x
    #     if (abs(coord_selec.y) <= (r_w)) & (abs(coord_selec.z - turbina.coord.z) <= (r_w)):
    #         return (1 - (1 - turbina.c_T)**0.5 ) / (1 + (2*(self.k_wake)*coord_selec.x)/turbina.d_0)**2
    #     else:
    #         return 0

#Terreno irregular
    def evaluar_deficit_normalizado(self, turbina, coord_selec):
        r_w = (turbina.d_0/2) + self.k_wake * (abs(turbina.coord.x - coord_selec.x))
        if (((turbina.coord.y - coord_selec.y)**2 + (turbina.coord.z - coord_selec.z)**2)**0.5 <= (r_w / 2)):
            verificacion = (1 - (1 - turbina.c_T)**0.5 ) / (1 + (2*(self.k_wake)*abs(turbina.coord.x-coord_selec.x))/turbina.d_0)**2
            if verificacion == None:
                print('Coord. Turbina aguas arriba =', turbina.coord)
                print('Coord. a evaluar =', coord)
                print('CT de turbina aguas arriba =', turbina.c_T)
            return (1 - (1 - turbina.c_T)**0.5 ) / (1 + (2*(self.k_wake)*abs(turbina.coord.x-coord_selec.x))/turbina.d_0)**2
        else:
            return 0

    def __repr__(self):
        return "Jenssen"