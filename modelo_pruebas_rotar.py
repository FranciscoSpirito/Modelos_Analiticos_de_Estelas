import numpy as np
import matplotlib.pyplot as plt
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica
from calcular_u_en_coord_integral_de_montecarlo import calcular_u_en_coord_integral_de_montecarlo
from Turbina_Rawson import Turbina_Rawson
from Turbina import Turbina
from Parque_de_turbinas import Parque_de_turbinas
from Coord import Coord
from U_inf import U_inf
from Jensen import Jensen
from Frandsen import Frandsen
from Gaussiana import Gaussiana



def reiniciar_turbinas(lista_turbinas):
    for turbina in lista_turbinas:
        turbina.reiniciar_turbina()

def sumar_potencia(lista_turbinas):
    potencia_parque = 0
    for turbina in lista_turbinas:
        potencia_parque += turbina.potencia

    return potencia_parque


u_inf = U_inf()
u_inf.coord_mast = 8.2
u_inf.perfil = 'log'


# distancia_1 = 5
# distancia_2 = 10
#
# turbina_0 = Turbina_Rawson(Coord(np.array([0, 0, 80])))
#
# D = turbina_0.d_0
# z_mast = turbina_0.coord.z
# z_0 de la superficie
# z_0 = 0.01
#
# turbina_1 = Turbina_Rawson(Coord(np.array([distancia_1 * D, 19, 80])))
# turbina_2 = Turbina_Rawson(Coord(np.array([distancia_2 * D, 0, 80])))


z_ground = 154




turbina_0 = Turbina_Rawson(Coord(np.array([(0),(0),260 - z_ground])))
turbina_1 = Turbina_Rawson(Coord(np.array([(-204.9),(286.1),269 - z_ground])))
turbina_2 = Turbina_Rawson(Coord(np.array([(41.9),(565.7),256 - z_ground])))
turbina_3 = Turbina_Rawson(Coord(np.array([(8.1),(870),247 - z_ground])))
turbina_4 = Turbina_Rawson(Coord(np.array([(27.2),(1195.9),241 - z_ground])))
turbina_5 = Turbina_Rawson(Coord(np.array([(-7),(1527),236 - z_ground])))
turbina_6 = Turbina_Rawson(Coord(np.array([(190.3),(1894.2),234 - z_ground])))
turbina_7 = Turbina_Rawson(Coord(np.array([(-78.8),(2222.6),234 - z_ground])))
turbina_8 = Turbina_Rawson(Coord(np.array([(414.8),(2380.9),233 - z_ground])))
turbina_9 = Turbina_Rawson(Coord(np.array([(602.4),(86.7),253 - z_ground])))
turbina_10 = Turbina_Rawson(Coord(np.array([(795.1),(386.7),253 - z_ground])))
turbina_11 = Turbina_Rawson(Coord(np.array([(965.4),(676.2),246 - z_ground])))
turbina_12 = Turbina_Rawson(Coord(np.array([(1043.8),(988.5),239 - z_ground])))
turbina_13 = Turbina_Rawson(Coord(np.array([(1202.3),(1269),235 - z_ground])))
turbina_14 = Turbina_Rawson(Coord(np.array([(1313.8),(1580.7),235 - z_ground])))
turbina_15 = Turbina_Rawson(Coord(np.array([(1362.8),(1919.5),230 - z_ground])))
turbina_16 = Turbina_Rawson(Coord(np.array([(1424.8),(2225.1),223 - z_ground])))
turbina_17 = Turbina_Rawson(Coord(np.array([(711.8),(-766.6),255 - z_ground])))
turbina_18 = Turbina_Rawson(Coord(np.array([(1107.7),(-503.6),250 - z_ground])))
turbina_19 = Turbina_Rawson(Coord(np.array([(1350.9),(-206.8),246 - z_ground])))
turbina_20 = Turbina_Rawson(Coord(np.array([(1705.8),(50.9),239 - z_ground])))
turbina_21 = Turbina_Rawson(Coord(np.array([(1949.7),(315.4),241 - z_ground])))
turbina_22 = Turbina_Rawson(Coord(np.array([(2045.2),(603.6),237 - z_ground])))
turbina_23 = Turbina_Rawson(Coord(np.array([(2256.4),(890.3),234 - z_ground])))
turbina_24 = Turbina_Rawson(Coord(np.array([(2331.4),(1210.7),229 - z_ground])))
turbina_25 = Turbina_Rawson(Coord(np.array([(2451),(1517.1),226 - z_ground])))
turbina_26 = Turbina_Rawson(Coord(np.array([(2548.5),(1800.4),224 - z_ground])))
turbina_27 = Turbina_Rawson(Coord(np.array([(2682.7),(2068.3),223 - z_ground])))
turbina_28 = Turbina_Rawson(Coord(np.array([(2816.2),(2348.8),220 - z_ground])))
turbina_29 = Turbina_Rawson(Coord(np.array([(1946.5),(-1595.2),274 - z_ground])))
turbina_30 = Turbina_Rawson(Coord(np.array([(2201.9),(-1358.8),269 - z_ground])))
turbina_31 = Turbina_Rawson(Coord(np.array([(2357.1),(-1060.7),262 - z_ground])))
turbina_32 = Turbina_Rawson(Coord(np.array([(2500.9),(-787.6),257 - z_ground])))
turbina_33 = Turbina_Rawson(Coord(np.array([(2650.9),(-516.6),251 - z_ground])))
turbina_34 = Turbina_Rawson(Coord(np.array([(2802.7),(-212.6),245 - z_ground])))
turbina_35 = Turbina_Rawson(Coord(np.array([(2909.2),(102.8),241 - z_ground])))
turbina_36 = Turbina_Rawson(Coord(np.array([(2982.2),(372.5),237 - z_ground])))
turbina_37 = Turbina_Rawson(Coord(np.array([(3173.6),(690.7),230 - z_ground])))
turbina_38 = Turbina_Rawson(Coord(np.array([(3283.3),(997.4),224 - z_ground])))
turbina_39 = Turbina_Rawson(Coord(np.array([(3432.1),(1310.3),220 - z_ground])))
turbina_40 = Turbina_Rawson(Coord(np.array([(3562.9),(1629.4),219 - z_ground])))
turbina_41 = Turbina_Rawson(Coord(np.array([(3785.2),(1931.9),214 - z_ground])))
turbina_42 = Turbina_Rawson(Coord(np.array([(3947.6),(2337.7),214 - z_ground])))

turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3, turbina_4, turbina_5,
turbina_6, turbina_7, turbina_8, turbina_9, turbina_10, turbina_11,
turbina_12, turbina_13, turbina_14, turbina_15, turbina_16, turbina_17,
turbina_18, turbina_19, turbina_20, turbina_21, turbina_22, turbina_23,
turbina_24, turbina_25, turbina_26, turbina_27, turbina_28, turbina_29,
turbina_30, turbina_31, turbina_32, turbina_33, turbina_34, turbina_35,
turbina_36, turbina_37, turbina_38, turbina_39, turbina_40, turbina_41,
turbina_42]

# D = 90
#
# turbina_0 = Turbina_Rawson(Coord(np.array([(0),(0),250])))
# turbina_1 = Turbina_Rawson(Coord(np.array([(3*D),(0),250])))
# turbina_2 = Turbina_Rawson(Coord(np.array([(3*D),(4*D),250])))
# turbina_3 = Turbina_Rawson(Coord(np.array([(6*D),(2*D),250])))
#
# turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3]

z_mast = turbina_0.coord.z
# z_0 de la superficie
z_0 = 0.01

parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)
lista_turbinas = turbinas_list
x_o = 10000
y_o = 10000
z_o = 250
coord = Coord(np.array([x_o, y_o, z_o]))

angulos = [0,22.5,45,67.5,90,112.5,135,157.5,180,202.5,225,247.5,270,292.5,315,337.5]

gaussiana = Gaussiana()
frandsen = Frandsen()
jensen = Jensen()
modelo_array = [gaussiana,frandsen,jensen]
metodo_array = ['linear', 'rss', 'largest']
lista_n = np.logspace(1,3,num = 100)

"""Angulos en el eje x"""

