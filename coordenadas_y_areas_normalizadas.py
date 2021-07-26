import numpy
import numpy as np
from Coord import Coord

""" Esta funcion esta para hacer graficos, el metodo usado se encuentra en la clase Turbina """

# Devuelve una lista de areas y coordenadas para un disco de radio = 1
def coordenadas_y_areas_normalizadas( n, e):
    # e: espesor
    # n: numero de puntos
    # lista_ri: distancia a la linea media de los discos
    # lista_areas_discos_dividido_pi: areas de los discos (no se las multiplica por pi porque despues vamos a dividirlas por pi cuando calculamos los n_i)
    # lista_n_i: numero de divisiones angulares de cada discos
    # lista_dAi: areas de los diferenciales de cada punto normalizados. np.array, pq despues lo usamos para calcular una integral.
    # lista_coord_normalizadas: lista con las coordenadas normalizadas.

    lista_ri = []
    ri = e + e / 2
    lista_ri.append(ri)
    while ri + e < 1:
        ri += e
        lista_ri.append(ri)

    lista_areas_discos_dividido_pi = [(radio + e / 2) ** 2 - (radio - e / 2) ** 2 for radio in lista_ri]
    n_min = 4
    lista_n_i = [round(area_de_disco_divido_pi * n) if round(area_de_disco_divido_pi * n) > n_min else n_min for
                 area_de_disco_divido_pi in lista_areas_discos_dividido_pi]

    lista_dAi_normalizados = []
    lista_coord_normalizadas = []
    for i in range(len(lista_ri)):
        dif_titta = (2 * np.pi) / lista_n_i[i]  # Creacion del paso angular
        j = 0
        dAi_normalizado = np.pi * lista_areas_discos_dividido_pi[i] / lista_n_i[i]
        while j < lista_n_i[i]:
            titta = j * dif_titta
            y_i = (lista_ri[i] * np.cos(titta))
            z_i = (lista_ri[i] * np.sin(titta))
            coord_disco_i = Coord(np.array([0, y_i, z_i]))
            lista_coord_normalizadas.append(coord_disco_i)
            lista_dAi_normalizados.append(dAi_normalizado)
            j += 1

    lista_coord_normalizadas.insert(0, Coord(np.array([0, 0, 0])))
    lista_dAi_normalizados.insert(0, np.pi * e ** 2)
    lista_dAi_normalizados = np.array(lista_dAi_normalizados)

    return lista_coord_normalizadas, lista_dAi_normalizados
