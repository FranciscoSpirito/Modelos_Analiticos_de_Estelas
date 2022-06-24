from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from ParqueEolico import ParqueEolico
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from U_inf import U_inf
from GaussianoAdaptadoTerreno import GaussianoAdaptadoTerreno
from IsoSuperficie import IsoSuperficie
from calcular_u_en_coord_con_terreno import calcular_u_con_terreno
from calcular_potencia_del_parque_con_terreno import calcular_potencia_del_parque_con_terreno
from load_txt_datos import cargar_datos
from scipy.interpolate import griddata


d0 = 90

# Carga datos desdes .raw o .txt e inicializa la clase IsoSuperficie
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.270.00.U8.50.raw"
xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
x, y, z, u, v, w = np.array(xl), np.array(yl), np.array(zl), np.array(ul), np.array(vl), np.array(wl)
iso_s = IsoSuperficie(x, y, z, u, v, w)
# Genera malla mas comoda y menos densa
iso_s.new_grid(100, d0)

# Carga las turbinas del parque
# ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
# turbinas_list  = cargar_datos('coordenadas_turbinas', ruta)
turbina_2 = Turbina_Rawson(Coord(np.array([2500,2500, iso_s._interp_z(2500, 2500).item()+80])))
turbina_0 = Turbina_Rawson(Coord(np.array([2500 + 8*d0, 2500 , iso_s._interp_z(2500, 2500).item()+80])))
turbina_3 = Turbina_Rawson(Coord(np.array([2500 + 8*d0, 2500 + 4*d0, iso_s._interp_z(2500 + 8*d0, 2500 + 4*d0).item()+80])))
turbina_1 = Turbina_Rawson(Coord(np.array([2500 + 16*d0, 2500, iso_s._interp_z(2500 + 16*d0, 2500).item()+80])))

turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3]

gaussiana_adaptado_al_terreno = GaussianoAdaptadoTerreno()

# Define el tipo de perfil de velocidades cte o log
z_mast, z_0, perfil = turbinas_list[0].coord.z, 0.01, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)

parque_de_turbinas = ParqueEolico(turbinas_list, z_0, z_mast)

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

# Define los interpoladores
iso_s.redef_interpoladores(streamlines, d0)
iso_s.flujo_base_turbinas(turbinas_list)

# Mallado para calculo de campo de velocidades
meshXmin, meshXmax, npoiX = 2000, 4500, 50
meshYmin, meshYmax, npoiY = 2000, 3000, 50
xg = np.linspace(meshXmin, meshXmax, npoiX)
yg = np.linspace(meshYmin, meshYmax, npoiY)
XG, YG = np.meshgrid(xg, yg)
positions = np.vstack([XG.ravel(), YG.ravel()])
coordenadas = []
for i in range(len(positions[0])):
    x = positions[:,i][0]
    y = positions[:,i][1]
    cooord = Coord([x, y, 80 + iso_s._interp_z(x,y).item()])
    coordenadas.append(cooord)
# Calcula CT, CP, P de las turbinas
# data_prueba = calcular_potencia_del_parque_con_terreno(gaussiana_adaptado_al_terreno, 'largest', parque_de_turbinas, u_inf, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
velocidades = []
for coord in coordenadas:
    velocidades.append(calcular_u_con_terreno(gaussiana_adaptado_al_terreno, 'Metodo_D', coord, parque_de_turbinas, iso_s, lista_coord_normalizadas,lista_dAi_normalizados))
print(velocidades)


# Ploteo
VG = griddata((positions[0], positions[1]), velocidades, (XG, YG), method='linear')
fig1 = plt.figure()
ax = fig1.add_subplot(1, 1, 1)
count = ax.contourf(XG,YG,VG)
fig1.colorbar(count)
plt.show()