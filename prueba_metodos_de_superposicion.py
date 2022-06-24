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
gaussiana = Gaussiano()

# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_5MW_NREL(Coord(np.array([0,0,90])))
D = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_5MW_NREL(Coord(np.array([8*D,0,90])))
turbina_parcialmente_alineada1 = Turbina_5MW_NREL(Coord(np.array([8*D,1*D,90])))
turbina_parcialmente_alineada2 = Turbina_5MW_NREL(Coord(np.array([8*D,1*D,90])))
turbina_desalineada = Turbina_5MW_NREL(Coord(np.array([8*D,1.75*D,90])))

# Diferenciacion del actuador discal
cantidad_de_puntos = 100
espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)

# Definicion de velocidad de entrada
z_0, z_mast, perfil = 0.01, 90, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 12
coord_u = Coord([0,0,z_mast])
u_inf.perfil_flujo_base(coord_u)

# calculo el deficit a 16D para la primera turbina independiente
parque_de_turbinas_primera_indep = ParqueEolico([turbina_0], z_0, z_mast)

x_0 = 16*D
step = 2
y = np.arange(-2*D, 3*D, step)
z_o = turbina_0.coord.z

# GRAFICOS DE TURBINAS INDEPENDIENTES O AISLADAS
data_turbina_0_independiente = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_turbina_0_independiente[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_primera_indep, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
turbina_0.reiniciar_turbina()

# calculo el deficit para la segunda turbina independiente (ubicada en x = 8D) a 16D
parque_de_turbinas_alineada_indep = ParqueEolico([turbina_alineada], z_0, z_mast)

data_turbina_alineada_indep = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_turbina_alineada_indep[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord, parque_de_turbinas_alineada_indep, u_inf, lista_coord_normalizadas,lista_dAi_normalizados)
turbina_alineada.reiniciar_turbina()

# calculo deficit con ambas turbinas
parque_de_turbinas_alineadas = ParqueEolico([turbina_0, turbina_alineada], z_0, z_mast)
parque_de_turbinas_parc_alineadas1 = ParqueEolico([turbina_0, turbina_parcialmente_alineada1], z_0, z_mast)
parque_de_turbinas_parc_alineadas2 = ParqueEolico([turbina_0, turbina_parcialmente_alineada2], z_0, z_mast)
parque_de_turbinas_desalineadas = ParqueEolico([turbina_0, turbina_desalineada], z_0, z_mast)

# CALCULO DE DATOS PARA GRAFICAR
data_prueba_alineadas_Metodo_A = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_A = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_A = np.zeros(len(y))
data_prueba_desalineadas_Metodo_A = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                                    parque_de_turbinas_parc_alineadas1, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                                    parque_de_turbinas_parc_alineadas2, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_A[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_B = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_B = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_B = np.zeros(len(y))
data_prueba_desalineadas_Metodo_B = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                                    parque_de_turbinas_parc_alineadas1, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                                    parque_de_turbinas_parc_alineadas2, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_B[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_B', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_C = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_C = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_C = np.zeros(len(y))
data_prueba_desalineadas_Metodo_C = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                                    parque_de_turbinas_parc_alineadas1, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                                    parque_de_turbinas_parc_alineadas2, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_C[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_C', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_D = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_D = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_D = np.zeros(len(y))
data_prueba_desalineadas_Metodo_D = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                               parque_de_turbinas_alineadas, u_inf,
                                                               lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                                    parque_de_turbinas_parc_alineadas1, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                                    parque_de_turbinas_parc_alineadas2, u_inf,
                                                                    lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_D[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_D', coord,
                                                                  parque_de_turbinas_desalineadas, u_inf,
                                                                  lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()

data_prueba_alineadas_Metodo_E = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_E = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_E = np.zeros(len(y))
data_prueba_desalineadas_Metodo_E = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_E[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_E',
                                                                     coord, parque_de_turbinas_alineadas, u_inf,
                                                                     lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_E[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_E', coord,
                                                                          parque_de_turbinas_parc_alineadas1, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_E[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_E', coord,
                                                                          parque_de_turbinas_parc_alineadas2, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_E[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_E',
                                                                        coord, parque_de_turbinas_desalineadas, u_inf,
                                                                        lista_coord_normalizadas,
                                                                        lista_dAi_normalizados)

data_prueba_alineadas_Metodo_G = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_G = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_G = np.zeros(len(y))
data_prueba_desalineadas_Metodo_G = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_G[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_G',
                                                                     coord, parque_de_turbinas_alineadas, u_inf,
                                                                     lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_G[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_G', coord,
                                                                          parque_de_turbinas_parc_alineadas1, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_G[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_G', coord,
                                                                          parque_de_turbinas_parc_alineadas2, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_G[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_G',
                                                                        coord, parque_de_turbinas_desalineadas, u_inf,
                                                                        lista_coord_normalizadas,
                                                                        lista_dAi_normalizados)
data_prueba_alineadas_Metodo_F = np.zeros(len(y))
data_prueba_parc_alineadas1_Metodo_F = np.zeros(len(y))
data_prueba_parc_alineadas2_Metodo_F = np.zeros(len(y))
data_prueba_desalineadas_Metodo_F = np.zeros(len(y))

for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_alineadas_Metodo_F[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_F',
                                                                     coord, parque_de_turbinas_alineadas, u_inf,
                                                                     lista_coord_normalizadas, lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas1_Metodo_F[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_F', coord,
                                                                          parque_de_turbinas_parc_alineadas1, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_parc_alineadas2_Metodo_F[i] = calcular_u_en_coord_integral_deterministica(gaussiana,
                                                                          'Metodo_F', coord,
                                                                          parque_de_turbinas_parc_alineadas2, u_inf,
                                                                          lista_coord_normalizadas,
                                                                          lista_dAi_normalizados)
for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_desalineada]:
    turbina.reiniciar_turbina()
for i in range(len(y)):
    coord = Coord(np.array([x_0, y[i], z_o]))
    data_prueba_desalineadas_Metodo_F[i] = calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_F',
                                                                        coord, parque_de_turbinas_desalineadas, u_inf,
                                                                        lista_coord_normalizadas,
                                                                        lista_dAi_normalizados)


# GRAFICO

# Obtencion de datos de CFD
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Resultados_02-06-22\Caso0\sets\Estela_16D_U.csv"
ycfd, ucfd, vcfd, wcfd = cargar_datos('gaussiano', ruta)
ycfd = ycfd - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Resultados_02-06-22\Caso1\sets\Estela_16D_U.csv"
yali, uali, vali, wali = cargar_datos('gaussiano', ruta)
yali = yali - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Resultados_02-06-22\Caso2\sets\Estela_16D_U.csv"
ypar1, upar1, vpar1, wpar1 = cargar_datos('gaussiano', ruta)
ypar1 = ypar1 - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Resultados_02-06-22\Caso3\sets\Estela_16D_U.csv"
ypar2, upar2, vpar2, wpar2 = cargar_datos('gaussiano', ruta)
ypar2 = ypar2 - 567
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Resultados_02-06-22\Caso4\sets\Estela_16D_U.csv"
ydes, udes, vdes, wdes = cargar_datos('gaussiano', ruta)
ydes = ydes - 567

# Normalizacion
data = [data_turbina_0_independiente,
data_turbina_alineada_indep,
data_prueba_alineadas_Metodo_A,
data_prueba_parc_alineadas1_Metodo_A,
data_prueba_parc_alineadas2_Metodo_A,
data_prueba_desalineadas_Metodo_A,
data_prueba_alineadas_Metodo_B,
data_prueba_parc_alineadas1_Metodo_B,
data_prueba_parc_alineadas2_Metodo_B,
data_prueba_desalineadas_Metodo_B,
data_prueba_alineadas_Metodo_C,
data_prueba_parc_alineadas1_Metodo_C,
data_prueba_parc_alineadas2_Metodo_C,
data_prueba_desalineadas_Metodo_C,
data_prueba_alineadas_Metodo_D,
data_prueba_parc_alineadas1_Metodo_D,
data_prueba_parc_alineadas2_Metodo_D,
data_prueba_desalineadas_Metodo_D,
data_prueba_alineadas_Metodo_E,
data_prueba_parc_alineadas1_Metodo_E,
data_prueba_parc_alineadas2_Metodo_E,
data_prueba_desalineadas_Metodo_E,
data_prueba_alineadas_Metodo_G,
data_prueba_parc_alineadas1_Metodo_G,
data_prueba_parc_alineadas2_Metodo_G,
data_prueba_desalineadas_Metodo_G,
data_prueba_alineadas_Metodo_F,
data_prueba_parc_alineadas1_Metodo_F,
data_prueba_parc_alineadas2_Metodo_F,
data_prueba_desalineadas_Metodo_F]
data_turbina_0_independiente = (u_inf.u_perfil - data_turbina_0_independiente)/u_inf.u_perfil
data_turbina_alineada_indep = (u_inf.u_perfil - data_turbina_alineada_indep)/u_inf.u_perfil
data_prueba_alineadas_Metodo_A = (u_inf.u_perfil - data_prueba_alineadas_Metodo_A)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_A = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_A)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_A = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_A)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_A = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_A)/u_inf.u_perfil
data_prueba_alineadas_Metodo_B = (u_inf.u_perfil - data_prueba_alineadas_Metodo_B)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_B = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_B)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_B = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_B)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_B = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_B)/u_inf.u_perfil
data_prueba_alineadas_Metodo_C = (u_inf.u_perfil - data_prueba_alineadas_Metodo_C)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_C = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_C)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_C = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_C)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_C = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_C)/u_inf.u_perfil
data_prueba_alineadas_Metodo_D = (u_inf.u_perfil - data_prueba_alineadas_Metodo_D)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_D = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_D)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_D = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_D)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_D = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_D)/u_inf.u_perfil
data_prueba_alineadas_Metodo_E = (u_inf.u_perfil - data_prueba_alineadas_Metodo_E)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_E = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_E)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_E = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_E)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_E = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_E)/u_inf.u_perfil
data_prueba_alineadas_Metodo_G = (u_inf.u_perfil - data_prueba_alineadas_Metodo_G)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_G = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_G)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_G = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_G)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_G = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_G)/u_inf.u_perfil
data_prueba_alineadas_Metodo_F = (u_inf.u_perfil - data_prueba_alineadas_Metodo_F)/u_inf.u_perfil
data_prueba_parc_alineadas1_Metodo_F = (u_inf.u_perfil - data_prueba_parc_alineadas1_Metodo_F)/u_inf.u_perfil
data_prueba_parc_alineadas2_Metodo_F = (u_inf.u_perfil - data_prueba_parc_alineadas2_Metodo_F)/u_inf.u_perfil
data_prueba_desalineadas_Metodo_F = (u_inf.u_perfil - data_prueba_desalineadas_Metodo_F)/u_inf.u_perfil
ucfd = (u_inf.u_perfil - ucfd)/u_inf.u_perfil
uali = (u_inf.u_perfil - uali)/u_inf.u_perfil
upar1 = (u_inf.u_perfil - upar1)/u_inf.u_perfil
upar2 = (u_inf.u_perfil - upar2)/u_inf.u_perfil
udes = (u_inf.u_perfil - udes)/u_inf.u_perfil

