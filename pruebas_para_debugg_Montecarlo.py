from __future__ import division
import numpy as np
from numpy import exp
import matplotlib.pyplot as plt
from Gaussiana import Gaussiana
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from U_inf import U_inf
from calcular_u_en_coord_integral_de_montecarlo import calcular_u_en_coord_integral_de_montecarlo



"""
Se realiza una prueba, igual a prueba rawson altura 
"""

gaussiana = Gaussiana()

u_inf = U_inf()
u_inf.coord_mast = 8.2
u_inf.perfil = 'log'


D = 90

D = 90

turbina_0 = Turbina_Rawson(Coord(np.array([(0),(0),250])))
turbina_1 = Turbina_Rawson(Coord(np.array([(3*D),(0),250])))
turbina_2 = Turbina_Rawson(Coord(np.array([(3*D),(4*D),250])))
turbina_3 = Turbina_Rawson(Coord(np.array([(6*D),(2*D),250])))


turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3]
z_mast = turbina_0.coord.z
# z_0 de la superficie
z_0 = 0.01
parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)



x_o = 4200
y_o = 3000
z_o = 250

coord = Coord(np.array([x_o, y_o, z_o]))
N = 1
data_prueba = calcular_u_en_coord_integral_de_montecarlo(gaussiana, 'rss', coord, parque_de_turbinas, u_inf, N)

# potencia nominal cuando la turbina trabaja con un viento de 8.2 m/s
potencia_mast = 949.027296358

potencia_de_cada_turbina_normalizada = []

for turbina in turbinas_list:
    potencia_de_cada_turbina_normalizada.append(float(turbina.potencia)/potencia_mast)

print(sum(potencia_de_cada_turbina_normalizada))