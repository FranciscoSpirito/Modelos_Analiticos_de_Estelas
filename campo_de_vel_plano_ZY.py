import matplotlib.pyplot as plt
import numpy as np
from ParqueEolico import ParqueEolico
from Turbina_5MW_NREL import Turbina_5MW_NREL
from Coord import Coord
from U_inf import U_inf
from Gaussiano import Gaussiano
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica
from scipy.interpolate import griddata


# Modelo analitico
gaussiana = Gaussiano()

# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_5MW_NREL(Coord(np.array([0,0,90])))
d0 = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_5MW_NREL(Coord(np.array([8*d0,0,90])))
turbina_parcialmente_alineada1 = Turbina_5MW_NREL(Coord(np.array([8*d0,0.5*d0,90])))
turbina_parcialmente_alineada2 = Turbina_5MW_NREL(Coord(np.array([8*d0,1*d0,90])))
turbina_desalineada = Turbina_5MW_NREL(Coord(np.array([8*d0,1.75*d0,90])))

# Diferenciacion del actuador discal
cantidad_de_puntos = 5
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

# Define el tipo de perfil de velocidades cte o log
z_mast, z_0, perfil = turbina_0.coord.z, 0.01, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 12
coord_u = Coord([0,0,z_mast])
u_inf.perfil_flujo_base(coord_u)

# Armado de mallados para los 4 casos.
listaMax = [2, 2, 2, 2.5, 3.5]
# Distancia entre nodos buscada 0.46 m
listaElementos = [750000, 750000, 750000, 850000, 1000000]
listaCoord = []
listaCoordYZ = []
listaMallas = []
for max, elementos in zip(listaMax, listaElementos):
    meshZmin, meshZmax = 90-1.25*d0, 90+1.25*d0
    meshYmin, meshYmax = -2*d0, max*d0
    rel = (meshYmax-meshYmin)/(meshZmax-meshZmin)
    npoiY = int(np.sqrt(elementos*rel))
    npoiZ = int(npoiY/rel)
    zg = np.linspace(meshZmin, meshZmax, npoiZ)
    yg = np.linspace(meshYmin, meshYmax, npoiY)
    print((meshYmax-meshYmin)/npoiY, (meshZmax-meshZmin)/npoiZ)
    YG, ZG = np.meshgrid(yg, zg)
    positions = np.vstack([YG.ravel(), ZG.ravel()])
    x = 16 * d0
    caso_coord = []
    for i in range(len(positions[0])):
        y = positions[:, i][0]
        z = positions[:, i][1]
        coord = Coord([x, y, z])
        caso_coord.append(coord)
    listaCoord.append(caso_coord)
    listaCoordYZ.append(positions)
    listaMallas.append([YG, ZG])

# Obtencion de datos de Modelos Analiticos
listasTurbinas = [[turbina_0], [turbina_0, turbina_alineada],[turbina_0, turbina_parcialmente_alineada1], [turbina_0, turbina_parcialmente_alineada2], [turbina_0, turbina_desalineada]]
datos_MA = []
for listaTurbinas, coordenadas in zip(listasTurbinas, listaCoord):
    parque_de_turbinas = ParqueEolico(listaTurbinas, z_0, z_mast)
    velocidades = []
    for coord in coordenadas:
        velocidades.append(calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados))
    datos_MA.append(velocidades)

# Obtencion de datos de CFD
casos = ['0', '1', '2', '3', '4']
datos_CFD = []
for caso in casos:
    ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Superficies\Caso0\surfaces\U_Estela_16D_superficie.raw"
    l_ruta = list(ruta)
    l_ruta[129] = caso
    ruta = "".join(l_ruta)
    pos_vel_CFD = np.loadtxt(ruta, delimiter=' ', skiprows=2)
    y = pos_vel_CFD[:, 1]
    z = pos_vel_CFD[:, 2]
    u = pos_vel_CFD[:, 3]
    dato = [y, z, u]
    datos_CFD.append(dato)


# PLOTEO

# La escala de colores sera la misma para todas las imagenes
levels_ctf = np.linspace(6, 13, 15)
levels_ct = [6, 7, 8, 9, 10, 10.5, 11, 11.5, 12]

# CASO 0

