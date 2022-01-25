from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from U_inf import U_inf
from Gaussiana_adaptado_al_Terreno import Gaussiana_adaptado_al_Terreno
from Iso_Superficie import Iso_Superficie
from calcular_u_en_coord_con_terreno import calcular_u_con_terreno
from calcular_potencia_del_parque_con_terreno import calcular_potencia_del_parque_con_terreno
from load_txt_datos import cargar_datos



d0 = 90

# Carga datos desdes .raw o .txt e inicializa la clase Iso_Superficie
ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.270.00.U8.50.raw"
xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
x, y, z, u, v, w = np.array(xl), np.array(yl), np.array(zl), np.array(ul), np.array(vl), np.array(wl)
iso_s = Iso_Superficie(x, y, z, u, v, w)
# Genera malla mas comoda y menos densa
iso_s.new_grid(100, d0)

x_coord = 5000
y_coord = 2700
z_coord = iso_s._interp_z(x_coord, y_coord).item() + 80
coord = Coord([x_coord, y_coord, z_coord])

# Carga las turbinas del parque
# ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
# turbinas_list  = cargar_datos('coordenadas_turbinas', ruta)
turbina_2 = Turbina_Rawson(Coord(np.array([2500,2500,iso_s._interp_z(2500, 2500).item()+80])))
turbina_0 = Turbina_Rawson(Coord(np.array([2500 + 8*d0, 2500 ,iso_s._interp_z(2500, 2500).item()+80])))
turbina_3 = Turbina_Rawson(Coord(np.array([2500 + 8*d0, 2500 + 4*d0,iso_s._interp_z(2500 + 8*d0, 2500 + 4*d0).item()+80])))
turbina_1 = Turbina_Rawson(Coord(np.array([2500 + 16*d0, 2500,iso_s._interp_z(2500 + 16*d0, 2500).item()+80])))
turbina_4 = Turbina_Rawson(Coord(np.array([ x_coord + d0, y_coord + d0, iso_s._interp_z(x_coord +d0, y_coord + d0).item()+80])))
turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3, turbina_4]


fig , axes = plt.subplots(1,2)


gaussiana_adaptado_al_terreno = Gaussiana_adaptado_al_Terreno()

# Define el tipo de perfil de velocidades cte o log
z_mast, z_0, perfil = turbinas_list[0].coord.z, 0.01, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)

parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)

# Define cantidad de puntos y divide el actuador discal en diferenciales similares
cantidad_de_puntos = 5
espesor = turbinas_list[0].definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbinas_list[0].coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)


angulo = 270 # angulo de direccion del viento
nstream = 20 # cantidad de streamlines
# Define la semilla inicial, debe cubrir todo el terreno
x_semillas, y_semillas = iso_s.gen_semillas(angulo, nstream)
dr = 250
# Calcula las streamlines
streamlines = iso_s._makeStreamline(x_semillas, y_semillas, dr, angulo, d0)
# Grafica streamlines sin rotar
for line in streamlines:
    axes[1].plot(line[0], line[1], '.r')
ldc = streamlines[10]
axes[1].text(ldc[0][3], ldc[1][3], 'inicio', fontsize=6)
axes[1].text(ldc[0][len(ldc[0])-3], ldc[1][len(ldc[0])-3], 'final', fontsize=6)
axes[1].set_xlim(iso_s.meshXmin, iso_s.meshXmax)
axes[1].set_ylim(iso_s.meshYmin, iso_s.meshYmax)

# Define los interpoladores
iso_s.redef_interpoladores(streamlines, d0)
iso_s.flujo_base_turbinas(turbinas_list)

# Calcula CT, CP, P de las turbinas
# data_prueba = calcular_potencia_del_parque_con_terreno(gaussiana_adaptado_al_terreno, 'largest', parque_de_turbinas, u_inf, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
data_prueba = calcular_u_con_terreno(gaussiana_adaptado_al_terreno, 'Metodo_Largest', coord, parque_de_turbinas, u_inf, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
print(data_prueba)
# potencia nominal cuando la turbina trabaja con un viento de 8.2 m/s
potencia_mast = 1800 * 1000

potencia_de_cada_turbina_normalizada = []

for turbina in parque_de_turbinas.turbinas:
    if turbina.potencia is None:
        print(turbina.coord)
    else:
        potencia_de_cada_turbina_normalizada.append(turbina.potencia/potencia_mast)
# Ploteo posicion sin rotar de las turbinas
for turbina in turbinas_list:
    if turbina.potencia is None:
        print(turbina.coord)
    else:
        x = turbina.coord.x
        y = turbina.coord.y
        axes[0].plot(turbina.coord.x, turbina.coord.y, 'o')
        axes[0].text(x*(1 - 0.01), y * (1 + 0.01),str(round(turbina.coord.z,2)), fontsize=6)
        axes[0].text(x*(1 - 0.01), y * (1 - 0.01), round(turbina.potencia / potencia_mast, 2), fontsize=6)
axes[0].set_title('Turbinas')
axes[0].plot(x_coord, y_coord, 'o')
axes[0].text(x_coord*(1 - 0.01), y_coord * (1 + 0.01), 'coord' + str(round(z_coord,2)), fontsize=6)
axes[0].text(x_coord, y_coord * (1 - 0.01), round(data_prueba,2), fontsize=6)
axes[0].set_ylim(2000, 3000)
fig.tight_layout()
plt.show()
print(sum(potencia_de_cada_turbina_normalizada))
print(potencia_de_cada_turbina_normalizada)
print(iso_s.meshXmin, iso_s.meshXmax, iso_s.meshYmin, iso_s.meshYmax)
print(min(iso_s.xng), max(iso_s.xng), min(iso_s.yng), max(iso_s.yng))