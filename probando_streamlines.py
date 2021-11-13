import numpy as np
from scipy.interpolate import interp2d
from scipy.interpolate import LinearNDInterpolator
from Iso_Superficie import Iso_Superficie
from load_txt_datos import cargar_datos
import matplotlib.pyplot as plt
from Coord import Coord

"""Con datos de CFD"""
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas(1).raw"
xl, yl, zl, ul, vl, wl = cargar_datos('isosuperficie', ruta)
#Las operaciones de abajo no hacen nada, xl etc ya son np.arrays
x = np.array(xl)
y = np.array(yl)
z = np.array(zl)
u = np.array(ul)
v = np.array(vl)
w = np.array(wl)
coord_turbina1 = Coord(np.array([400, 400, 260]))
coord_turbina2 = Coord(np.array([500, 500, 260]))
coord_turbina3 = Coord(np.array([10, 10, 260]))




"""Con una funcion simple que podemos ver los resultados aca: https://www.desmos.com/calculator/eijhparfmd"""
# x = np.linspace(-10,100,100)
# y = np.linspace(-10,100,100)
# xx,yy = np.meshgrid(x,y)
# # Los ordeno de forma tal que sean similares a los vectores que paso con los datos de CFD
# out = np.column_stack((xx.ravel('F'), yy.ravel('F') ))
# xc = np.array(out[:,0])
# yc = np.array(out[:,1])
# x = xc.T
# y = yc.T
# u, v = y, -x+y
# coord_turbina1 = Coord(np.array([0, 0, 260]))
# coord_turbina2 = Coord(np.array([0, 50, 260]))
# coord_turbina3 = Coord(np.array([10, 10, 260]))

"""Con la funcion del windmap"""
# x = np.linspace(-10,100,100)
# y = np.linspace(-10,100,100)
# xx,yy = np.meshgrid(x,y)
# # Graficamos con streamplot de matplotlib
# uu, vv = 1 + xx**2 - y, -1 - xx + xx*yy**2
# plt.streamplot(xx,yy,uu,vv)
# plt.show()
#
# # Los ordeno de forma tal que sean similares a los vectores que paso con los datos de CFD
# out = np.column_stack((xx.ravel('F'), yy.ravel('F') ))
# xc = np.array(out[:,0])
# yc = np.array(out[:,1])
# x = xc.T
# y = yc.T
# u, v = 1 + x**2 - y, -1 - x + x*y**2
# coord_turbina1 = Coord(np.array([10, 10, 260]))
# coord_turbina2 = Coord(np.array([0, 0, 260]))
# coord_turbina3 = Coord(np.array([20, 20, 260]))



# Prueba
iso_superficie = Iso_Superficie(x, y, z, u, v, w)
x_s1, y_s1 = iso_superficie.streamline_in_coord(coord_turbina1)
x_s2, y_s2 = iso_superficie.streamline_in_coord(coord_turbina2)
x_s3, y_s3 = iso_superficie.streamline_in_coord(coord_turbina3)

x_s1 = np.array(x_s1)
y_s1 = np.array(y_s1)
desplazamiento_vertical = iso_superficie.desplazamiento_vertical(x_s1, y_s1)
longitud_ldc = iso_superficie.longitud_streamline(x_s1, y_s1)
print(desplazamiento_vertical, longitud_ldc)

# Ploteo
plt.plot(x_s1,y_s1)
plt.plot(x_s2,y_s2)
plt.plot(x_s3,y_s3)
plt.show()
