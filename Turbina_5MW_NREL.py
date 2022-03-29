from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
# coding=utf-8
from Turbina import Turbina
from scipy import interpolate

class Turbina_5MW_NREL(Turbina):

    def __init__(self, coord):
        d_0 = 126
        self.U_tabla = np.array([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        self.c_T_tabla = np.array([0.7520550686657348, 0.7516128829462181, 0.7514588681052317, 0.7515138617147656, 0.7513495222110561, 0.7516100186957215, 0.7514985048867064, 0.7513920901507976, 0.7512958134597263, 0.717722980142324, 0.3989701921091376, 0.30994898032322354, 0.2501278125062632, 0.2053411869382588, 0.17176328316380038])
        self.c_P_tabla = np.array([0.5370121121467192, 0.5363145383353082, 0.5360703732558356, 0.5361452596154849, 0.5358956610854716, 0.5362874302502514, 0.5361113578459391, 0.5359546248014831, 0.5358163272161462, 0.5186308982457745, 0.3335393349682015, 0.26457276286057435, 0.2154108414589844, 0.17729295001652468, 0.14804028312771067])


        super(Turbina_5MW_NREL, self).__init__(d_0, coord)

    # OUTPUT:
    def c_T_tabulado(self, U):
        # interpola utilizando los datos dados por el fabricante
        tck = interpolate.interp1d(self.U_tabla, self.c_T_tabla, kind='linear', fill_value=(0, 0), bounds_error=False)
        # calcula el cT en el viento U
        c_Tnew = tck(U)
        return c_Tnew

    # OUTPUT:
    def c_P_tabulado(self, U):
        tck = interpolate.interp1d(self.U_tabla, self.c_P_tabla, kind='linear', fill_value=(0, 0), bounds_error=False)
        c_Pnew = tck(U)
        return c_Pnew
