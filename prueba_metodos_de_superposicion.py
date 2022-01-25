import numpy as np
import matplotlib.pyplot as plt
from Gaussiana import Gaussiana
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from Estela import Estela
from U_inf import U_inf
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica

"""
Configuraciones de la prueba segun paper: "Limitations to the validity of single wake
superposition in wind farm yield assessment"

Tenemos dos turbinas alineadas separadas por 8D
A continuacion se grafica:
    1) El deficit a la altura del hub para dos turbinas alineadas a 16D por
    atras de la primera (8D del segundo) usando CFD (OpenFOAM).
    2) El deficit de las dos turbinas trabajando independientemente (a 16D de
    la primera turbina y a 8D de la segunda turbina)
    3) El deficit generado por ambas (a 16D de la primera turbina) utilizando
    distintos metodos de superposicion de estelas
"""

# Modelo analitico
gaussiana = Gaussiana()

# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_Rawson(Coord(np.array([0,0,80])))
D = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_Rawson(Coord(np.array([8*D,0,80])))
turbina_parcialmente_alineada = Turbina_Rawson(Coord(np.array([8*D,1*D,80])))
turbina_desalineada = Turbina_Rawson(Coord(np.array([8*D,1.75*D,80])))


# Diferenciacion del actuador discal
cantidad_de_puntos = 5
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)


# Definicion de velocidad de entrada
z_0, z_mast, perfil = 0.01, 80, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 8.2
coord_u = Coord([0,0,z_mast])
u_inf.perfil_flujo_base(coord_u)


""" TURBINAS ALINEADAS """
# calculo el deficit a 16D para la primera turbina independiente

parque_de_turbinas_primera_indep = Parque_de_turbinas([turbina_0], z_0, z_mast)

x_0 = 16*D
y = np.arange(-1.2*D, 1.2*D, 0.01)
z_o = turbina_0.coord.z

data_turbina_0_independiente = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_turbina_0_independiente[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_primera_indep, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)

# calculo el deficit para la segunda turbina independiente (ubicada en x = 8D) a 16D

parque_de_turbinas_alineada_indep = Parque_de_turbinas([turbina_alineada], z_0, z_mast)
x_0 = 16*D

y = np.arange(-1.2*D, 1.2*D, 0.01)
z_o = turbina_0.coord.z

data_turbina_alineada_indep = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_turbina_alineada_indep[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_alineada_indep, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)

# calculo deficit con ambas turbinas

parque_de_turbinas_alineadas = Parque_de_turbinas([turbina_0, turbina_alineada], z_0, z_mast)
parque_de_turbinas_parc_alineadas = Parque_de_turbinas([turbina_0, turbina_parcialmente_alineada], z_0, z_mast)
parque_de_turbinas_desalineadas = Parque_de_turbinas([turbina_0, turbina_desalineada], z_0, z_mast)


x_0 = 16*D
y = np.arange(-1.2*D, 1.2*D, 0.01)
z_o = turbina_0.coord.z

data_prueba_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_desalineadas_Metodo_C = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_alineadas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
    data_prueba_parc_alineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_parc_alineadas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
    data_prueba_desalineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_desalineadas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)

# calculo el deficit generado por ambas (a 16D de la primera turbina) utilizando
# el metodo de superposicion cuadratico 'Metodo_D'

data_prueba_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_desalineadas_Metodo_D = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord, parque_de_turbinas_alineadas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
    data_prueba_parc_alineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord, parque_de_turbinas_parc_alineadas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
    data_prueba_desalineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord, parque_de_turbinas_desalineadas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)

plt.plot(y/D, data_turbina_0_independiente, label = 'Turbina 0 idependiente')
plt.plot(y/D, data_turbina_alineada_indep, label = 'Turbina alineada idependiente')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()
plt.plot(y/D, data_prueba_alineadas_Metodo_C, label = 'Alineadas Metodo C')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_C, label = 'Parc. Ali. Metodo C')
plt.plot(y/D, data_prueba_desalineadas_Metodo_C, label = 'Desalineadas Metodo C')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()
plt.plot(y/D, data_prueba_alineadas_Metodo_D, label = 'Alineadas Metodo D')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_D, label = 'Parc. Ali. Metodo D')
plt.plot(y/D, data_prueba_desalineadas_Metodo_D, label = 'Desalineadas Metodo D')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()