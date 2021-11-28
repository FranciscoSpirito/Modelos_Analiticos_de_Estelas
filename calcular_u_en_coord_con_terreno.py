from __future__ import division
import numpy as np
from scipy.interpolate import interp1d
from Modelo import Modelo
from Parque_de_turbinas import Parque_de_turbinas
from Turbina import Turbina
from Coord import Coord
from Estela import Estela
from Iso_Superficie import Iso_Superficie


# calcular_u_en_coord:
# .INPUT
# modelo_deficit: instancia de Modelo, define la forma con la que se ajustara el perfil de la estela
# metodo_superposicion: forma en la que se superone la estela (lineal, dominante, etc)
# coord: instancia de Coord, es el punto del espacio en el que se busca calcular el viento u
# parque_de_turbinas: instancia de Parque_de_turbinas, incluye toda la informacion relevante al
# parque que perturba el flujo
# iso_s: intancia de iso_s, contiene la informacion sobre el viento de entrada (isosuperficie)
# lista_coord_normalizadas: coordenadas de un disco de radio 1 ubicado en el (0,0,0)
# lista_dAi_normalizadas: areas de los diferenciales de un disco de radio 1 ubicado en el (0,0,0)
# u: viento en la coordenada coord al atravezar el parque con las condiciones de entrada definidas


def calcular_u_en_coord_integral_deterministica(modelo_deficit, metodo_superposicion, coord, parque_de_turbinas, iso_s,
                                                lista_coord_normalizadas, lista_dAi_normalizados):
    parque_de_turbinas.ordenar_turbinas_de_izquierda_a_derecha()
    turbinas_a_la_izquierda_de_coord = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord(coord)
    # lista que guardara los deficits normalizados generados por todas las turbinas a la izquierda de coord
    deficit_normalizado_en_coord = []
    # Radio maximo de interseccion con las ldc (turbinas con estelas fuera de este no se toman en cuenta su influencia)
    rmax = 500
    # Puntos dentro del radio maximo (normalizados)
    nsamp = 21
    samp_l = np.linspace(-1, 1, nsamp)

    for turbina_selec in turbinas_a_la_izquierda_de_coord:

        turbina_selec.desnormalizar_coord_y_areas(lista_coord_normalizadas, lista_dAi_normalizados)
        turbinas_a_la_izquierda_de_turbina_selec = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord(
            turbina_selec.coord)
        cantidad_turbinas_izquierda_de_selec = len(turbinas_a_la_izquierda_de_turbina_selec)

        # Velocidades del flujo base en el hub
        coord_xy = np.vstack(turbina_selec.coord.x, turbina_selec.coord.y)
        u0, v0 = turbina_selec.U[0], turbina_selec.U[1]
        muv = np.sqrt(u0 ** 2 + v0 ** 2)

        # Se desnormalizan las muestras samp_l dejandolas pertenecientes al plano perp. a la vel. del flujo en el hub.
        samp_xy = (np.vstack((samp_l * rmax * -v0 / muv,
                              samp_l * rmax * u0 / muv)).T + coord_xy).T

        # lista que guardara los deficits generados sobre las coordenadas random dentro del disco
        # de turbina selec para calcular el montecarlo
        arreglo_deficit = []

        # separa el caso en el que la turbina es la 'mas a la izquierda', es decir, es la turbina que recibe
        # el viento limpio, sin verse afectado por otra turbina
        if cantidad_turbinas_izquierda_de_selec == 0:
            turbina_virtual = Turbina(turbina_selec.d_0, Coord(
                np.array([turbina_selec.coord.x, turbina_selec.coord.y, turbina_selec.coord.z])))
            turbina_virtual.c_T = 0
            turbinas_a_la_izquierda_de_turbina_selec = [turbina_virtual]

        for turbina_a_la_izquierda in turbinas_a_la_izquierda_de_turbina_selec:

            # Verificamos que este dentro del rmax
            samp_l_int = interp1d(iso_s._interp_t(*samp_xy, grid=False), samp_l, kind='cubic', bounds_error=False)(turbina_a_la_izquierda.t)

            if samp_l_int != None:
                interseccion = (np.vstack((samp_l * rmax * -v0 / muv,
                                      samp_l * rmax * u0 / muv)).T + coord_xy).T
                # calculo del deficit en las coord de coord_turbina_selec
                for coordenada in turbina_selec.lista_coord:
                    deficit_normalizado_en_coordenada = modelo_deficit.evaluar_deficit_normalizado(
                        turbina_a_la_izquierda, coordenada, iso_s, interseccion)
                    arreglo_deficit.append(deficit_normalizado_en_coordenada)

            cantidad_coords = len(turbina_selec.lista_coord)

        # crea una instancia de Estela con los datos calculados sobre las coordenadas aleatorias
        estela_sobre_turbina_selec = Estela(arreglo_deficit, cantidad_coords, cantidad_turbinas_izquierda_de_selec)
        estela_sobre_turbina_selec.merge(metodo_superposicion)

        # Se calculan C_T C_P y Potencia de cada turbina
        turbina_selec.calcular_c_T_Int_Det(estela_sobre_turbina_selec, parque_de_turbinas.z_0, parque_de_turbinas.z_mast)
        turbina_selec.calcular_c_P_Int_Det(estela_sobre_turbina_selec, parque_de_turbinas.z_0, parque_de_turbinas.z_mast)
        turbina_selec.calcular_P_Int_Det(estela_sobre_turbina_selec, parque_de_turbinas.z_0, parque_de_turbinas.z_mast)

        # calcula el deficit generado por la turbina seleccionada (ya tiene el c_T como para hacer esto)
        # sobre la coordenada coord
        deficit_normalizado_en_coord_contribucion_turbina_selec = modelo_deficit.evaluar_deficit_normalizado(
            turbina_selec, coord)
        deficit_normalizado_en_coord.append(deficit_normalizado_en_coord_contribucion_turbina_selec)

    # crea una instancia de Estela con los datos calculados sobre coord generados por las coordenadas a
    # la izquierda
    estela_sobre_coord = Estela(deficit_normalizado_en_coord, 1, len(turbinas_a_la_izquierda_de_coord))
    estela_sobre_coord.merge(metodo_superposicion)

    # define el parametro coord de la instancia u_inf como la coord
    u_inf.coord = coord
    u_inf.perfil_flujo_base(parque_de_turbinas.z_mast, parque_de_turbinas.z_0)
    u = u_inf.coord * (1 - estela_sobre_coord.mergeada[0])
    return u
