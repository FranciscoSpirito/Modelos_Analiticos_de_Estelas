from __future__ import division
# coding=utf-8

from Modelo import Modelo
from numpy import pi

class Larsen(Modelo):

    def __init__(self):
        super(Larsen, self).__init__()

    def evaluar_deficit_normalizado(self, turbina, coord_selec):

        # ambient streamwise turbulence intensity:
        Ia = 0.1
        D_eff = turbina.d_0 * ( (1 + (1 - turbina.c_T)**0.5 ) / (2 * (1 - turbina.c_T)*0.5 ) )**0.5
        R_nb = max(1.08 * turbina.d_0, 1.08 * turbina.d_0 + 21.7 * turbina.d_0 * (Ia - 0.05))
        R_95 = 0.5 * (R_nb + min(turbina.coord.z, R_nb))
        x_0 = (9.5 * turbina.d_0) / (((2 * R_95) / D_eff)**3 - 1)
        c_T_A = turbina.c_T * pi * (turbina.d_0/2)**2
        C1 = (D_eff / 2)**(5/2) * (105 / (2*pi))**(-1/2) * (c_T_A * x_0)**(-5/6)
        dist = coord_selec.x-x_0
        radio_W = (35 / (2*pi))**(1/5) * (3 * C1**2)**(1/5) * (c_T_A * dist)**(1/3)

        if (abs(coord_selec.y - turbina.coord.y) <= (radio_W)) & (abs(coord_selec.z - turbina.coord.z) <= (radio_W)):
            r = ((turbina.coord.y - coord_selec.y)**2 + (turbina.coord.z - coord_selec.z)**2)**0.5
            U_inf = 2.2
            return (-U_inf / 9) * (c_T_A * dist**(-2))**(1/3) * (r**(3/2) * (3 * C1**2 * c_T_A * dist)**(-1/2) - (35 / (2*pi))**(3/10) * (3 * C1**2)**(-1/5))**2

        else:
            return 0

    def __repr__(self):
        return "Larsen"
