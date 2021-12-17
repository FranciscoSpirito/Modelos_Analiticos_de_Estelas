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

ruta1  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.00.00.U8.50.raw"
ruta2  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.22.50.U8.50.raw"
ruta3  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.45.00.U8.50.raw"
ruta4  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.67.50.U8.50.raw"
ruta5  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.90.00.U8.50.raw"
ruta6  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.112.50.U8.50.raw"
ruta7  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.135.00.U8.50.raw"
ruta8  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.157.50.U8.50.raw"
ruta9  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.180.00.U8.50.raw"
ruta10  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.202.50.U8.50.raw"
ruta11 = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.225.00.U8.50.raw"
ruta12  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.247.50.U8.50.raw"
ruta13  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.270.00.U8.50.raw"
ruta14  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.292.50.U8.50.raw"
ruta15  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.315.00.U8.50.raw"
ruta16  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.337.50.U8.50.raw"
rutas = [ruta1, ruta2, ruta3, ruta4, ruta5, ruta6, ruta7, ruta8, ruta9, ruta10, ruta11, ruta12, ruta13, ruta14, ruta15, ruta16]
isoSuperficies = []
for ruta in rutas:
     xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
     x = np.array(xl)
     y = np.array(yl)
     z = np.array(zl)
     u = np.array(ul)
     v = np.array(vl)
     w = np.array(wl)
     iso_s = Iso_Superficie(x, y, z, u, v, w)
     isoSuperficies.append(iso_s)

angulos = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
# angulos = ["00.00", "22.50", "45.00", "67.50", "90.00", "112.50", "135.00", "157.50", "180.00", "202.50", "225.00", "247.50", "270.00", "292.50", "315.00"]
potencia_del_parque = []

# Carga las turbinas del parque
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
turbinas_list = cargar_datos('coordenadas_turbinas', ruta)
d0 = turbinas_list[0].d_0

for iso_s, angulo in zip(isoSuperficies, angulos):


    # Carga datos desdes .raw o .txt e inicializa la clase Iso_Superficie
    # ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir."+str(angulo)+".U8.50.raw"
    # xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
    # x, y, z, u, v, w = np.array(xl), np.array(yl), np.array(zl), np.array(ul), np.array(vl), np.array(wl)
    # iso_s = Iso_Superficie(x, y, z, u, v, w)

    gaussiana_adaptado_al_terreno = Gaussiana_adaptado_al_Terreno()

    # Define el tipo de perfil de velocidades cte o log
    u_inf = U_inf()
    u_inf.perfil = 'cte'

    z_mast = turbinas_list[0].coord.z
    # z_0 de la superficie
    z_0 = 0.01

    parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)

    # Define cantidad de puntos y divide el actuador discal en diferenciales similares
    cantidad_de_puntos = 10
    espesor = turbinas_list[0].definicion_de_espesor(cantidad_de_puntos)
    lista_coord_normalizadas, lista_dAi_normalizados = turbinas_list[0].coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

    # Genera malla mas comoda y menos densa
    iso_s.new_grid(200, d0)
    nstream = 20 # cantidad de streamlines
    # Define la semilla inicial, debe cubrir todo el terreno
    x_semillas, y_semillas = iso_s.gen_semillas(angulo, nstream)
    dr = 250
    # Calcula las streamlines
    streamlines = iso_s._makeStreamline(x_semillas, y_semillas, dr, angulo, d0)
    # Grafica streamlines sin rotar

    # Define los interpoladores
    iso_s.redef_interpoladores(streamlines, d0)
    iso_s.flujo_base_turbinas(turbinas_list)

    # Calcula CT, CP, P de las turbinas
    data_prueba = calcular_potencia_del_parque_con_terreno(gaussiana_adaptado_al_terreno, 'largest', parque_de_turbinas, u_inf, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)

    # potencia nominal cuando la turbina trabaja con un viento de 8.2 m/s
    potencia_mast = 1800*1000

    potencia_de_cada_turbina_normalizada = []

    for turbina in parque_de_turbinas.turbinas:
        if turbina.potencia == None:
            print(turbina.coord)
        potencia_de_cada_turbina_normalizada.append(turbina.potencia/potencia_mast)
    potencia = sum(potencia_de_cada_turbina_normalizada)
    potencia_del_parque.append(potencia)

    fig, axes = plt.subplots(1, 2)
    # Ploteo posicion de las turbinas rotadas
    for turbina in turbinas_list:
        x = float(turbina.coord.x)
        y = float(turbina.coord.y)
        axes[0].plot(x, y, 'o')
        axes[0].text(x * (1 + 0.01), y * (1 + 0.01), round(turbina.potencia/potencia_mast, 2), fontsize=6)
    axes[0].set_title('Potencia')

    for line in streamlines:
        axes[1].plot(line[0], line[1], '.r')
    axes[1].set_title('Streamlines')
    fig.suptitle(angulo)
    plt.show()

    for turbina_resuelta in parque_de_turbinas.turbinas:
        turbina_resuelta.reiniciar_turbina()

i=0
angulos_float = []
for angulo in angulos:
    angulos_float.append(float(angulo))
plt.plot(angulos_float, potencia_del_parque, 'o')
plt.ylabel('Potencia')
plt.xlabel('Angulo')
plt.show()
print(potencia_del_parque)