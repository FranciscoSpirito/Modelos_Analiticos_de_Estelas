from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from U_inf import U_inf
from Gaussiana import Gaussiana
from calcular_potencia_del_parque_deterministica import calcular_potencia_del_parque_integral_deterministica
from load_txt_datos import cargar_datos

angulos = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
potencia_del_parque = []

# Carga las turbinas del parque
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
turbinas_list = cargar_datos('coordenadas_turbinas', ruta)
d0 = turbinas_list[0].d_0

for angulo in angulos:

    gaussiana = Gaussiana()

    # Define el tipo de perfil de velocidades cte o log
    perfil = 'cte'
    z_0 = 0.01
    z_mast = 180
    u_inf = U_inf(z_mast, z_0, perfil)
    u_inf.u_mast = 8.23
    coord_u = Coord([0,0,180])
    u_inf.perfil_flujo_base(coord_u)

    z_mast = turbinas_list[0].coord.z
    # z_0 de la superficie
    z_0 = 0.01

    parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)
    parque_de_turbinas.rotar(angulo)
    # Define cantidad de puntos y divide el actuador discal en diferenciales similares
    cantidad_de_puntos = 10
    espesor = turbinas_list[0].definicion_de_espesor(cantidad_de_puntos)
    lista_coord_normalizadas, lista_dAi_normalizados = turbinas_list[0].coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

    # Calcula CT, CP, P de las turbinas
    data_prueba = calcular_potencia_del_parque_integral_deterministica(gaussiana, 'Metodo_D', parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)

    # potencia nominal cuando la turbina trabaja con un viento de 8.2 m/s
    potencia_mast = 1800*1000

    potencia_de_cada_turbina_normalizada = []

    for turbina in parque_de_turbinas.turbinas:
        if turbina.potencia is None:
            print(turbina.coord)
        potencia_de_cada_turbina_normalizada.append(turbina.potencia/potencia_mast)
    potencia = sum(potencia_de_cada_turbina_normalizada)
    potencia_del_parque.append(potencia/43)

    fig, axes = plt.subplots(2, 2)
    # Ploteo Turbinas
    for turbina in parque_de_turbinas.turbinas:
        x = float(turbina.coord.x)
        y = float(turbina.coord.y)
        axes[0][0].plot(x, y, 'o')
        axes[0][0].text(x * (1 + 0.01), y + 100, round(np.linalg.norm(turbina.U_f_base), 2), fontsize=6)
    axes[0][0].set_title('Flujo Base')
    for turbina in parque_de_turbinas.turbinas:
        x = float(turbina.coord.x)
        y = float(turbina.coord.y)
        axes[0][1].plot(x, y, 'o')
        axes[0][1].text(x *(1 +0.01), y + 100, round(turbina.potencia/potencia_mast, 2), fontsize=6)
    axes[0][1].set_title('Potencia')
    for turbina in parque_de_turbinas.turbinas:
        x = float(turbina.coord.x)
        y = float(turbina.coord.y)
        axes[1][0].plot(x, y, 'o')
        axes[1][0].text(x * (1 + 0.01), y + 100, round(turbina.c_T, 2), fontsize=6)
    axes[1][0].set_title('CT')
    fig.suptitle(angulo)
    fig.tight_layout()
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