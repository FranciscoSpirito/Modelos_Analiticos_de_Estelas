import numpy as np
import matplotlib.pyplot as plt
from Gaussiano import Gaussiano
from ParqueEolico import ParqueEolico
from Turbina_5MW_NREL import Turbina_5MW_NREL
from Coord import Coord
from load_txt_datos import cargar_datos
from U_inf import U_inf
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica

"""
casos de la prueba segun paper: "Limitations to the validity of single wake
superposition in wind farm yield assessment"

Tenemos dos turbinas alineadas separadas por 8D
A continuacion se grafica:
    1) El deficit a la altura del hub para dos turbinas alineadas a 16D por
    atras de la primera (8D del segundo) usando CFD (OpenFOAM).
    2) El deficit de las dos turbinas trabajando independientemente (a 16D de
    la primera turbina y a 8D de la segunda turbina)
    3) El deficit generado por ambas (a 16D de la primera turbina) utilizando
    distintos metodos de superposicion de estelas
"""

# Modelo analitico
gaussiana = Gaussiano()

# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_5MW_NREL(Coord(np.array([0,0,90])))
D = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_5MW_NREL(Coord(np.array([8*D,0,90])))
turbina_parcialmente_alineada1 = Turbina_5MW_NREL(Coord(np.array([8*D,0.5*D,90])))
turbina_parcialmente_alineada2 = Turbina_5MW_NREL(Coord(np.array([8*D,1*D,90])))
turbina_desalineada = Turbina_5MW_NREL(Coord(np.array([8*D,1.75*D,90])))

# Diferenciacion del actuador discal
cantidad_de_puntos = 5
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

# Definicion de velocidad de entrada
z_0, z_mast, perfil = 0.01, 90, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 12
coord_u = Coord([0,0,z_mast])
u_inf.perfil_flujo_base(coord_u)

# METODOS DE SUPERPOSICION
metodos_sup = ['Metodo_A', 'Metodo_B', 'Metodo_C', 'Metodo_D', 'Metodo_E', 'Metodo_F', 'Metodo_G']
# CASOS
parque_de_turbinas_primera_indep = ParqueEolico([turbina_0], z_0, z_mast)
parque_de_turbinas_segunda_indep = ParqueEolico([turbina_alineada], z_0, z_mast)
parque_de_turbinas_alineadas = ParqueEolico([turbina_0, turbina_alineada], z_0, z_mast)
parque_de_turbinas_parc_alineadas1 = ParqueEolico([turbina_0, turbina_parcialmente_alineada1], z_0, z_mast)
parque_de_turbinas_parc_alineadas2 = ParqueEolico([turbina_0, turbina_parcialmente_alineada2], z_0, z_mast)
parque_de_turbinas_desalineadas = ParqueEolico([turbina_0, turbina_desalineada], z_0, z_mast)
casos_ss = [parque_de_turbinas_primera_indep, parque_de_turbinas_segunda_indep]
casos_cs = [parque_de_turbinas_alineadas, parque_de_turbinas_parc_alineadas1, parque_de_turbinas_parc_alineadas2, parque_de_turbinas_desalineadas]
# calculo el deficit a 16D para la primera turbina independiente
x_0 = 16*D
step = 2
y = np.arange(-2*D, 3*D, step)
z_o = turbina_0.coord.z
datos = []
for caso in casos_ss:
    datos_i = np.zeros(len(y))
    for i in range(len(y)):
        coord = Coord(np.array([x_0, y[i], z_o]))
        datos_i[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                                                      caso,
                                                                                      u_inf,
                                                                                      lista_coord_normalizadas,
                                                                                      lista_dAi_normalizados)
    datos.append(datos_i)
    for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_parcialmente_alineada2, turbina_desalineada]:
        turbina.reiniciar_turbina()
for caso in casos_cs:
    for metodo_sup in metodos_sup:
        datos_i = np.zeros(len(y))
        for i in range(len(y)):
            coord = Coord(np.array([x_0, y[i], z_o]))
            datos_i[i] = calcular_u_en_coord_integral_deterministica(gaussiana, metodo_sup, coord,
                                                                                          caso,
                                                                                          u_inf,
                                                                                          lista_coord_normalizadas,
                                                                                          lista_dAi_normalizados)
        datos.append(datos_i)
        for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_parcialmente_alineada2, turbina_desalineada]:
            turbina.reiniciar_turbina()

