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

# Carga datos desdes .raw o .txt e inicializa la clase Iso_Superficie
ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.180.00.U8.50.raw"
xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
x, y, z, u, v, w = np.array(xl), np.array(yl), np.array(zl), np.array(ul), np.array(vl), np.array(wl)
iso_s = Iso_Superficie(x, y, z, u, v, w)

gaussiana_adaptado_al_terreno = Gaussiana_adaptado_al_Terreno()

# Define el tipo de perfil de velocidades cte o log
u_inf = U_inf()
u_inf.perfil = 'log'

# Carga las turbinas del parque
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
turbinas_list  = cargar_datos('coordenadas_turbinas', ruta)

fig1 , axes1 = plt.subplots(1,1)
# Ploteo posicion sin rotar de las turbinas
turbinas_x = []
turbinas_y = []
for turbina in turbinas_list:
    turbinas_x.append(turbina.coord.x)
    turbinas_y.append(turbina.coord.y)
axes1.plot(turbinas_x, turbinas_y, 'o')
axes1.set_title('Posicion de turbinas sin rotar')

turbina_0 = turbinas_list [0]
z_mast = turbina_0.coord.z
# z_0 de la superficie
z_0 = 0.01

parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)

# Define cantidad de puntos y divide el actuador discal en diferenciales similares
cantidad_de_puntos = 5
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

# Genera malla mas comoda y menos densa
iso_s.new_grid(100)
angulo = 180 # angulo de direccion del viento
nstream = 20 # cantidad de streamlines
# Define la semilla inicial, debe cubrir todo el terreno
x0, y0 = iso_s.gen_semillas(angulo, nstream)
dr = 250
# Calcula las streamlines
streamlines = [iso_s._makeStreamline(*xy, dr) for xy in zip(x0, y0)]
# Grafica streamlines sin rotar
for line in streamlines:
    axes1.plot(line[0], line[1], '.r')

fig2 ,axes2 = plt.subplots(1,1)
# Rota cooordenadas de Turbinas (las referencia al nuevo sistema de coordenadas alineado con el viento)
parque_de_turbinas.rotar(angulo)
# Ploteo posicion de las turbinas rotadas
turbinas_x = []
turbinas_y = []
for turbina in turbinas_list:
    turbinas_x.append(turbina.coord.x)
    turbinas_y.append(turbina.coord.y)
axes2.plot(turbinas_x, turbinas_y, 'o')
axes2.set_title('Posicion de turbinas rotadas')

# Rota streamlines (las referencia al nuevo sistema de coordenadas alineado con el viento)
streamlines = iso_s.rotar(angulo, streamlines)
# Grafica streamlines rotadas
for line in streamlines:
    axes2.plot(line[0], line[1], '.r')
line = streamlines[6]
axes2.plot(line[0][0], line[1][0], '.y')
axes2.plot(line[0][len(line[1])-1], line[1][len(line[1])-1], '.k')
plt.show()

# Define los interpoladores
iso_s.redef_interpoladores(streamlines)
iso_s.flujo_base_turbinas(turbinas_list)

# Calcula CT, CP, P de las turbinas
data_prueba = calcular_potencia_del_parque_con_terreno(gaussiana_adaptado_al_terreno, 'linear', parque_de_turbinas, u_inf, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)

# potencia nominal cuando la turbina trabaja con un viento de 8.2 m/s
potencia_mast = 949.027296358

potencia_de_cada_turbina_normalizada = []

for turbina in turbinas_list:
    if turbina.potencia == None:
        print(turbina.coord)
    potencia_de_cada_turbina_normalizada.append(turbina.potencia/potencia_mast)

print(sum(potencia_de_cada_turbina_normalizada))
print(potencia_de_cada_turbina_normalizada)