from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
# coding=utf-8
from Turbina import Turbina
from scipy import interpolate

class Turbina_5MW_NREL(Turbina):

    def __init__(self, coord):
        d_0 = 126
        self.U_tabla = np.array([4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0])
        self.c_T_tabla = np.array([0.9126726099033362, 0.8687903370768008, 0.7800469905014111, 0.7726336604294938, 0.7702530978349217, 0.7675751963849531, 0.764630155765929, 0.7460760574610608, 0.5327700556243904, 0.3921680691153145, 0.3048141858493565, 0.24439151289556107, 0.20039542167168448, 0.1673223774804871, 0.14186054848190674, 0.12189240591443229, 0.10558063842098647, 0.09248896984799376, 0.08176302128348775, 0.07265310356753815, 0.06506351706348608, 0.058637926679061946])
        self.c_P_tabla = np.array([0.4532499420585651, 0.4933995547191924, 0.4912461581129812, 0.4899536862714288, 0.4895791271379793, 0.4891382449365905, 0.48862357237312426, 0.4843993765394049, 0.4013036072639607, 0.3157278495306418, 0.2527758569157412, 0.20547022779176713, 0.16928562086371082, 0.1411143058147779, 0.11886022629346842, 0.1011893180181898, 0.08662837993876549, 0.07485556771275063, 0.06518027703193373, 0.056953354560288764, 0.050114019857823155, 0.04434413096148738])


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
