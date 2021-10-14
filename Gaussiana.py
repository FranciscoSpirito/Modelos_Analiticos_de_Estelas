from __future__ import division
# coding=utf-8

from Modelo import Modelo
from numpy import exp

class Gaussiana(Modelo):

    def __init__(self):
        super(Gaussiana, self).__init__()
        # por ahora los datos estan hardcodeados con los PARAMETROS DEL PAPER, habria
        # que calcularlos correctamente del fit del CFD
        # self.k_estrella = 0.023
        # self.epsilon = 0.219

        # cambio estos valores con el ajuste del OpenFOAM Rawson:
        self.k_estrella = 0.0297
        self.epsilon = 0.3281

        # cambio estos valores con el ajuste del OpenFOAM BlindTest usando gaussiana
        # (no es un muy buen ajuste pero es el que mejor funciona, suponemos que es malo
        # por no ser un caso de laboratorio)
        # self.k_estrella = -0.0016
        # self.epsilon = 0.4082
#Terreno Plano
    # def evaluar_deficit_normalizado(self, turbina, coord_selec):
    #     sigma_n = self.k_estrella * ((coord_selec.x-turbina.coord.x)/turbina.d_0) + self.epsilon
    #     c = 1 - (1-(turbina.c_T/(8*(sigma_n**2))))**(0.5)
    #     return c * exp(-(((coord_selec.y-turbina.coord.y)/turbina.d_0)**2 + ((coord_selec.z-turbina.coord.z)/turbina.d_0)**2) / (2 * (sigma_n**2)))

#Terreno irregular
    def evaluar_deficit_normalizado(self, turbina, coord_selec):
        # sigma_n es sigma/d_0
        sigma_n = (self.k_estrella * (abs(turbina.coord.x - coord_selec.x)/turbina.d_0) + self.epsilon)
        c = 1 - (1-(turbina.c_T/(8*(sigma_n**2))))**(0.5)
        return c * exp(-(((turbina.coord.y - coord_selec.y)/turbina.d_0)**2 + ((turbina.coord.z - coord_selec.z)/turbina.d_0)**2) / (2 * (sigma_n**2)))

    def __repr__(self):
        return "Gaussiana"
