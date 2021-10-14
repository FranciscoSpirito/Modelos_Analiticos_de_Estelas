# coding=utf-8
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from Gaussiana import Gaussiana
from Jensen import Jensen
from Frandsen import Frandsen
from Larsen import Larsen
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_BlindTest import Turbina_BlindTest
from Coord import Coord
from U_inf import U_inf
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica


gaussiana = Gaussiana()
jensen = Jensen()
frandsen = Frandsen()
larsen = Larsen()
modelos = [gaussiana, jensen, frandsen]

z_mast = 0.187

u_inf = U_inf()
u_inf.coord_mast = 10 # es parametro del BlindTest
u_inf.perfil = 'cte'   # por ser un tunel de viento

turbina_0 = Turbina_BlindTest(Coord(np.array([0,0,0.817])))
D = turbina_0.d_0

cantidad_de_puntos = 50
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

# z_0 de la superficie
z_0 = 0.1
parque_de_turbinas = Parque_de_turbinas([turbina_0], z_0, z_mast)

z_o = turbina_0.coord.z
y_o = turbina_0.coord.y

iters_estadistica = 100
distancia = 5

y = np.linspace(-1.5*D, 1.5*D, 500)
z = np.linspace(z_o-1.5*D, z_o+1.5*D, 500)
y_norm = y/D
z_norm = z/D


for modelo in modelos:

    x_o = distancia * D
    data_prueba_estadistica = 0
    deficit_estadistica = np.zeros(iters_estadistica)
    deficit = np.zeros(len(y))

    for i in range(len(y)):
        coord = Coord(np.array([x_o, y[i], z_o]))
        velocidad_i = calcular_u_en_coord_integral_deterministica(modelo, 'linear', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas, lista_dAi_normalizados)
        deficit[i] = 1-velocidad_i/u_inf.coord_mast

    plt.plot(y_norm, deficit, label= u'{} (Modelo analítico)'.format(type(modelo).__name__),  linewidth=3)
    plt.xlabel('y/D')
    plt.ylabel('Deficit')
    plt.legend(loc = 'upper right' )
    plt.ylim(0, 0.4)
plt.show()



for modelo in modelos:

    x_o = distancia * D
    data_prueba_estadistica = 0
    deficit_estadistica = np.zeros(iters_estadistica)
    deficit = np.zeros(len(y))

    for i in range(len(y)):
        coord = Coord(np.array([x_o, y_o, z[i]]))
        data_prueba_estadistica = calcular_u_en_coord_integral_deterministica(modelo, 'linear', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas, lista_dAi_normalizados)
        deficit[i] = 1-data_prueba_estadistica/u_inf.coord_mast

    plt.plot(z_norm, deficit, label= u'{} (Modelo analítico)'.format(type(modelo).__name__),  linewidth=3)
    plt.xlabel('z/D')
    plt.ylabel('Deficit')
    plt.legend(loc = 'upper right' )
    plt.ylim(0,0.4)
plt.show()