# Normalizamos
datos_norm = []
for vel in datos:
    vel = (u_inf.u_perfil - vel)/u_inf.u_perfil
    datos_norm.append(vel)

# GRAFICOS

# Obtencion de datos de CFD
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso0\Estela_16D_U.csv"
ycfd, ucfd, vcfd, wcfd = cargar_datos('gaussiano', ruta)
ycfd = ycfd - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso1\Estela_16D_U.csv"
yali, uali, vali, wali = cargar_datos('gaussiano', ruta)
yali = yali - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso2\Estela_16D_U.csv"
ypar1, upar1, vpar1, wpar1 = cargar_datos('gaussiano', ruta)
ypar1 = ypar1 - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso3\Estela_16D_U.csv"
ypar2, upar2, vpar2, wpar2 = cargar_datos('gaussiano', ruta)
ypar2 = ypar2 - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso4\Estela_16D_U.csv"
ydes, udes, vdes, wdes = cargar_datos('gaussiano', ruta)
ydes = ydes - 567
# Normalizamos
ucfd_n = (u_inf.u_perfil - ucfd)/u_inf.u_perfil
uali_n = (u_inf.u_perfil - uali)/u_inf.u_perfil
upar1_n = (u_inf.u_perfil - upar1)/u_inf.u_perfil
upar2_n = (u_inf.u_perfil - upar2)/u_inf.u_perfil
udes_n = (u_inf.u_perfil - udes)/u_inf.u_perfil

# Turbina Independiente
plt.plot(ycfd[125:375]/D, ucfd_n[125:375], '.', markersize=1, label='CFD')
plt.plot(y[0:252]/D, datos_norm[0][0:252], label='Modelo Gaussiano')
plt.legend(loc='upper right', fontsize=10, markerscale=5)
plt.title('Caso 0, x = 16d')
plt.grid()
plt.yticks(np.arange(0, 0.2, 0.01))
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
plt.show()

# Turbinas alineadas deficit sin superposicion
plt.plot(y[0:252]/D, datos_norm[0][0:252], label='Turbina 0')
plt.plot(y[0:252]/D, datos_norm[1][0:252], label='Turbina 1')
plt.legend(loc='upper right', fontsize=10, markerscale=5)
plt.title('Turbina 0 y Turbina 1 sin superposición, x = 16 d')
plt.grid()
plt.yticks(np.arange(0, 0.26, 0.02))
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
plt.show()

