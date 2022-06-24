import matplotlib.pyplot as plt
import numpy as np
from Turbina_5MW_NREL import Turbina_5MW_NREL
from ParqueEolico import ParqueEolico
from load_txt_datos import cargar_datos
from Coord import Coord
from U_inf import U_inf
from Gaussiano import Gaussiano
from calcular_u_en_coord_integral_deterministica import  calcular_u_en_coord_integral_deterministica



ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso0\Estela_1D_U.csv"
X = [str(i) for i in range(4,18,4)]
l_ruta = list(ruta)
datosCFD = []
for x in X:
    l_ruta[135] = x
    ruta = "".join(l_ruta)
    print(ruta)
    y, u, v, w = cargar_datos('gaussiano', ruta)
    datosCFD.append([y, u])

casosCoord = []
for datos, i in zip(datosCFD,X):
    x = 630 + int(i)*126
    listaCoord = []
    for y_i in datos[0]:
        listaCoord.append(Coord([x, y_i, 567]))
    casosCoord.append(listaCoord)

turbina = Turbina_5MW_NREL(Coord(np.array([630, 567, 567])))
# Diferenciacion del actuador discal
cantidad_de_puntos = 5
espesor = turbina.definicion_de_espesor(cantidad_de_puntos)
lista_coord_normalizadas, lista_dAi_normalizados = turbina.coordenadas_y_areas_normalizadas(cantidad_de_puntos, espesor)
# Define el tipo de perfil de velocidades cte o log
z_mast, z_0, perfil = 90, 0.01, 'cte'
u_inf = U_inf(z_mast, z_0, perfil)
u_inf.u_mast = 12
coord_u = Coord([0,0,z_mast])
u_inf.perfil_flujo_base(coord_u)
gaussiano = Gaussiano()

datosMA = []
for coordenadas in casosCoord:
    parque_de_turbinas = ParqueEolico([turbina], z_0, z_mast)
    velocidades = []
    for coord in coordenadas:
        velocidades.append(calcular_u_en_coord_integral_deterministica(gaussiano, 'Metodo_C', coord, parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados))
    datosMA.append([y, np.array(velocidades)])

for datoMA, datoCFD in zip(datosMA, datosCFD):
    plt.plot((datoCFD[0]-567)/turbina.d_0, (12-datoCFD[1])/12,  color='slategray')
    plt.plot((datoMA[0]-567)/turbina.d_0, (12-datoMA[1])/12, '-.', color='black')
datoCFD, datoMA = datosCFD[0], datosMA[0]
plt.plot((datoCFD[0]-567)/turbina.d_0, (12-datoCFD[1])/12,  color='slategray', label='CFD')
plt.plot((datoMA[0]-567)/turbina.d_0, (12-datoMA[1])/12, '-.', color='black', label='Modelo Gaussiano')
plt.xlabel('y/d')
plt.ylabel('Δu/u')
plt.legend()
plt.title('Ajuste 2')
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Ajustes\Ajustes_2')
plt.show()