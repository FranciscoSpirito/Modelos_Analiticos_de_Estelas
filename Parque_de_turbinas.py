
from __future__ import division
import numpy as np
# coding=utf-8

class Parque_de_turbinas(object):

    def __init__(self, turbinas, z_0, z_mast):
        self.turbinas = turbinas
        self.z_0 = z_0
        self.potencia = 0
        self.z_mast = z_mast

    # ordena la lista turbinas de izquierda a derecha
    def ordenar_turbinas_de_izquierda_a_derecha(self):
        turbinas_ordenadas = []
        for turbina in self.turbinas:
            self.turbinas.sort(key=lambda turbina:turbina.coord.x)

    def ordenar_turbinas_de_izquierda_a_derecha_con_terreno(self):
        turbinas_ordenadas = []
        for turbina in self.turbinas:
            self.turbinas.sort(key=lambda turbina:turbina.s)

    # OUTPUT:
    # lista de turbinas a la izquierda de una coordenada
    def turbinas_a_la_izquierda_de_una_coord(self, una_coord):
        turbinas_a_la_izquierda = []
        for turbina in self.turbinas:
            if (turbina.coord.x < una_coord.x):
                turbinas_a_la_izquierda.append(turbina)
        return turbinas_a_la_izquierda

    def turbinas_a_la_izquierda_de_una_coord_con_terreno(self, una_coord, iso_s):
        turbinas_a_la_izquierda = []
        una_coord_s = iso_s._interp_s(una_coord.x, una_coord.y).item()
        for turbina in self.turbinas:
            if (turbina.s < una_coord_s):
                turbinas_a_la_izquierda.append(turbina)
        return turbinas_a_la_izquierda

    # recibe un angulo en grados y rota las coordenadas x e y en ese angulo
    def rotar(self, angulo_viento):
        theta = -(180 + (90 - angulo_viento))
        theta_rad = (np.pi/180) * theta
        R = np.matrix([[np.cos(theta_rad), -np.sin(theta_rad)], [np.sin(theta_rad), np.cos(theta_rad)]])
        for turbina in self.turbinas:
            vector_coord = np.array([turbina.coord.x, turbina.coord.y])
            vector_coord_rotado = np.dot(R, vector_coord)
            turbina.coord.x = vector_coord_rotado.getA1()[0]
            turbina.coord.y = vector_coord_rotado.getA1()[1]
