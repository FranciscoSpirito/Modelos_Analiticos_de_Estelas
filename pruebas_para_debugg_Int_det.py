from __future__ import division
import numpy as np
from Gaussiana import Gaussiana
from Jensen import Jensen
from Frandsen import Frandsen
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from U_inf import U_inf
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica
from calcular_potencia_del_parque_deterministica import calcular_potencia_del_parque_integral_deterministica
from load_txt_datos import cargar_datos
import matplotlib.pyplot as plt

"""
Se realiza una prueba, igual a prueba rawson altura
donde se cambia el metodo de integrar 
"""

gaussiana = Gaussiana()
D = 90


turbina_0 = Turbina_Rawson(Coord(np.array([0,0,250])))
turbina_1 = Turbina_Rawson(Coord(np.array([90*5,0,250])))
turbina_2 = Turbina_Rawson(Coord(np.array([90*10,0,250])))
# turbina_3 = Turbina_Rawson(Coord(np.array([(5),(-5),250])))
turbinas_list = [turbina_0, turbina_1, turbina_2]

# ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
# turbinas_list = cargar_datos('coordenadas_turbinas', ruta)

perfil = 'cte'
z_0 = 0.01
z_mast = 180
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 8.2
coord_u = Coord([0,0,180])
u_inf.perfil_flujo_base(coord_u)
parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)

# i=1
# for turbina in parque_de_turbinas.turbinas:
#     plt.plot(turbina.coord.x, turbina.coord.y, 'o')
#     plt.text(turbina.coord.x, turbina.coord.y, i)
#     i+=1
# plt.show()

cantidad_de_puntos = 1
espesor = turbinas_list[0].definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbinas_list[0].coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

x_o = 6000
y_o = 0
z_o = 180

coord = Coord(np.array([x_o, y_o, z_o]))

data_prueba = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_Momento_Lineal', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
# print(data_prueba)
# calcular_potencia_del_parque_integral_deterministica(gaussiana, 'Metodo_C', parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
# potencia nominal cuando la turbina trabaja con un viento de 8.2 m/s
potencia_mast = 949.027296358 * 1000

potencia_de_cada_turbina_normalizada = []

for turbina in turbinas_list:
    if turbina.potencia is None:
        print(turbina.coord)
    else:
        potencia_de_cada_turbina_normalizada.append(float(turbina.potencia)/potencia_mast)

print(sum(potencia_de_cada_turbina_normalizada))