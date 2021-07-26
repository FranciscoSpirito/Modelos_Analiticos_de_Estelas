from __future__ import division
import numpy as np
from numpy import abs
# coding=utf-8

from Modelo import Modelo

#k_wake = 0.1						# proposed by Jensen
# k_wake_on_shore = 0.075			#suggested in the literature
#k_wake_off_shore = 0.04 and 0.05	#suggested in the literature

class Frandsen(Modelo):

    def __init__(self):
        super(Frandsen, self).__init__()
        self.k_wake = 0.1

    def evaluar_deficit_normalizado(self, turbina, coord_selec):
        beta = 0.5 * ((1+((1 - turbina.c_T)**0.5))/((1 - turbina.c_T)**0.5))
        d_w = ((beta + 0.7 * (coord_selec.x/turbina.d_0))**0.5)*turbina.d_0
        a_w = np.pi * (d_w / 2)**2
        d_0 =(beta**0.5) * turbina.d_0
        a_0 = np.pi * (d_0 / 2)**2
        if (abs(coord_selec.y - turbina.coord.y) <= (d_w / 2)) & (abs(coord_selec.z - turbina.coord.z) <= (d_w / 2)):
            return 0.5 * (1 - (1 - (2*turbina.c_T) * (a_0/a_w) )**0.5)
        else:
            return 0

    def __repr__(self):
        return "Frandsen"