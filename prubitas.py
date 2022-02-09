import numpy as np
from Coord import Coord
from definicion_de_espesor import definicion_de_espesor
import matplotlib.pyplot as plt
from scipy import interpolate
from Jensen import Jensen
from Frandsen import Frandsen
from Gaussiana import Gaussiana
from Turbina_Rawson import Turbina_Rawson
from Iso_Superficie import Iso_Superficie
from load_txt_datos import cargar_datos

"""Grafico de CT con interpolacion 1D"""
# U_tabulado = np.array([3.97553683, 4.9669611, 5.95972269, 6.95196727,
#                             7.95116277, 8.93613964, 9.93634081, 10.92857237,
#                             11.9171516, 12.9245659, 13.91116425, 14.90904084,
#                             15.9053444, 16.88414983, 17.88072698, 18.87876044,
#                             19.87055544, 20.84568607, 21.87016143, 22.8544895,
#                             23.847984, 24.83090363])
# c_T_tabulado = np.array([0.824, 0.791, 0.791, 0.791, 0.732, 0.606, 0.510,
#                               0.433, 0.319, 0.247, 0.196, 0.159, 0.134, 0.115,
#                               0.100, 0.086, 0.074, 0.064, 0.057, 0.050, 0.045, 0.040])
# P_tabulado = np.array([88, 204, 371, 602, 880, 1147, 1405, 1623, 1729, 1761, 1774,
#                             1786, 1795, 1799, 1800, 1800, 1800, 1800, 1800, 1800,
#                             1800, 1800])
# c_P_tabulado = np.array([0.3528756612, 0.4188313302, 0.4407975431, 0.4504238495,
#                               0.4410945765, 0.4037893836, 0.3605747665, 0.3129388419,
#                               0.2567853612, 0.2057066378, 0.1659160941, 0.1358084161,
#                               0.1124665859, 0.093973068, 0.0792089026, 0.0673489313,
#                               0.05774329, 0.049880825, 0.0433833884, 0.0379671505,
#                               0.0334162558, 0.0295645645])
# interpolacion_cT_linear = interpolate.interp1d(U_tabulado, c_T_tabulado, kind='linear', fill_value=(0,0), bounds_error=False)
# interpolacion_cT_zero = interpolate.interp1d(U_tabulado, c_T_tabulado, kind='zero', fill_value=(0,0), bounds_error=False)
# interpolacion_cT_slinear = interpolate.interp1d(U_tabulado, c_T_tabulado, kind='slinear', fill_value=(0,0), bounds_error=False)
# interpolacion_cT_quadratic = interpolate.interp1d(U_tabulado, c_T_tabulado, kind='quadratic', fill_value=(0,0), bounds_error=False)
# interpolacion_cT_cubic = interpolate.interp1d(U_tabulado, c_T_tabulado, kind='cubic', fill_value=(0,0), bounds_error=False)
#
# x = np.arange(0,30,1)
# ylinear = interpolacion_cT_linear(x)
# yzero = interpolacion_cT_linear(x)
# yquadratic = interpolacion_cT_linear(x)
# ycubic = interpolacion_cT_linear(x)
#
#
# plt.plot(x, ylinear,'x', label='linear')
# plt.plot(x, yzero, 'o', label='zero')
# # plt.plot(x, yquadratic, label='quadratic')
# # plt.plot(x, ycubic, label='cubic')
# plt.legend()
# plt.show()
# tck = interpolacion_cT_linear(8.2)
# print(tck)


"""Probando Modelos de deficit"""
# frandsen = Frandsen()
# gaussiana = Gaussiana()
# ct_array = np.linspace(0,1,10)
# turbina = Turbina_Rawson(Coord(np.array([(100),(100),100])))
# coordenada = Coord(np.array([(150),(100),100]))
# deficit_array = np.zeros(len(ct_array))
# i=0
# for CT in ct_array:
#     turbina.c_T = CT
#     deficit_array[i] = gaussiana.evaluar_deficit_normalizado(turbina,coordenada)
#     i += 1
# plt.plot(ct_array,deficit_array)
# plt.show()

# a = np.array([[1, 2], [3, 4]])
# print(a)
# b = np.array([1, 2])
# print(b)
# c = np.dot(a,b)
# print(c)


#
# ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Coordenadas_de_turbinas\Coordenadas_turbinas_parque_Rawson.txt"
# turbinas_list = cargar_datos('coordenadas_turbinas', ruta)
#
# for turbina in turbinas_list:
#     x = float(turbina.coord.x)
#     y = float(turbina.coord.y)
#     plt.plot(x,y, 'o')
#     plt.text(x, y * (1 + 0.01),'x = ' + str(int(x)) + ' y = ' + str(int(y)), fontsize=6)
#
# plt.show()


meshXmin, meshXmax, npoiX = 1000, 4000, 10
meshYmin, meshYmax, npoiY = 1000, 4000, 10
xg = np.linspace(meshXmin, meshXmax, npoiX)
yg = np.linspace(meshYmin, meshYmax, npoiY)
XG, YG = np.meshgrid(xg, yg)
positions = np.vstack([XG.ravel(), YG.ravel()])
coordenadas = []
for i in range(len(positions[0])):
    x = positions[:,i][0]
    y = positions[:,i][1]
    cooord = Coord([x, y, 0])
    coordenadas.append(cooord)
print('hola')