import numpy as np
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
import matplotlib.pyplot as plt

# Carga datos desde archivos .raw y .txt
def cargar_datos(tipo, ruta):
    # Devuelve los datos de posiciones y velocidades del flujo base
    if tipo == 'isosuperficie':
        datos_isosuperficie = np.loadtxt(ruta, skiprows=2)
        x = datos_isosuperficie[:, 0]
        y = datos_isosuperficie[:, 1]
        z = datos_isosuperficie[:, 2]
        u = datos_isosuperficie[:, 3]
        v = datos_isosuperficie[:, 4]
        w = datos_isosuperficie[:, 5]

        return x, y, z, u, v, w


    # Devuelve la lista de turbinas
    elif tipo == 'coordenadas_turbinas':
            coordenadas_turbinas = np.loadtxt(ruta, skiprows=2)
            lista_de_turbinas = []
            for raw in range(len(coordenadas_turbinas[:, 0])):
                turbina = Turbina_Rawson(Coord(coordenadas_turbinas[raw]))
                lista_de_turbinas.append(turbina)
            return lista_de_turbinas


    elif tipo == 'gaussiano':
        datos_Gaussiano = np.loadtxt(ruta, delimiter=',', skiprows=1)
        y = datos_Gaussiano[:, 0]
        u = datos_Gaussiano[:, 1]
        v = datos_Gaussiano[:, 2]
        w = datos_Gaussiano[:, 3]

        return y, u, v, w

# ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
# turbinas_list  = np.loadtxt(ruta, skiprows=2)
# plt.plot(turbinas_list[:,0], turbinas_list[:, 1], 'o')
# plt.show()
#
# turbina_0 = Turbina_Rawson(Coord(np.array([(0),(0),260])))
# turbina_1 = Turbina_Rawson(Coord(np.array([(-204.9),(286.1),269])))
# turbina_2 = Turbina_Rawson(Coord(np.array([(41.9),(565.7),256])))
# turbina_3 = Turbina_Rawson(Coord(np.array([(8.1),(870),247])))
# turbina_4 = Turbina_Rawson(Coord(np.array([(27.2),(1195.9),241])))
# turbina_5 = Turbina_Rawson(Coord(np.array([(-7),(1527),236])))
# turbina_6 = Turbina_Rawson(Coord(np.array([(190.3),(1894.2),234])))
# turbina_7 = Turbina_Rawson(Coord(np.array([(-78.8),(2222.6),234])))
# turbina_8 = Turbina_Rawson(Coord(np.array([(414.8),(2380.9),233])))
# turbina_9 = Turbina_Rawson(Coord(np.array([(602.4),(86.7),253])))
# turbina_10 = Turbina_Rawson(Coord(np.array([(795.1),(386.7),253])))
# turbina_11 = Turbina_Rawson(Coord(np.array([(965.4),(676.2),246])))
# turbina_12 = Turbina_Rawson(Coord(np.array([(1043.8),(988.5),239])))
# turbina_13 = Turbina_Rawson(Coord(np.array([(1202.3),(1269),235])))
# turbina_14 = Turbina_Rawson(Coord(np.array([(1313.8),(1580.7),235])))
# turbina_15 = Turbina_Rawson(Coord(np.array([(1362.8),(1919.5),230])))
# turbina_16 = Turbina_Rawson(Coord(np.array([(1424.8),(2225.1),223])))
# turbina_17 = Turbina_Rawson(Coord(np.array([(711.8),(-766.6),255])))
# turbina_18 = Turbina_Rawson(Coord(np.array([(1107.7),(-503.6),250])))
# turbina_19 = Turbina_Rawson(Coord(np.array([(1350.9),(-206.8),246])))
# turbina_20 = Turbina_Rawson(Coord(np.array([(1705.8),(50.9),239])))
# turbina_21 = Turbina_Rawson(Coord(np.array([(1949.7),(315.4),241])))
# turbina_22 = Turbina_Rawson(Coord(np.array([(2045.2),(603.6),237])))
# turbina_23 = Turbina_Rawson(Coord(np.array([(2256.4),(890.3),234])))
# turbina_24 = Turbina_Rawson(Coord(np.array([(2331.4),(1210.7),229])))
# turbina_25 = Turbina_Rawson(Coord(np.array([(2451),(1517.1),226])))
# turbina_26 = Turbina_Rawson(Coord(np.array([(2548.5),(1800.4),224])))
# turbina_27 = Turbina_Rawson(Coord(np.array([(2682.7),(2068.3),223])))
# turbina_28 = Turbina_Rawson(Coord(np.array([(2816.2),(2348.8),220])))
# turbina_29 = Turbina_Rawson(Coord(np.array([(1946.5),(-1595.2),274])))
# turbina_30 = Turbina_Rawson(Coord(np.array([(2201.9),(-1358.8),269])))
# turbina_31 = Turbina_Rawson(Coord(np.array([(2357.1),(-1060.7),262])))
# turbina_32 = Turbina_Rawson(Coord(np.array([(2500.9),(-787.6),257])))
# turbina_33 = Turbina_Rawson(Coord(np.array([(2650.9),(-516.6),251])))
# turbina_34 = Turbina_Rawson(Coord(np.array([(2802.7),(-212.6),245])))
# turbina_35 = Turbina_Rawson(Coord(np.array([(2909.2),(102.8),241])))
# turbina_36 = Turbina_Rawson(Coord(np.array([(2982.2),(372.5),237])))
# turbina_37 = Turbina_Rawson(Coord(np.array([(3173.6),(690.7),230])))
# turbina_38 = Turbina_Rawson(Coord(np.array([(3283.3),(997.4),224])))
# turbina_39 = Turbina_Rawson(Coord(np.array([(3432.1),(1310.3),220])))
# turbina_40 = Turbina_Rawson(Coord(np.array([(3562.9),(1629.4),219])))
# turbina_41 = Turbina_Rawson(Coord(np.array([(3785.2),(1931.9),214])))
# turbina_42 = Turbina_Rawson(Coord(np.array([(3947.6),(2337.7),214])))
#
# turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3, turbina_4, turbina_5,
# turbina_6, turbina_7, turbina_8, turbina_9, turbina_10, turbina_11,
# turbina_12, turbina_13, turbina_14, turbina_15, turbina_16, turbina_17,
# turbina_18, turbina_19, turbina_20, turbina_21, turbina_22, turbina_23,
# turbina_24, turbina_25, turbina_26, turbina_27, turbina_28, turbina_29,
# turbina_30, turbina_31, turbina_32, turbina_33, turbina_34, turbina_35,
# turbina_36, turbina_37, turbina_38, turbina_39, turbina_40, turbina_41,
# turbina_42]
# for turbina in turbinas_list:
#     plt.plot(turbina.coord.x, turbina.coord.y, 'o')
# plt.show()
#
# ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.Dir.00.00.U8.50.raw"
# xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
# plt.plot(xl, yl, 'o', markersize=0.25)
# plt.show()