nposcfd = len(yali)
npos = len(y[0:252])
# Turbinas alineadas
plt.plot(yali[125:375]/D, uali_n[125:375], '.', markersize=1, label='CFD')
plt.plot(y[0:252]/D, datos_norm[2][0:252],label='Método A')
plt.plot(y[0:252]/D, datos_norm[3][0:252], label='Método B')
plt.plot(y[0:252]/D, datos_norm[4][0:252], label='Método C')
plt.plot(y[0:252]/D, datos_norm[5][0:252], label='Método D')
plt.plot(y[0:252]/D, datos_norm[6][0:252], label='Método E')
plt.plot(y[0:252]/D, datos_norm[7][0:252], label='Método F')
plt.plot(y[0:252]/D, datos_norm[8][0:252], label='Método G')
plt.annotate('CFD', xy=(yali[int(nposcfd/2)]/D, uali_n[int(nposcfd/2)]), xycoords='data', xytext=(1, 0.35), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método A', xy=(y[int(npos/2.3)]/D, datos_norm[2][int(npos/2.3)]), xycoords='data', xytext=(-1.5, 0.3), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método B', xy=(y[int(npos/2)]/D, datos_norm[3][int(npos/2)]), xycoords='data', xytext=(1, 0.5), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método C', xy=(y[int(npos/2)]/D, datos_norm[4][int(npos/2)]), xycoords='data', xytext=(-1.5, 0.4), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método D', xy=(y[int(npos/2)]/D, datos_norm[5][int(npos/2)]), xycoords='data', xytext=(1, 0.4), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método E', xy=(y[int(npos/2)]/D, datos_norm[6][int(npos/2)]), xycoords='data', xytext=(1, 0.45), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método F', xy=(y[int(npos/2.2)]/D, datos_norm[7][int(npos/2.2)]), xycoords='data', xytext=(-1.5, 0.5), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método G', xy=(y[int(npos/2)]/D, datos_norm[8][int(npos/2)]), xycoords='data', xytext=(-1.5, 0.55), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
# plt.legend(loc='lower right', fontsize=10)
plt.grid()
plt.yticks(np.arange(0, 0.6, 0.05))
plt.title('Caso 1')
plt.xlabel('y/d')
plt.ylabel('Δu/$u_oo$')
plt.show()

# Turbinas Parcialmente Alineadas 1
nposcfd = len(yali)
npos = len(y)
plt.plot(ypar1[125:375]/D, upar1_n[125:375], '.', label='CFD', markersize=1)
plt.plot(y[0:252]/D, datos_norm[10][0:252], label='Método B')
plt.plot(y[0:252]/D, datos_norm[12][0:252], label='Método D')
plt.plot(y[0:252]/D, datos_norm[13][0:252], label='Método E')
plt.grid()
plt.yticks(np.arange(0, 0.4, 0.02))
plt.xticks(np.arange(-2, 2.1, 0.5))
# plt.legend( loc='lower right', fontsize=10)
plt.title('Caso 2')
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
plt.annotate('CFD', xy=(ypar1[int(nposcfd/2.5)]/D, upar1_n[int(nposcfd/2.5)]), xycoords='data', xytext=(-1.5, 0.2), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método B', xy=(y[int(npos/2.1)]/D, datos_norm[10][int(npos/2.1)]), xycoords='data', xytext=(-1.5, 0.34), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método D', xy=(y[int(npos/2.3)]/D, datos_norm[12][int(npos/2.3)]), xycoords='data', xytext=(-1.5, 0.3), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método E', xy=(y[int(npos/2.05)]/D, datos_norm[13][int(npos/2.05)]), xycoords='data', xytext=(1.5, 0.3), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.show()

plt.plot(ypar1[125:375]/D, upar1_n[125:375], '.', label='CFD', markersize=1)
plt.plot(y[0:252]/D, datos_norm[9][0:252], label='Método A')
plt.plot(y[0:252]/D, datos_norm[11][0:252], label='Método C')
plt.plot(y[0:252]/D, datos_norm[14][0:252], label='Método F')
plt.plot(y[0:252]/D, datos_norm[15][0:252], label='Método G')
plt.grid()
plt.yticks(np.arange(0, 0.6, 0.05))
plt.xticks(np.arange(-2, 2.1, 0.5))
# plt.legend( loc='lower right', fontsize=10)
plt.title('Caso 2')
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
plt.annotate('CFD', xy=(ypar1[int(nposcfd/1.8)]/D, upar1_n[int(nposcfd/1.8)]), xycoords='data', xytext=(-1, 0.4), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método A', xy=(y[int(npos/1.95)]/D, datos_norm[9][int(npos/1.95)]), xycoords='data', xytext=(1, 0.51), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método C', xy=(y[int(npos/2.3)]/D, datos_norm[11][int(npos/2.3)]), xycoords='data', xytext=(-1, 0.45), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método F', xy=(y[int(npos/1.9)]/D, datos_norm[14][int(npos/1.9)]), xycoords='data', xytext=(1, 0.48), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método G', xy=(y[int(npos/2.05)]/D, datos_norm[15][int(npos/2.05)]), xycoords='data', xytext=(-1, 0.5), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.show()

# Turbinas Parcialmente Alineadas 2
plt.plot(ypar2[125:437]/D, upar2_n[125:437], '.', label='CFD', markersize=1)
plt.plot(y/D, datos_norm[17], label='Método B')
plt.plot(y/D, datos_norm[19], label='Método D')
plt.plot(y/D, datos_norm[20], label='Método E')
plt.legend( loc='upper right', fontsize=10)
plt.grid()
plt.yticks(np.arange(0, 0.3, 0.02))
plt.xticks(np.arange(-2, 3.1, 0.5))
plt.title('Caso 3')
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
# plt.annotate('CFD', xy=(ypar2[int(nposcfd/3)]/D, upar2_n[int(nposcfd/3)]), xycoords='data', xytext=(-1.5, 0.2), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
# plt.annotate('Método B', xy=(y[int(npos/2.1)]/D, datos_norm[17][int(npos/2.1)]), xycoords='data', xytext=(-1.5, 0.34), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
# plt.annotate('Método D', xy=(y[int(npos/2.3)]/D, datos_norm[19][int(npos/2.3)]), xycoords='data', xytext=(-1.5, 0.3), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
# plt.annotate('Método E', xy=(y[int(npos/2.05)]/D, datos_norm[20][int(npos/2.05)]), xycoords='data', xytext=(1.5, 0.3), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.show()

plt.plot(ypar2[125:437]/D, upar2_n[125:437], '.', label='CFD', markersize=1)
plt.plot(y/D, datos_norm[16], label='Método A')
plt.plot(y/D, datos_norm[18], label='Método C')
plt.plot(y/D, datos_norm[21], label='Método F')
plt.plot(y/D, datos_norm[22], label='Método G')
plt.legend( loc='upper right', fontsize=10)
plt.yticks(np.arange(0, 0.3, 0.02))
plt.xticks(np.arange(-2, 3.1, 0.5))
plt.grid()
plt.title('Caso 3')
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
# plt.annotate('Método A', xy=(y[int(npos/1.95)]/D, datos_norm[16][int(npos/1.95)]), xycoords='data', xytext=(1, 0.51), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
# plt.annotate('Método C', xy=(y[int(npos/2.3)]/D, datos_norm[18][int(npos/2.3)]), xycoords='data', xytext=(-1, 0.45), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
# plt.annotate('Método F', xy=(y[int(npos/1.9)]/D, datos_norm[21][int(npos/1.9)]), xycoords='data', xytext=(1, 0.48), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
# plt.annotate('Método G', xy=(y[int(npos/2.05)]/D, datos_norm[22][int(npos/2.05)]), xycoords='data', xytext=(-1, 0.5), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.show()


# Turbinas Desalineadas
plt.plot(ydes[125:437]/D, udes_n[125:437], '.', label='CFD', markersize=1)
plt.plot(y/D, datos_norm[23], label='Método A')
plt.plot(y/D, datos_norm[24], label='Método B')
plt.plot(y/D, datos_norm[25], label='Método C')
plt.plot(y/D, datos_norm[26], label='Método D')
plt.plot(y/D, datos_norm[27], label='Método E')
plt.plot(y/D, datos_norm[28], label='Método F')
plt.plot(y/D, datos_norm[29], label='Método G')
plt.legend( loc='upper left', fontsize=10)
plt.title('Caso 4')
plt.xlabel('y/d')
plt.ylabel('Δu/$u_∞$')
plt.show()

# # Grafico de COMPARACION CON PAPER: Limitations to the validity of single wake:
# plt.plot(ycfd/D, 1-ucfd_n,'.', markersize=1, label='Turbina 0 CFD')
# plt.plot(y[0:252]/D, 1-datos_norm[0][0:252], label='Turbina 0')
# plt.plot(y[0:252]/D, 1-datos_norm[1][0:252], label='Turbina 1')
# plt.plot(yali/D, 1-uali_n, '.', markersize=1, label='Turbinas Alineadas CFD')
# plt.plot(y[0:252]/D, 1-datos_norm[2][0:252],label='Método A - Lineal')
# plt.plot(y[0:252]/D, 1-datos_norm[3][0:252], label='Método B - RSS')
# plt.plot(y[0:252]/D, 1-datos_norm[4][0:252], label='Método C - Lineal')
# plt.plot(y[0:252]/D, 1-datos_norm[5][0:252], label='Método D - RSS')
# plt.plot(y[0:252]/D, 1-datos_norm[6][0:252], label='Método E - Largest')
# plt.title('Velocidad normalizada a la altura del hub')
# plt.grid()
# plt.legend(loc='lower right', fontsize=10)
# plt.yticks(np.arange(0.3, 1.05, 0.05))
# plt.xlabel('y/d')
# plt.ylabel('Δu/$u_∞$')
# plt.show()
