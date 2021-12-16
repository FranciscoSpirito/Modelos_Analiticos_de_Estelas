import numpy as np
from scipy.interpolate import interp2d
from scipy.interpolate import LinearNDInterpolator
from Iso_Superficie import Iso_Superficie
from load_txt_datos import cargar_datos
import matplotlib.pyplot as plt
from Coord import Coord
from mpl_toolkits.axes_grid1 import make_axes_locatable



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
# nstream = 20 # cantidad de streamlines
# meshXmin, meshXmax = 1000, 5500
# meshYmin, meshYmax = 500, 5000
# x0 = np.linspace(meshXmax, meshXmin, nstream)
# y0 = np.linspace(meshYmin, meshYmax, nstream)
# dr = 500
# streamlines = [iso_s._makeStreamline(*xy, dr) for xy in zip(x0, y0)]



# # Ploteo
# fig1 = plt.figure()
# ax = fig1.add_subplot(1, 1, 1)
#
# count = ax.contourf(iso_s.XG, iso_s.YG, iso_s.ZG, 10)
# # ax.plot(*streamline, '.')
#
# for line in streamlines:
#     ax.plot(line[0], line[1], '.r')
#
# item = streamlines[8]
# ax.plot(item[0], item[1], '.b')
#
# ax.streamplot(iso_s.XG, iso_s.YG, iso_s.UG, iso_s.VG, color='k', linewidth=.5)
# fig1.colorbar(count)
# ax.set_aspect('equal', 'box')
#
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(1, 1, 1)
#
#
# # Para 1ra funcion mostramos la diferenciad de acumulado y sin acumular
# ax2.plot(item[1], item[3], 'r')
# z_iso = []
# for x, y in zip(item[0], item[1]):
#     z_iso.append(iso_s._interp_z(x, y).item())
# ax2.plot(item[1], z_iso)
# plt.show()
#
# x = np.linspace(1500,2500,20)
# y = np.linspace(1998,2001,20)
# iso_s.interpoladoresSZT(streamlines)
# t = iso_s._interp_t(x,y)
# print(t)


# iso_s = Iso_Superficie(x, y, z, u, v, w)
# nstream = 20 # cantidad de streamlines
# angulos = [0, 45, 90, 135, 180, 225, 270, 315]
# for angulo in angulos:
#     x0, y0 = iso_s.gen_semillas(angulo,nstream)
#     plt.title(angulo)
#     plt.plot(x0, y0)
#     plt.show()




# fig1, axes1 = plt.subplots(1, 2)
# iso_s = Iso_Superficie(x, y, z, u, v, w)
# angulo = 67.5
# nstream = 20 # cantidad de streamlines
# iso_s.new_grid(100)
# x0, y0 = iso_s.gen_semillas(angulo, nstream)
# axes1[1].plot(x0, y0, 'o')
# dr = 250
# streamlines = [iso_s._makeStreamline(*xy, dr) for xy in zip(x0, y0)]
# axes1[0].contourf(iso_s.XG, iso_s.YG, iso_s.ZG, 10)
# for line in streamlines:
#     axes1[0].plot(line[0], line[1], '.r')
# line = streamlines[7]
# axes1[0].plot(line[0][0], line[1][0], '.y')
# axes1[0].plot(line[0][len(line[1])-1], line[1][len(line[1])-1], '.k')
# axes1[0].streamplot(iso_s.XG, iso_s.YG, iso_s.UG, iso_s.VG, color='k', linewidth=.5)
#
#
# streamlines1 = iso_s.rotar(angulo, streamlines)
# fig2, axes2 = plt.subplots(1, 2)
# axes2[1] = plt.plot(x0, y0, 'o')
# dr = 250
# for line1 in streamlines1:
#     axes2[0].plot(line1[0], line1[1], '.r')
# line1 = streamlines1[7]
# axes2[0].plot(line1[0][0], line1[1][0], '.y')
# axes2[0].plot(line1[0][len(line1[1])-1], line1[1][len(line1[1])-1], '.k')
# plt.show()

# angulos = [0, 22.5, 90, 135, 180, 225, 270, 315]
# for angulo in angulos:
#     x_semillas, y_semillas = iso_s.gen_semillas(angulo, 20)
#     streamlines = iso_s._makeStreamline(angulo, x_semillas, y_semillas, 250)
#     plt.plot(streamlines[i][0], streamlines[i][1])
#     plt.title(angulo)
#     i += 1
#     plt.show()

    # for i in range(len(x_semillas)):
    #     x = x_semillas[i]
    #     y = y_semillas[i]
    #     plt.plot(x, y, 'bo')
    #     plt.text(x * (1 + 0.01), y * (1 + 0.01), i, fontsize=12)
    # plt.title("angulo = " + str(angulo))
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.xlim(iso_s.meshXmin-100, iso_s.meshXmax+100)
    # plt.ylim(iso_s.meshYmin-100, iso_s.meshYmax+100)
    # plt.show()

"""Con datos de CFD"""
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
for iso_s, angulo in zip(isoSuperficies, angulos):
     fig, axes = plt.subplots(2,2)
     fig.suptitle('angulo = '+ str(angulo))
     iso_s.new_grid(200)
     x_semillas, y_semillas = iso_s.gen_semillas(angulo, 20)

     axes[0,0].plot(x_semillas, y_semillas, 'o')
     axes[0,0].set_title('Semillas')
     axes[0,0].set_xlim(iso_s.meshXmin-100, iso_s.meshXmax+100)
     axes[0,0].set_ylim(iso_s.meshYmin-100, iso_s.meshYmax+100)

     streamlines = iso_s._makeStreamline(x_semillas, y_semillas, 50, angulo)
     for line in streamlines:
          axes[0,1].plot(line[0], line[1], '.r')
     axes[0,1].set_title('Streamlines')
     line_prueba = streamlines[2]
     axes[0,1].plot(line_prueba[0][3], line_prueba[1][3], 'y')
     axes[0,1].plot(line_prueba[0][len(line_prueba[0])-3], line_prueba[1][len(line_prueba[0])-3], 'k')

     iso_s.redef_interpoladores(streamlines)
     count = axes[1,0].contourf(iso_s.XG, iso_s.YG, iso_s.SG, 10)
     axes[1,0].set_title('S')
     divider = make_axes_locatable(axes[1,0])
     cax = divider.append_axes('right', size='5%', pad=0.05)
     fig.colorbar(count, cax=cax, orientation='vertical')

     count = axes[1,1].contourf(iso_s.XG, iso_s.YG, iso_s.TG, 10)
     axes[1,1].set_title('T')
     axes[1,1].get_yaxis().set_visible(False)
     divider = make_axes_locatable(axes[1,1])
     cax = divider.append_axes('right', size='5%', pad=0.05)
     fig.colorbar(count, cax=cax, orientation='vertical')
     plt.show()

