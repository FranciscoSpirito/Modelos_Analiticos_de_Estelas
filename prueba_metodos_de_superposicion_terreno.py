import numpy as np
import matplotlib.pyplot as plt
from Gaussiana_adaptado_al_Terreno import Gaussiana_adaptado_al_Terreno
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from U_inf import U_inf
from calcular_u_en_coord_con_terreno import calcular_u_con_terreno
from load_txt_datos import cargar_datos
from Iso_Superficie import Iso_Superficie


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
gaussiana_adaptado_al_Terreno = Gaussiana_adaptado_al_Terreno()
xtb, ytb, ztb = 3000, 3000, 181
# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_Rawson(Coord(np.array([xtb,ytb,ztb + 80])))
D = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_Rawson(Coord(np.array([xtb+8*D,ytb,ztb+80])))
turbina_parcialmente_alineada = Turbina_Rawson(Coord(np.array([xtb+8*D,ytb+1*D,ztb+80])))
turbina_desalineada = Turbina_Rawson(Coord(np.array([xtb+8*D,ytb+1.75*D,ztb+80])))

# Diferenciacion del actuador discal
cantidad_de_puntos = 25
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Mallado_con_velocidad_cte\mallado_con_u_cte.txt"
xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
x, y, z, u, v, w = np.array(xl), np.array(yl), np.array(zl), np.array(ul), np.array(vl), np.array(wl)
iso_s = Iso_Superficie(x, y, z, u, v, w)
# Genera malla mas comoda y menos densa
iso_s.new_grid(100, D)

angulo = 270 # angulo de direccion del viento
nstream = 2000 # cantidad de streamlines
# Define la semilla inicial, debe cubrir todo el terreno
x_semillas, y_semillas = iso_s.gen_semillas(angulo, nstream)
dr = 250
# Calcula las streamlines
streamlines = iso_s._makeStreamline(x_semillas, y_semillas, dr, angulo, D)

# Define los interpoladores
iso_s.redef_interpoladores(streamlines, D)

# Definicion de velocidad de entrada
z_0, z_mast, perfil = 0.01, 181 + 80, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 8.2
coord_u = Coord([3000,3000,z_mast])
u_inf.perfil_flujo_base(coord_u)


""" TURBINAS ALINEADAS """
# calculo el deficit a 16D para la primera turbina independiente
x_0 = xtb + 16*D
y = np.arange(xtb-1.2*D, ytb+1.2*D, 0.01)
z_o = turbina_0.coord.z
parque_de_turbinas_primera_indep = Parque_de_turbinas([turbina_0], z_0, z_mast)
data_turbina_0_independiente = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_turbina_0_independiente[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_C', coord, parque_de_turbinas_primera_indep, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
turbina_0.reiniciar_turbina()
# calculo el deficit para la segunda turbina independiente (ubicada en x = 8D) a 16D

parque_de_turbinas_alineada_indep = Parque_de_turbinas([turbina_alineada], z_0, z_mast)
data_turbina_alineada_indep = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_turbina_alineada_indep[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_C', coord, parque_de_turbinas_alineada_indep, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
turbina_alineada.reiniciar_turbina()


parque_de_turbinas_alineadas = Parque_de_turbinas([turbina_0, turbina_alineada], z_0, z_mast)
parque_de_turbinas_parc_alineadas = Parque_de_turbinas([turbina_0, turbina_parcialmente_alineada], z_0, z_mast)
parque_de_turbinas_desalineadas = Parque_de_turbinas([turbina_0, turbina_desalineada], z_0, z_mast)

data_prueba_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_desalineadas_Metodo_C = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_alineadas_Metodo_C[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_C', coord, parque_de_turbinas_alineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_parc_alineadas_Metodo_C[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_C', coord, parque_de_turbinas_parc_alineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_desalineadas_Metodo_C[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_C', coord, parque_de_turbinas_desalineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_desalineadas_Metodo_D = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_alineadas_Metodo_D[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_D', coord, parque_de_turbinas_alineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_parc_alineadas_Metodo_D[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_D', coord, parque_de_turbinas_parc_alineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_desalineadas_Metodo_D[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_D', coord, parque_de_turbinas_desalineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_Largest = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_Largest = np.zeros(len(y))
data_prueba_desalineadas_Metodo_Largest = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_alineadas_Metodo_Largest[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_Largest', coord, parque_de_turbinas_alineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_parc_alineadas_Metodo_Largest[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_Largest', coord, parque_de_turbinas_parc_alineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    iso_s.flujo_base_turbinas([turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada])
    data_prueba_desalineadas_Metodo_Largest[i] = calcular_u_con_terreno(gaussiana_adaptado_al_Terreno, 'Metodo_Largest', coord, parque_de_turbinas_desalineadas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)


plt.plot(y/D, data_turbina_0_independiente, label = 'Turbina 0 idependiente')
plt.plot(y/D, data_turbina_alineada_indep, label = 'Turbina alineada idependiente')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion con Terreno')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()
plt.plot(y/D, data_prueba_alineadas_Metodo_C, label = 'Alineadas Metodo C')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_C, label = 'Parc. Ali. Metodo C')
plt.plot(y/D, data_prueba_desalineadas_Metodo_C, label = 'Desalineadas Metodo C')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion con Terreno')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()
plt.plot(y/D, data_prueba_alineadas_Metodo_D, label = 'Alineadas Metodo D')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_D, label = 'Parc. Ali. Metodo D')
plt.plot(y/D, data_prueba_desalineadas_Metodo_D, label = 'Desalineadas Metodo D')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion con Terreno')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()
plt.plot(y/D, data_prueba_alineadas_Metodo_Largest, label = 'Alineadas Metodo Largest')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_Largest, label = 'Parc. Ali. Metodo Largest')
plt.plot(y/D, data_prueba_desalineadas_Metodo_Largest, label = 'Desalineadas Metodo Largest')
plt.legend( loc='lower right', fontsize=5)
plt.title('Prueba Metodos de Superposicion con Terreno')
plt.xlabel('y/D')
plt.ylabel('Velocidades [m/s]')
plt.show()