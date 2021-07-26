from __future__ import division
import numpy as np
# coding=utf-8

from Modelo import Modelo
from Parque_de_turbinas import Parque_de_turbinas
from Turbina import Turbina
from Coord import Coord
from Estela import Estela

# calcular_u_en_coord:
# .INPUT
# modelo_deficit: instancia de Modelo, define la forma con la que se ajustara el perfil de la estela
# metodo_superposicion: forma en la que se superone la estela (lineal, dominante, etc)
# coord: instancia de Coord, es el punto del espacio en el que se busca calcular el viento u
# parque_de_turbinas: instancia de Parque_de_turbinas, incluye toda la informacion relevante al
# parque que perturba el flujo
# u_inf: intancia de U_inf, contiene la informacion sobre el viento de entrada
# N: orden de la integral de montecarlo
# .OUTPUT
# u: viento en la coordenada coord al atravezar el parque con las condiciones de entrada definidas

def calcular_u_en_coord_integral_de_montecarlo(modelo_deficit, metodo_superposicion, coord, parque_de_turbinas, u_inf, N):

    parque_de_turbinas.ordenar_turbinas_de_izquierda_a_derecha()
    turbinas_a_la_izquierda_de_coord = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord(coord)

    # lista que guardara los deficits normalizados generados por todas las turbinas a la izquierda de coord
    deficit_normalizado_en_coord = []

    # calcula c_T teniendo en cuenta la interaccion de las otras turbinas
    for turbina_selec in turbinas_a_la_izquierda_de_coord:
        coord_random_arreglo = turbina_selec.generar_coord_random(N)
        turbinas_a_la_izquierda_de_turbina_selec = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord(turbina_selec.coord)
        cantidad_turbinas_izquierda_de_selec = len(turbinas_a_la_izquierda_de_turbina_selec)

        # lista que guardara los deficits generados sobre las coordenadas random dentro del disco
        # de turbina selec para calcular el montecarlo
        arreglo_deficit = []

        # separa el caso en el que la turbina es la 'mas a la izquierda', es decir, es la turbina que recibe
        # el viento limpio, sin verse afectado por otra turbina
        if cantidad_turbinas_izquierda_de_selec==0:
            turbina_virtual = Turbina(turbina_selec.d_0, Coord(np.array([turbina_selec.coord.x,turbina_selec.coord.y,turbina_selec.coord.z])))
            turbina_virtual.c_T = 0
            turbinas_a_la_izquierda_de_turbina_selec = [turbina_virtual]

        for turbina in turbinas_a_la_izquierda_de_turbina_selec:

            # lista que guardara las coordenadas aleatorias que se usaran para el montecarlo
            coord_random_adentro_disco = []
            for coord_random in coord_random_arreglo:
                # si la coordenada esta contenida en el disco de la turbina seleccionada entonces calcula
                # el deficit normalizado
                if ((coord_random.y-turbina_selec.coord.y)**2 + (coord_random.z-turbina_selec.coord.z)**2 < (turbina_selec.d_0/2)**2):
                    deficit_normalizado_en_coord_random = modelo_deficit.evaluar_deficit_normalizado(turbina, coord_random)
                    # arreglo_deficit = np.append(arreglo_deficit, deficit_normalizado_en_coord_random)
                    # coord_random_adentro_disco = np.append(coord_random_adentro_disco, coord_random)
                    arreglo_deficit.append(deficit_normalizado_en_coord_random)
                    coord_random_adentro_disco.append(coord_random)
        cantidad_coords_adentro_disco = len(coord_random_adentro_disco)

        # crea una instancia de Estela con los datos calculados sobre las coordenadas aleatorias
        estela_sobre_turbina_selec = Estela(arreglo_deficit, cantidad_coords_adentro_disco, cantidad_turbinas_izquierda_de_selec)
        estela_sobre_turbina_selec.merge(metodo_superposicion)

        # Se calculan C_T C_P y Potencia de cada turbina
        turbina_selec.calcular_c_T_Montecarlo(estela_sobre_turbina_selec, coord_random_adentro_disco, parque_de_turbinas.z_0, parque_de_turbinas.z_mast, u_inf, N)
        turbina_selec.calcular_c_P_Montecarlo(estela_sobre_turbina_selec, coord_random_adentro_disco, parque_de_turbinas.z_0, parque_de_turbinas.z_mast, u_inf, N)
        turbina_selec.calcular_P_Montecarlo(estela_sobre_turbina_selec, coord_random_adentro_disco, parque_de_turbinas.z_0, parque_de_turbinas.z_mast, u_inf, N)

        # calcula el deficit generado por la turbina seleccionada (ya tiene el c_T como para hacer esto)
        # sobre la coordenada coord
        deficit_normalizado_en_coord_contribucion_turbina_selec = modelo_deficit.evaluar_deficit_normalizado(turbina_selec, coord)
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