figure, axis = plt.subplots(nrows=1, ncols=2)
figure.set_figheight(4)
figure.set_figwidth(12)
y, z, vel_MA = listaCoordYZ[0][0], listaCoordYZ[0][1], np.array(datos_MA[0])
YG, ZG = listaMallas[0][0], listaMallas[0][1]
# Malla de velocidades para countourf
UG = griddata((y, z), vel_MA, (YG, ZG), method='cubic')
CFS = axis[0].contourf(YG/d0, (ZG-90)/d0, UG, levels_ctf, cmap='jet')
line_colors = ['black' for l in levels_ct]
CS = axis[0].contour(YG/d0, (ZG-90)/d0, UG, levels=levels_ct, colors=line_colors)
axis[0].clabel(CS, fontsize=10, colors=line_colors)
axis[0].set_xticks(np.arange(-2, 2.5, 0.5))
axis[0].set_yticks(np.arange(-1.25, 1.26, 0.25))
figure.colorbar(CFS, ax=axis[0])
axis[0].set_xlabel('y/d')
axis[0].set_ylabel('z/d')
# CFD
y_sort = np.sort(datos_CFD[0][0])
z_sort = np.sort(datos_CFD[0][1])
YG, ZG = np.meshgrid(y_sort, z_sort)
UG = griddata((datos_CFD[0][0], datos_CFD[0][1]), datos_CFD[0][2], (YG, ZG), method='cubic')
YGnorm, ZGnorm, UG = (YG[3141:6901, 2092:8060]-567)/d0, (ZG[3141:6901, 2092:8060]-567)/d0, UG[3141:6901, 2092:8060]
CFS = axis[1].contourf(YGnorm, ZGnorm, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[1].contour(YGnorm, ZGnorm, UG, levels=levels_ct, colors=line_colors)
axis[1].clabel(CS, fontsize=10, colors=line_colors)
axis[1].set_xticks(np.arange(-2, 2.5, 0.5))
axis[1].set_yticks(np.arange(-1.25, 1.26, 0.25))
axis[1].set_xlabel('y/d')
axis[1].set_ylabel('z/d')
figure.colorbar(CFS, ax=axis[1])
figure.suptitle('Caso 0')
plt.tight_layout()
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Planos ZY\PlanoZY_Caso_0')
plt.show()

# CASO 1

figure, axis = plt.subplots(nrows=1, ncols=2)
figure.set_figheight(4)
figure.set_figwidth(12)
y, z, vel_MA = listaCoordYZ[1][0], listaCoordYZ[1][1], np.array(datos_MA[1])
YG, ZG = listaMallas[1][0], listaMallas[1][1]
# Malla de velocidades para countourf
UG = griddata((y, z), vel_MA, (YG, ZG), method='cubic')
CFS = axis[0].contourf(YG/d0, (ZG-90)/d0, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[0].contour(YG/d0, (ZG-90)/d0, UG, levels=levels_ct, colors=line_colors)
axis[0].clabel(CS, fontsize=10, colors=line_colors)
axis[0].set_xticks(np.arange(-2, 2.5, 0.5))
axis[0].set_yticks(np.arange(-1.25, 1.26, 0.25))
figure.colorbar(CFS, ax=axis[0])
axis[0].set_xlabel('y/d')
axis[0].set_ylabel('z/d')
# CFD
y_sort = np.sort(datos_CFD[1][0])
z_sort = np.sort(datos_CFD[1][1])
YG, ZG = np.meshgrid(y_sort, z_sort)
UG = griddata((datos_CFD[1][0], datos_CFD[1][1]), datos_CFD[1][2], (YG, ZG), method='cubic')
YGnorm, ZGnorm, UG = (YG[3141:6901, 2092:8060]-567)/d0, (ZG[3141:6901, 2092:8060]-567)/d0, UG[3141:6901, 2092:8060]
CFS = axis[1].contourf(YGnorm, ZGnorm, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[1].contour(YGnorm, ZGnorm, UG, levels=levels_ct, colors=line_colors)
axis[1].clabel(CS, fontsize=10, colors=line_colors)
axis[1].set_xticks(np.arange(-2, 2.5, 0.5))
axis[1].set_yticks(np.arange(-1.25, 1.26, 0.25))
axis[1].set_xlabel('y/d')
axis[1].set_ylabel('z/d')
figure.colorbar(CFS, ax=axis[1])
figure.suptitle('Caso 1')
plt.tight_layout()
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Planos ZY\PlanoZY_Caso_1')
plt.show()


# CASO 2

figure, axis = plt.subplots(nrows=1, ncols=2)
figure.set_figheight(4)
figure.set_figwidth(12)
y, z, vel_MA = listaCoordYZ[2][0], listaCoordYZ[2][1], np.array(datos_MA[2])
YG, ZG = listaMallas[2][0], listaMallas[2][1]
# Malla de velocidades para countourf
UG = griddata((y, z), vel_MA, (YG, ZG), method='cubic')
CFS = axis[0].contourf(YG/d0, (ZG-90)/d0, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[0].contour(YG/d0, (ZG-90)/d0, UG, levels=levels_ct, colors=line_colors)
axis[0].clabel(CS, fontsize=10, colors=line_colors)
axis[0].set_xticks(np.arange(-2, 2.5, 0.5))
axis[0].set_yticks(np.arange(-1.25, 1.26, 0.25))
figure.colorbar(CFS, ax=axis[0])
axis[0].set_xlabel('y/d')
axis[0].set_ylabel('z/d')
# CFD
y_sort = np.sort(datos_CFD[2][0])
z_sort = np.sort(datos_CFD[2][1])
YG, ZG = np.meshgrid(y_sort, z_sort)
UG = griddata((datos_CFD[2][0], datos_CFD[2][1]), datos_CFD[2][2], (YG, ZG), method='cubic')
YGnorm, ZGnorm, UG = (YG[3141:6901, 2092:8060]-567)/d0, (ZG[3141:6901, 2092:8060]-567)/d0, UG[3141:6901, 2092:8060]
CFS = axis[1].contourf(YGnorm, ZGnorm, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[1].contour(YGnorm, ZGnorm, UG, levels=levels_ct, colors=line_colors)
axis[1].clabel(CS, fontsize=10, colors=line_colors)
axis[1].set_xticks(np.arange(-2, 2.5, 0.5))
axis[1].set_yticks(np.arange(-1.25, 1.26, 0.25))
axis[1].set_xlabel('y/d')
axis[1].set_ylabel('z/d')
figure.colorbar(CFS, ax=axis[1])
figure.suptitle('Caso 2')
plt.tight_layout()
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Planos ZY\PlanoZY_Caso_2')
plt.show()

# CASO 3

figure, axis = plt.subplots(nrows=1, ncols=2)
figure.set_figheight(4)
figure.set_figwidth(12)
y, z, vel_MA = listaCoordYZ[3][0], listaCoordYZ[3][1], np.array(datos_MA[3])
YG, ZG = listaMallas[3][0], listaMallas[3][1]
# Malla de velocidades para countourf
UG = griddata((y, z), vel_MA, (YG, ZG), method='cubic')
CFS = axis[0].contourf(YG/d0, (ZG-90)/d0, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[0].contour(YG/d0, (ZG-90)/d0, UG, levels=levels_ct, colors=line_colors)
axis[0].clabel(CS, fontsize=10, colors=line_colors)
axis[0].set_xticks(np.arange(-2, 3, 0.5))
axis[0].set_yticks(np.arange(-1.25, 1.26, 0.25))
figure.colorbar(CFS, ax=axis[0])
axis[0].set_xlabel('y/d')
axis[0].set_ylabel('z/d')
# CFD
y_sort = np.sort(datos_CFD[3][0])
z_sort = np.sort(datos_CFD[3][1])
YG, ZG = np.meshgrid(y_sort, z_sort)
UG = griddata((datos_CFD[3][0], datos_CFD[3][1]), datos_CFD[3][2], (YG, ZG), method='cubic')
YGnorm, ZGnorm, UG = (YG[3141:6901, 2092:8481]-567)/d0, (ZG[3141:6901, 2092:8481]-567)/d0, UG[3141:6901, 2092:8481]
CFS = axis[1].contourf(YGnorm, ZGnorm, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[1].contour(YGnorm, ZGnorm, UG, levels=levels_ct, colors=line_colors)
axis[1].clabel(CS, fontsize=10, colors=line_colors)
axis[1].set_xticks(np.arange(-2, 3, 0.5))
axis[1].set_yticks(np.arange(-1.25, 1.26, 0.25))
axis[1].set_xlabel('y/d')
axis[1].set_ylabel('z/d')
figure.colorbar(CFS, ax=axis[1])
figure.suptitle('Caso 3')
plt.tight_layout()
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Planos ZY\PlanoZY_Caso_3')
plt.show()

# CASO 4

figure, axis = plt.subplots(nrows=1, ncols=2)
figure.set_figheight(4)
figure.set_figwidth(12)
y, z, vel_MA = listaCoordYZ[4][0], listaCoordYZ[4][1], np.array(datos_MA[4])
YG, ZG = listaMallas[4][0], listaMallas[4][1]
# Malla de velocidades para countourf
UG = griddata((y, z), vel_MA, (YG, ZG), method='cubic')
CFS = axis[0].contourf(YG/d0, (ZG-90)/d0, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[0].contour(YG/d0, (ZG-90)/d0, UG, levels=levels_ct, colors=line_colors)
axis[0].clabel(CS, fontsize=10, colors=line_colors)
axis[0].set_xticks(np.arange(-2, 4, 0.5))
axis[0].set_yticks(np.arange(-1.25, 1.26, 0.25))
figure.colorbar(CFS, ax=axis[0])
axis[0].set_xlabel('y/d')
axis[0].set_ylabel('z/d')
# CFD
y_sort = np.sort(datos_CFD[4][0])
z_sort = np.sort(datos_CFD[4][1])
YG, ZG = np.meshgrid(y_sort, z_sort)
UG = griddata((datos_CFD[4][0], datos_CFD[4][1]), datos_CFD[4][2], (YG, ZG), method='cubic')
YGnorm, ZGnorm, UG = (YG[3141:6901, 2092:9307]-567)/d0, (ZG[3141:6901, 2092:9307]-567)/d0, UG[3141:6901, 2092:9307]
CFS = axis[1].contourf(YGnorm, ZGnorm, UG, levels_ctf, cmap='jet')
# Set all level lines to black
line_colors = ['black' for l in levels_ct]
CS = axis[1].contour(YGnorm, ZGnorm, UG, levels=levels_ct, colors=line_colors)
axis[1].clabel(CS, fontsize=10, colors=line_colors)
axis[1].set_xticks(np.arange(-2, 4, 0.5))
axis[1].set_yticks(np.arange(-1.25, 1.26, 0.25))
axis[1].set_xlabel('y/d')
axis[1].set_ylabel('z/d')
figure.colorbar(CFS, ax=axis[1])
figure.suptitle('Caso 4')
plt.tight_layout()
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Planos ZY\PlanoZY_Caso_4')
plt.show()