# LISTAS DE DATOS
modelos_analiticos = [data_turbina_0_independiente,	data_turbina_alineada_indep, data_prueba_alineadas_Metodo_A, data_prueba_parc_alineadas1_Metodo_A, data_prueba_desalineadas_Metodo_A, data_prueba_alineadas_Metodo_B, data_prueba_parc_alineadas1_Metodo_B, data_prueba_desalineadas_Metodo_B, data_prueba_alineadas_Metodo_C, data_prueba_parc_alineadas1_Metodo_C, data_prueba_desalineadas_Metodo_C, data_prueba_alineadas_Metodo_D,	data_prueba_parc_alineadas1_Metodo_D, data_prueba_desalineadas_Metodo_D, data_prueba_alineadas_Metodo_E, data_prueba_parc_alineadas1_Metodo_E, data_prueba_desalineadas_Metodo_E]
# CFD = [ucfd, uali, upar, udes]

# Turbina Independiente
plt.plot(ycfd/D, ucfd, label='CFD')
plt.plot(y[0:252]/D, data_turbina_0_independiente[0:252], label='Modelo Gaussiano')
plt.legend(loc='lower right', fontsize=10, markerscale=1000)
plt.title('Deficit a 16D')
plt.xlabel('y/D')
plt.ylabel('Deficits')
plt.show()

