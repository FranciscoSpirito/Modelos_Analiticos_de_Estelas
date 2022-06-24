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

# Obtencion de datos de CFD
ruta = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso0\Estela_16D_U.csv"
X = [str(i) for i in range(0,5,1)]
l_ruta = list(ruta)
datosCFD = []
for x in X:
    l_ruta[126] = x
    ruta = "".join(l_ruta)
    print(ruta)
    y, u, v, w = cargar_datos('gaussiano', ruta)
    datosCFD.append([y, u])


# Modelo analitico
gaussiana = Gaussiano()

# Definimos la primera turbina en el 0 0
turbina_0 = Turbina_5MW_NREL(Coord(np.array([630, 567, 567])))
D = turbina_0.d_0

# Turbinas
turbina_alineada = Turbina_5MW_NREL(Coord(np.array([630+8*D, 567, 567])))
turbina_parcialmente_alineada1 = Turbina_5MW_NREL(Coord(np.array([630+8*D, 567+0.5*D, 567])))
turbina_parcialmente_alineada2 = Turbina_5MW_NREL(Coord(np.array([630+8*D, 567+1*D, 567])))
turbina_desalineada = Turbina_5MW_NREL(Coord(np.array([630+8*D, 567+1.75*D, 567])))

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

# METODOS DE SUPERPOSICION
metodos_sup = ['Metodo_A', 'Metodo_B', 'Metodo_C', 'Metodo_D', 'Metodo_E', 'Metodo_F', 'Metodo_G']
# CASOS
parque_de_turbinas_primera_indep = ParqueEolico([turbina_0], z_0, z_mast)
parque_de_turbinas_segunda_indep = ParqueEolico([turbina_alineada], z_0, z_mast)
parque_de_turbinas_alineadas = ParqueEolico([turbina_0, turbina_alineada], z_0, z_mast)
parque_de_turbinas_parc_alineadas1 = ParqueEolico([turbina_0, turbina_parcialmente_alineada1], z_0, z_mast)
parque_de_turbinas_parc_alineadas2 = ParqueEolico([turbina_0, turbina_parcialmente_alineada2], z_0, z_mast)
parque_de_turbinas_desalineadas = ParqueEolico([turbina_0, turbina_desalineada], z_0, z_mast)
casos_ss = [parque_de_turbinas_primera_indep]
casos_cs = [parque_de_turbinas_alineadas, parque_de_turbinas_parc_alineadas1, parque_de_turbinas_parc_alineadas2, parque_de_turbinas_desalineadas]
# calculo el deficit a 16D para la primera turbina independiente
x_0 = 630 + 16*D
z_o = turbina_0.coord.z
datosMA = []
# for caso in casos_ss:
#     datos = []
#     for y in datosCFD[0][0]:
#         coord = Coord(np.array([x_0, y, z_o]))
#        datos.append(calcular_u_en_coord_integral_deterministica(gaussiana, 'Metodo_A', coord,
#                                                                                       caso,
#                                                                                       u_inf,
#                                                                                       lista_coord_normalizadas,
#                                                                                       lista_dAi_normalizados))
#     datosMA.append([datosCFD[0][0], datos])
#     for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_parcialmente_alineada2, turbina_desalineada]:
#         turbina.reiniciar_turbina()
for metodo in metodos_sup:
    datosMetodo = []
    for caso, datoCFD in zip(casos_cs, datosCFD):
        datos = []
        for y in datoCFD[0]:
            coord = Coord(np.array([x_0, y, z_o]))
            datos.append(calcular_u_en_coord_integral_deterministica(gaussiana, metodo, coord,
                                                                     caso,
                                                                     u_inf,
                                                                     lista_coord_normalizadas,
                                                                     lista_dAi_normalizados))
        datosMetodo.append(datos)
    datosMA.append(datosMetodo)
    for turbina in [turbina_0, turbina_alineada, turbina_parcialmente_alineada1, turbina_parcialmente_alineada2, turbina_desalineada]:
        turbina.reiniciar_turbina()

for datoMA, metodo in zip(datosMA, metodos_sup):
    sum_e1 = sum(np.array(datosCFD[1][1]) - np.array(datoMA[0]))
    sum_e2 = sum(np.array(datosCFD[2][1]) - np.array(datoMA[1]))
    sum_e3 = sum(np.array(datosCFD[3][1]) - np.array(datoMA[2]))
    sum_e4 = sum(np.array(datosCFD[4][1]) - np.array(datoMA[3]))
    error = sum_e1+sum_e2+sum_e3+sum_e4
    print(metodo + ': ' + str(error))
