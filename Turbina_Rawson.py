from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
# coding=utf-8
from Turbina import Turbina
from scipy import interpolate

class Turbina_Rawson(Turbina):

    def __init__(self, coord):
        d_0 = 90
        self.U_tabla = np.array([3.97553683,   4.9669611 ,   5.95972269,   6.95196727,
                                      7.95116277,   8.93613964,   9.93634081,  10.92857237,
                                      11.9171516 ,  12.9245659 ,  13.91116425,  14.90904084,
                                      15.9053444 ,  16.88414983,  17.88072698,  18.87876044,
                                      19.87055544, 20.84568607,  21.87016143,  22.8544895,
                                      23.847984  ,  24.83090363])
        self.c_T_tabla = np.array([0.824, 0.791, 0.791, 0.791, 0.732, 0.606, 0.510,
                                      0.433, 0.319, 0.247, 0.196, 0.159, 0.134, 0.115,
                                      0.100, 0.086, 0.074, 0.064, 0.057, 0.050, 0.045, 0.040])
        self.P_tabla = np.array([88, 204, 371, 602, 880, 1147, 1405, 1623, 1729, 1761, 1774,
                                    1786, 1795, 1799, 1800, 1800, 1800, 1800, 1800, 1800,
                                    1800, 1800])
        self.c_P_tabla = np.array([0.3528756612, 0.4188313302, 0.4407975431, 0.4504238495,
                                      0.4410945765, 0.4037893836, 0.3605747665, 0.3129388419,
                                      0.2567853612, 0.2057066378, 0.1659160941, 0.1358084161,
                                      0.1124665859, 0.093973068, 0.0792089026, 0.0673489313,
                                      0.05774329, 0.049880825, 0.0433833884, 0.0379671505,
                                      0.0334162558, 0.0295645645])


        super(Turbina_Rawson, self).__init__(d_0, coord)

    # OUTPUT:
    # cT obtenido considerando el viento de entrada calculado a partir de una interpolacion (spline cubico)
    # de la tabla dada por el fabricante
    def c_T_tabulado(self, U):
        # interpola utilizando los datos dados por el fabricante
        tck = interpolate.interp1d(self.U_tabla, self.c_T_tabla, kind='linear', fill_value=(0, 0), bounds_error=False)
        # calcula el cT en el viento U
        c_Tnew = tck(U)
        return c_Tnew

    # OUTPUT:
    # potencia obtenida considerando el viento de entrada calculado a partir de una interpolacion (spline cubico)
    # de la tabla dada por el fabricante
    def P_tabulado(self, U):
        tck = interpolate.interp1d(self.U_tabla, self.P_tabla, kind='linear', fill_value=(0, 0), bounds_error=False)
        Pnew = tck(U)
        return Pnew

    # OUTPUT:
    # cP obtenido considerando el viento de entrada calculado a partir de una interpolacion (spline cubico) 
    # de la tabla dada por el fabricante
    def c_P_tabulado(self, U):
        tck = interpolate.interp1d(self.U_tabla, self.c_P_tabla, kind='linear', fill_value=(0, 0), bounds_error=False)
        c_Pnew = tck(U)
        return c_Pnew