# for cantidad_de_puntos in lista_n:
#
#     lista_potencia_modelo_deterministico = []
#     lista_potencia_modelo_montecarlo = []
#     espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
#     lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)
#     for angulo in angulos:
#         parque_de_turbinas.rotar(angulo)
#         calcular_u_en_coord_integral_deterministica(gaussiana, 'rss', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas, lista_dAi_normalizados)
#         aux = sumar_potencia(lista_turbinas)
#         lista_potencia_modelo_deterministico.append(aux)
#         reiniciar_turbinas(lista_turbinas)
#
#         cantidad_de_puntos = int(cantidad_de_puntos)
#         calcular_u_en_coord_integral_de_montecarlo(gaussiana, 'rss', coord, parque_de_turbinas, u_inf, cantidad_de_puntos)
#         aux = sumar_potencia(lista_turbinas)
#         lista_potencia_modelo_montecarlo.append(aux)
#         reiniciar_turbinas(lista_turbinas)
#     plt.plot(angulos, lista_potencia_modelo_deterministico,'o', label = u'Deterministico', linewidth=3)
#     plt.plot(angulos,lista_potencia_modelo_montecarlo,'o', label = u'Montecarlo', linewidth=3)
#     plt.title(cantidad_de_puntos)
#     plt.legend(fontsize = 10, loc = 'center right')
#     plt.xlabel(u'Angulo º ', fontsize=10)
#     plt.ylabel(r'Potencia', fontsize=10)
#     plt.grid()
#     plt.show()


"""Solo int deterministica"""
# for cantidad_de_puntos in lista_n:
#
#     lista_potencia_modelo_deterministico = []
#     espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
#     lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)
#     for angulo in angulos:
#         parque_de_turbinas.rotar(angulo)
#         calcular_u_en_coord_integral_deterministica(gaussiana, 'rss', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas, lista_dAi_normalizados)
#         aux = sumar_potencia(lista_turbinas)
#         lista_potencia_modelo_deterministico.append(aux)
#         reiniciar_turbinas(lista_turbinas)
#     plt.plot(angulos, lista_potencia_modelo_deterministico,'o', label = u'Deterministico', linewidth=3)
#     plt.title(cantidad_de_puntos)
#     plt.legend(fontsize = 10, loc = 'center right')
#     plt.xlabel(u'Angulo º ', fontsize=10)
#     plt.ylabel(r'Potencia', fontsize=10)
#     plt.grid()
#     plt.show()






""" Solo dos angulos. Cantidad de puntos en el eje x """

angulos_reducidos = [30,270]


# for modelo in modelo_array:
#     for metodo in metodo_array:
#         for angulo in angulos_reducidos:
#             parque_de_turbinas.rotar(angulo)
#             lista_potencia_modelo_deterministico = []
#             lista_potencia_modelo_montecarlo = []
#             for cantidad_de_puntos in range(10,1100,100):
#                 espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
#                 lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)
#                 calcular_u_en_coord_integral_deterministica(gaussiana, 'largest', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas, lista_dAi_normalizados)
#                 aux = sumar_potencia(lista_turbinas)
#                 lista_potencia_modelo_deterministico.append(aux)
#                 reiniciar_turbinas(lista_turbinas)
#                 calcular_u_en_coord_integral_de_montecarlo(gaussiana, 'largest', coord, parque_de_turbinas, u_inf, cantidad_de_puntos)
#                 aux = sumar_potencia(lista_turbinas)
#                 lista_potencia_modelo_montecarlo.append(aux)
#                 reiniciar_turbinas(lista_turbinas)
#             puntos = [100,200,300,400,500,600,700,800,900,1000]
#             plt.plot(puntos, lista_potencia_modelo_deterministico, 'o', label = u'Deterministico', linewidth=3)
#             plt.plot(puntos, lista_potencia_modelo_montecarlo, 'o', label=u'Montecarlo', linewidth=3)
#             plt.title([str(modelo), str(metodo), angulo])
#             plt.legend(fontsize=10, loc='lower right')
#             plt.xlabel(u'N', fontsize=10)
#             plt.ylabel(r'Potencia', fontsize=10)
#             plt.grid()
#             plt.show()


""" Solo integral deterministica """

for modelo in modelo_array:
    for metodo in metodo_array:
        for angulo in angulos_reducidos:
            parque_de_turbinas.rotar(angulo)
            lista_potencia_modelo_deterministico = []
            lista_puntos = np.arange(1,200,10)
            for cantidad_de_puntos in lista_puntos:
                espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
                lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)
                calcular_u_en_coord_integral_deterministica(gaussiana, 'largest', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas, lista_dAi_normalizados)
                aux = sumar_potencia(lista_turbinas)
                lista_potencia_modelo_deterministico.append(aux)
                reiniciar_turbinas(lista_turbinas)
            puntos = lista_puntos
            plt.plot(puntos, lista_potencia_modelo_deterministico, 'o', label = u'Deterministico', linewidth=3)
            plt.title([str(modelo), str(metodo), angulo])
            plt.legend(fontsize=10)
            plt.xlabel(u'N', fontsize=10)
            plt.ylabel(r'Potencia', fontsize=10)
            plt.grid()
            plt.show()


