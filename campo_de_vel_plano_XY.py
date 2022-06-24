import matplotlib.pyplot as plt
import numpy as np
from ParqueEolico import ParqueEolico
from Turbina_5MW_NREL import Turbina_5MW_NREL
from Coord import Coord
from U_inf import U_inf
from Gaussiano import Gaussiano
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica
from scipy.interpolate import griddata

d0 = 90


# Carga las turbinas del parque
# turbinas_list  = cargar_datos('coordenadas_turbinas', ruta)
turbina_0 = Turbina_5MW_NREL(Coord(np.array([0, 0, 90])))
turbina_1 = Turbina_5MW_NREL(Coord(np.array([8*d0, 0, 90])))
turbina_2 = Turbina_5MW_NREL(Coord(np.array([16*d0, 0, 90])))
turbina_3 = Turbina_5MW_NREL(Coord(np.array([8*d0, 2*d0, 90])))
turbina_4 = Turbina_5MW_NREL(Coord(np.array([16*d0, 3*d0, 90])))
turbina_5 = Turbina_5MW_NREL(Coord(np.array([0, 5*d0, 90])))

turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3, turbina_4, turbina_5]

gaussiano = Gaussiano()

# Define el tipo de perfil de velocidades cte o log
z_mast, z_0, perfil = turbinas_list[0].coord.z, 0.01, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 12
coord_u = Coord([0,0,z_mast])
u_inf.perfil_flujo_base(coord_u)

parque_de_turbinas = ParqueEolico(turbinas_list, z_0, z_mast)

# Define cantidad de puntos y divide el actuador discal en diferenciales similares
cantidad_de_puntos = 1000
espesor = turbinas_list[0].definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbinas_list[0].coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

# Mallado para calculo de campo de velocidades
meshXmin, meshXmax= -2*d0, 32*d0
meshYmin, meshYmax= -2*d0, 6*d0
rel = (meshYmax-meshYmin)/(meshXmax-meshXmin)
elementos = 1000000
npoiY = int(np.sqrt(elementos*rel))
npoiX = int(npoiY/rel)
xg = np.linspace(meshXmin, meshXmax, npoiX)
yg = np.linspace(meshYmin, meshYmax, npoiY)
XG, YG = np.meshgrid(xg, yg)
positions = np.vstack([XG.ravel(), YG.ravel()])
coordenadas = []
for i in range(len(positions[0])):
    x = positions[:,i][0]
    y = positions[:,i][1]
    cooord = Coord([x, y, 90])
    coordenadas.append(cooord)
# Calcula CT, CP, P de las turbinas
# data_prueba = calcular_potencia_del_parque_con_terreno(gaussiano, 'largest', parque_de_turbinas, u_inf, iso_s, lista_coord_normalizadas,lista_dAi_normalizados)
velocidades = []
for coord in coordenadas:
    velocidades.append(calcular_u_en_coord_integral_deterministica(gaussiano, 'Metodo_C', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados))
# print(velocidades)


# Ploteo
VG = griddata((positions[0], positions[1]), velocidades, (XG, YG), method='cubic')

fig1 = plt.figure()
ax = fig1.add_subplot(1, 1, 1)
levels_ctf = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
levels_ct = [2, 4, 6, 8, 10]
line_colors = ['black' for l in levels_ct]
CFS = ax.contourf(XG/d0, YG/d0, VG, levels_ctf, cmap='jet')
CS = ax.contour(XG/d0, YG/d0, VG, levels=levels_ct, colors=line_colors)
ax.clabel(CS, fontsize=10, colors=line_colors)
ax.set_xticks(np.arange(-2, 34, 2))
ax.set_yticks(np.arange(-2, 7, 1))
ax.set_xlabel('x/d')
ax.set_ylabel('y/d')
fig1.colorbar(CFS)
plt.tight_layout()
plt.savefig('Imagen_Ale_XY_escalas_dif')
plt.show()

fig2 = plt.figure()
ax = fig2.add_subplot(1, 1, 1)
CFS = ax.contourf(XG/d0, YG/d0, VG, levels_ctf, cmap='jet')
ax.set_xticks(np.arange(-2, 34, 2))
ax.set_yticks(np.arange(-2, 7, 1))
ax.set_xlabel('x/d')
ax.set_ylabel('y/d')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig('Imagen_Ale_XY_escalas_iguales')
plt.show()