# Turbinas alineadas deficit sin superposicion
plt.plot(y/D, data_turbina_0_independiente, label='Turbina 0')
plt.plot(y/D, data_turbina_alineada_indep, label='Turbina 1')
plt.legend(loc='lower right', fontsize=10)
plt.title('Turbinas aisladas, X = 16 d')
plt.xlabel('y/d')
plt.ylabel('Deficits')
plt.show()

nposcfd = len(yali)
npos = len(y[0:252])
# Turbinas alineadas
plt.plot(yali/D, uali, '.', markersize=1, label='CFD')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_A[0:252],label='Método A')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_B[0:252], label='Método B')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_C[0:252], label='Método C')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_D[0:252], label='Método D')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_E[0:252], label='Método E')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_G[0:252], label='Método G')
plt.plot(y[0:252]/D, data_prueba_alineadas_Metodo_F[0:252], label='Método F')
plt.annotate('CFD', xy=(yali[int(nposcfd/2)]/D, uali[int(nposcfd/2)]), xycoords='data', xytext=(1, 0.35), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método A', xy=(y[int(npos/2.3)]/D, data_prueba_alineadas_Metodo_A[int(npos/2.3)]), xycoords='data', xytext=(-1.5, 0.3), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método B', xy=(y[int(npos/2)]/D, data_prueba_alineadas_Metodo_B[int(npos/2)]), xycoords='data', xytext=(1, 0.5), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método C', xy=(y[int(npos/2)]/D, data_prueba_alineadas_Metodo_C[int(npos/2)]), xycoords='data', xytext=(-1.5, 0.5), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método D', xy=(y[int(npos/2)]/D, data_prueba_alineadas_Metodo_D[int(npos/2)]), xycoords='data', xytext=(1, 0.4), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método E', xy=(y[int(npos/2)]/D, data_prueba_alineadas_Metodo_E[int(npos/2)]), xycoords='data', xytext=(1, 0.45), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=-50,rad=0"))
plt.annotate('Método F', xy=(y[int(npos/2.2)]/D, data_prueba_alineadas_Metodo_F[int(npos/2.2)]), xycoords='data', xytext=(-1.5, 0.35), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
plt.annotate('Método G', xy=(y[int(npos/2)]/D, data_prueba_alineadas_Metodo_G[int(npos/2)]), xycoords='data', xytext=(-1.5, 0.55), arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=0, connectionstyle="arc,angleA=0,armA=50,rad=0"))
# plt.legend( loc='lower right', fontsize=10)
plt.title('Caso 1')
plt.xlabel('y/d')
plt.ylabel('Deficits')
plt.show()
#
# # Turbinas Parcialmente Alineadas 1
# plt.plot(ypar1/D, upar1, '.', label='CFD', markersize=1)
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_A, label='Método A')
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_B, label='Método B')
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_C, label='Método C')
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_D, label='Método D')
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_E, label='Método E')
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_G, label='Método G')
# plt.plot(y/D, data_prueba_parc_alineadas1_Metodo_F, label='Método_F')
# plt.legend( loc='lower right', fontsize=10)
# plt.title('Caso 2')
# plt.xlabel('y/d')
# plt.ylabel('Deficits')
# plt.show()
#
# # Turbinas Parcialmente Alineadas 2
# plt.plot(ypar2/D, upar2, '.', label='CFD', markersize=1)
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_A, label='Método A')
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_B, label='Método B')
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_C, label='Método C')
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_D, label='Método D')
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_E, label='Método E')
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_G, label='Método G')
# plt.plot(y/D, data_prueba_parc_alineadas2_Metodo_F, label='Método_F')
# plt.legend( loc='lower right', fontsize=10)
# plt.title('Caso 3')
# plt.xlabel('y/d')
# plt.ylabel('Deficits')
# plt.show()
#
#
# # Turbinas Desalineadas
# plt.plot(ydes/D, udes, '.', label='CFD', markersize=1)
# plt.plot(y/D, data_prueba_desalineadas_Metodo_A, label='Método A')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_B, label='Método B')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_C, label='Método C')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_D, label='Método D')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_E, label='Método E')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_G, label='Método G')
# plt.plot(y/D, data_prueba_desalineadas_Metodo_F, label='Método_F')
# plt.legend( loc='lower right', fontsize=10)
# plt.title('Caso 4')
# plt.xlabel('y/d')
# plt.ylabel('Deficits')
# plt.show()