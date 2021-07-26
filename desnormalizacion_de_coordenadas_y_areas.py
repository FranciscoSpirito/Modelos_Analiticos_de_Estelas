import numpy as np

""" Esta funcion esta para hacer graficos, el metodo usado se encuentra en la clase Turbina """

# Define el espesor que genera los diferenciales mas cuadrados con el numero de puntos elegido
def definicion_de_espesor(self, n):
    #  n: numero de puntos
    #  factor_de_tolerancia_porcentual es la maxima diferencia que puede haber entre los arcos y el espesor
    #  expresado como porsentaje del espesor.
    #  El metodo itera desde una tolerancia del 100% hasta 1% o corta cuando queda un unico espesor que cumple con esta tolerancia

    n_min = 4
    cantidad_max_de_discos = round(n / n_min)

    for factor_tolerancia_porcentual in range(100, 1, -1):
        lista_de_espesores = []
        for cantidad_de_discos in range(2, cantidad_max_de_discos):
            e = 1 / cantidad_de_discos
            if round((2 * e - e ** 2) * n) <= 4:
                n_ext = n_min
            else:
                n_ext = round((2 * e - e ** 2) * n)

            if round((3 * e ** 2) * n) <= 4:
                n_int = n_min
            else:
                n_int = round((3 * e ** 2) * n)

            arco_ext = 2 * np.pi / n_ext
            arco_int = e * 2 * np.pi / n_int
            diferencia_ext = abs(arco_ext - e)
            diferencia_int = abs(e - arco_int)
            factor_tolerancia = factor_tolerancia_porcentual / 100
            if diferencia_ext <= factor_tolerancia * e and diferencia_int <= factor_tolerancia * e:
                lista_de_espesores.append(e)

        if len(lista_de_espesores) == 1:
            break

    return lista_de_espesores[0]


# Genera una lista de areas y coordenadas para un disco de radio = 1
def coordenadas_y_areas_normalizadas(self, n, e):
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


# Desnormaliza coordenadas y las coloca en la posicion de la turbina en el parque. Guarda las coordenadas en el objeto turbina como lista_coord.
# Desnormaliza los diferenciales de areas. Guarda los diferenciales en el objeto turbina, como lista_dAi
def desnormalizar_coord_y_areas(self, lista_coord_normalizadas, lista_dAi_normalizados):
    self.lista_dAi = (self.d_0 / 2) ** 2 * lista_dAi_normalizados
    self.lista_coord = []
    for coord_aux in lista_coord_normalizadas:
        coord_turbina_xi = self.coord.x + self.d_0 / 2 * coord_aux.x
        coord_turbina_yi = self.coord.y + self.d_0 / 2 * coord_aux.y
        coord_turbina_zi = self.coord.z + self.d_0 / 2 * coord_aux.z
        coord_turbina_i = Coord(np.array([coord_turbina_xi, coord_turbina_yi, coord_turbina_zi]))
        self.lista_coord.append(coord_turbina_i)