import numpy as np
import matplotlib.pyplot as plt
from Gaussiana import Gaussiana
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_5MW_NREL import Turbina_5MW_NREL
from Coord import Coord
from load_txt_datos import cargar_datos
from U_inf import U_inf
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica

"""
Configuraciones de la prueba segun paper: "Limitations to the validity of single wake
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
gaussiana = Gaussiana()

# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_5MW_NREL(Coord(np.array([0,0,90])))
D = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_5MW_NREL(Coord(np.array([8*D,0,90])))
turbina_parcialmente_alineada = Turbina_5MW_NREL(Coord(np.array([8*D,1*D,90])))
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

# calculo el deficit a 16D para la primera turbina independiente
parque_de_turbinas_primera_indep = Parque_de_turbinas([turbina_0], z_0, z_mast)

x_0 = 16*D
y = np.arange(-3*D, 3*D, 0.01)
z_o = turbina_0.coord.z

data_turbina_0_independiente = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_turbina_0_independiente[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_primera_indep, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
turbina_0.reiniciar_turbina()

# calculo el deficit para la segunda turbina independiente (ubicada en x = 8D) a 16D
parque_de_turbinas_alineada_indep = Parque_de_turbinas([turbina_alineada], z_0, z_mast)

data_turbina_alineada_indep = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_turbina_alineada_indep[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_alineada_indep, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
turbina_alineada.reiniciar_turbina()

# calculo deficit con ambas turbinas
parque_de_turbinas_alineadas = Parque_de_turbinas([turbina_0, turbina_alineada], z_0, z_mast)
parque_de_turbinas_parc_alineadas = Parque_de_turbinas([turbina_0, turbina_parcialmente_alineada], z_0, z_mast)
parque_de_turbinas_desalineadas = Parque_de_turbinas([turbina_0, turbina_desalineada], z_0, z_mast)

# CALCULO DE DATOS PARA GRAFICAR
data_prueba_alineadas_Metodo_A = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_A = np.zeros(len(y))
data_prueba_desalineadas_Metodo_A = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                                    parque_de_turbinas_parc_alineadas, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_B = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_B = np.zeros(len(y))
data_prueba_desalineadas_Metodo_B = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                                    parque_de_turbinas_parc_alineadas, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_desalineadas_Metodo_C = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                                    parque_de_turbinas_parc_alineadas, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_desalineadas_Metodo_D = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                                    parque_de_turbinas_parc_alineadas, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_Largest = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_Largest = np.zeros(len(y))
data_prueba_desalineadas_Metodo_Largest = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_Largest[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_Largest',
                                                                     coord, parque_de_turbinas_alineadas, u_inf,
                                                                     lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas_Metodo_Largest[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_Largest', coord,
                                                                          parque_de_turbinas_parc_alineadas, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_Largest[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_Largest',
                                                                        coord, parque_de_turbinas_desalineadas, u_inf,
                                                                        lista_coord_normalizadas,
                                                                        lista_dAi_normalizados)

data_prueba_alineadas_Metodo_Bernoulli = np.zeros(len(y))
data_prueba_parc_alineadas_Metodo_Bernoulli = np.zeros(len(y))
data_prueba_desalineadas_Metodo_Bernoulli = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_Bernoulli[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_Bernoulli',
                                                                     coord, parque_de_turbinas_alineadas, u_inf,
                                                                     lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas_Metodo_Bernoulli[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_Bernoulli', coord,
                                                                          parque_de_turbinas_parc_alineadas, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_Bernoulli[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_Bernoulli',
                                                                        coord, parque_de_turbinas_desalineadas, u_inf,
                                                                        lista_coord_normalizadas,
                                                                        lista_dAi_normalizados)


# GRAFICO

# Obtencion de datos de CFD
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Caso0\Estela_16D_U.csv"
ycfd, ucfd, vcfd, wcfd = cargar_datos('gaussiano', ruta)
ycfd = ycfd - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Caso1\Estela_16D_U.csv"
yali, uali, vali, wali = cargar_datos('gaussiano', ruta)
yali = yali - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Caso2\Estela_16D_U.csv"
ypar, upar, vpar, wpar = cargar_datos('gaussiano', ruta)
ypar = ypar - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Caso3\Estela_16D_U.csv"
ydes, udes, vdes, wdes = cargar_datos('gaussiano', ruta)
ydes = ydes - 567

# Normalizacion
data_turbina_0_independiente = (u_inf.u_perfil - data_turbina_0_independiente)/u_inf.u_perfil
data_turbina_alineada_indep = (u_inf.u_perfil - data_turbina_alineada_indep)/u_inf.u_perfil
data_prueba_alineadas_Metodo_A = (u_inf.u_perfil - data_prueba_alineadas_Metodo_A)/u_inf.u_perfil
data_prueba_parc_alineadas_Metodo_A = (u_inf.u_perfil - data_prueba_parc_alineadas_Metodo_A)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_A = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_A)/u_inf.u_perfil
data_prueba_alineadas_Metodo_B = (u_inf.u_perfil - data_prueba_alineadas_Metodo_B)/u_inf.u_perfil
data_prueba_parc_alineadas_Metodo_B = (u_inf.u_perfil - data_prueba_parc_alineadas_Metodo_B)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_B = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_B)/u_inf.u_perfil
data_prueba_alineadas_Metodo_C = (u_inf.u_perfil - data_prueba_alineadas_Metodo_C)/u_inf.u_perfil
data_prueba_parc_alineadas_Metodo_C = (u_inf.u_perfil - data_prueba_parc_alineadas_Metodo_C)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_C = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_C)/u_inf.u_perfil
data_prueba_alineadas_Metodo_D = (u_inf.u_perfil - data_prueba_alineadas_Metodo_D)/u_inf.u_perfil
data_prueba_parc_alineadas_Metodo_D = (u_inf.u_perfil - data_prueba_parc_alineadas_Metodo_D)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_D = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_D)/u_inf.u_perfil
data_prueba_alineadas_Metodo_Largest = (u_inf.u_perfil - data_prueba_alineadas_Metodo_Largest)/u_inf.u_perfil
data_prueba_parc_alineadas_Metodo_Largest = (u_inf.u_perfil - data_prueba_parc_alineadas_Metodo_Largest)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_Largest = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_Largest)/u_inf.u_perfil
data_prueba_alineadas_Metodo_Bernoulli = (u_inf.u_perfil - data_prueba_alineadas_Metodo_Bernoulli)/u_inf.u_perfil
data_prueba_parc_alineadas_Metodo_Bernoulli = (u_inf.u_perfil - data_prueba_parc_alineadas_Metodo_Bernoulli)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_Bernoulli = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_Bernoulli)/u_inf.u_perfil
ucfd = (u_inf.u_perfil - ucfd)/u_inf.u_perfil
uali = (u_inf.u_perfil - uali)/u_inf.u_perfil
upar = (u_inf.u_perfil - upar)/u_inf.u_perfil
udes = (u_inf.u_perfil - udes)/u_inf.u_perfil

# LISTAS DE DATOS
modelos_analiticos = [data_turbina_0_independiente,	data_turbina_alineada_indep, data_prueba_alineadas_Metodo_A, data_prueba_parc_alineadas_Metodo_A, data_prueba_desalineadas_Metodo_A, data_prueba_alineadas_Metodo_B, data_prueba_parc_alineadas_Metodo_B, data_prueba_desalineadas_Metodo_B, data_prueba_alineadas_Metodo_C, data_prueba_parc_alineadas_Metodo_C, data_prueba_desalineadas_Metodo_C, data_prueba_alineadas_Metodo_D,	data_prueba_parc_alineadas_Metodo_D, data_prueba_desalineadas_Metodo_D, data_prueba_alineadas_Metodo_Largest, data_prueba_parc_alineadas_Metodo_Largest, data_prueba_desalineadas_Metodo_Largest]
CFD = [ucfd, uali, upar, udes]

# Turbina Independiente
plt.plot(ycfd/D, ucfd, label = 'CFD')
plt.plot(y/D, data_turbina_0_independiente, label = 'Modelo Gaussiano')
plt.legend( loc='lower right', fontsize=10, markerscale=1000)
plt.title('Deficit a 16D')
plt.xlabel('y/D')
plt.ylabel('Deficits')
plt.show()

# Turbinas alineadas deficit sin superposicion
plt.plot(y/D, data_turbina_0_independiente, label = 'Turbina 0 idependiente')
plt.plot(y/D, data_turbina_alineada_indep, label = 'Turbina alineada idependiente')
plt.legend(loc='lower right', fontsize=10)
plt.title('Deficits a 16D sin superposición')
plt.xlabel('y/D')
plt.ylabel('Deficits')
plt.show()

# Turbinas alineadas
plt.plot(yali/D, uali, label='CFD')
plt.plot(y/D, data_prueba_alineadas_Metodo_A, label='Método A')
plt.plot(y/D, data_prueba_alineadas_Metodo_B, label='Método B')
plt.plot(y/D, data_prueba_alineadas_Metodo_C, label='Método C')
plt.plot(y/D, data_prueba_alineadas_Metodo_D, label='Método D')
plt.plot(y/D, data_prueba_alineadas_Metodo_Largest, label='Método Largest')
plt.plot(y/D, data_prueba_alineadas_Metodo_Bernoulli, label='Método Bernoulli')
plt.legend( loc='lower right', fontsize=10)
plt.title('Turbinas alineadas')
plt.xlabel('y/D')
plt.ylabel('Deficits')
plt.show()

# Turbinas Parcialmente Alineadas
plt.plot(ypar/D, upar, label='CFD')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_A, label='Método A')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_B, label='Método B')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_C, label='Método C')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_D, label='Método D')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_Largest, label='Método Largest')
plt.plot(y/D, data_prueba_parc_alineadas_Metodo_Bernoulli, label='Método Bernoulli')
plt.legend( loc='lower right', fontsize=10)
plt.title('Turbinas parcialmente alineadas')
plt.xlabel('y/D')
plt.ylabel('Deficits')
plt.show()

# Turbinas Desalineadas
plt.plot(ydes/D, udes, label='CFD')
plt.plot(y/D, data_prueba_desalineadas_Metodo_A, label='Método A')
plt.plot(y/D, data_prueba_desalineadas_Metodo_B, label='Método B')
plt.plot(y/D, data_prueba_desalineadas_Metodo_C, label='Método C')
plt.plot(y/D, data_prueba_desalineadas_Metodo_D, label='Método D')
plt.plot(y/D, data_prueba_desalineadas_Metodo_Largest, label='Método Largest')
plt.plot(y/D, data_prueba_desalineadas_Metodo_Bernoulli, label='Método Bernoulli')
plt.legend( loc='lower right', fontsize=10)
plt.title('Turbinas desalineadas')
plt.xlabel('y/D')
plt.ylabel('Deficits')
plt.show()

# # METODO A
# plt.plot(yali/D, uali, label = 'Alineadas CFD')
# plt.plot(ypar/D, upar, label = 'Parcialmente Alineadas CFD')
# plt.plot(ydes/D, udes, label = 'Desalineadas CFD')
# plt.plot(y/D, data_prueba_alineadas_Metodo_A, label = 'Alineadas Metodo A')
# plt.plot(y/D, data_prueba_parc_alineadas_Metodo_A, label = 'Parc. Ali. Metodo A')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_A, label = 'Desalineadas Metodo A')
# plt.legend( loc='lower right', fontsize=5)
# plt.title('Prueba Metodos de Superposicion con Int. Deterministica')
# plt.xlabel('y/D')
# plt.ylabel('Velocidades [m/s]')
# plt.show()
# # METODO B
# plt.plot(yali/D, uali, label = 'Alineadas CFD')
# plt.plot(ypar/D, upar, label = 'Parcialmente Alineadas CFD')
# plt.plot(ydes/D, udes, label = 'Desalineadas CFD')
# plt.plot(y/D, data_prueba_alineadas_Metodo_B, label = 'Alineadas Metodo B')
# plt.plot(y/D, data_prueba_parc_alineadas_Metodo_B, label = 'Parc. Ali. Metodo B')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_B, label = 'Desalineadas Metodo B')
# plt.legend( loc='lower right', fontsize=5)
# plt.title('Prueba Metodos de Superposicion con Int. Deterministica')
# plt.xlabel('y/D')
# plt.ylabel('Velocidades [m/s]')
# plt.show()
# # METODO C
# plt.plot(yali/D, uali, label = 'Alineadas CFD')
# plt.plot(ypar/D, upar, label = 'Parcialmente Alineadas CFD')
# plt.plot(ydes/D, udes, label = 'Desalineadas CFD')
# plt.plot(y/D, data_prueba_alineadas_Metodo_C, label = 'Alineadas Metodo C')
# plt.plot(y/D, data_prueba_parc_alineadas_Metodo_C, label = 'Parc. Ali. Metodo C')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_C, label = 'Desalineadas Metodo C')
# plt.legend( loc='lower right', fontsize=5)
# plt.title('Prueba Metodos de Superposicion con Int. Deterministica')
# plt.xlabel('y/D')
# plt.ylabel('Velocidades [m/s]')
# plt.show()
# # METODO D
# plt.plot(yali/D, uali, label = 'Alineadas CFD')
# plt.plot(ypar/D, upar, label = 'Parcialmente Alineadas CFD')
# plt.plot(ydes/D, udes, label = 'Desalineadas CFD')
# plt.plot(y/D, data_prueba_alineadas_Metodo_D, label = 'Alineadas Metodo D')
# plt.plot(y/D, data_prueba_parc_alineadas_Metodo_D, label = 'Parc. Ali. Metodo D')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_D, label = 'Desalineadas Metodo D')
# plt.legend( loc='lower right', fontsize=5)
# plt.title('Prueba Metodos de Superposicion con Int. Deterministica')
# plt.xlabel('y/D')
# plt.ylabel('Velocidades [m/s]')
# plt.show()
# # METODO LARGEST
# plt.plot(yali/D, uali, label = 'Alineadas CFD')
# plt.plot(ypar/D, upar, label = 'Parcialmente Alineadas CFD')
# plt.plot(ydes/D, udes, label = 'Desalineadas CFD')
# plt.plot(y/D, data_prueba_alineadas_Metodo_Largest, label = 'Alineadas Metodo Largest')
# plt.plot(y/D, data_prueba_parc_alineadas_Metodo_Largest, label = 'Parc. Ali. Metodo Largest')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_Largest, label = 'Desalineadas Metodo Largest')
# plt.legend( loc='lower right', fontsize=5)
# plt.title('Prueba Metodos de Superposicion con Int. Deterministica')
# plt.xlabel('y/D')
# plt.ylabel('Velocidades [m/s]')
# plt.show()