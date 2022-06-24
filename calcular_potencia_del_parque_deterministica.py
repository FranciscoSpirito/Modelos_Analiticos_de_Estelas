from __future__ import division
import numpy as np
from Modelo import Modelo
from ParqueEolico import ParqueEolico
from Turbina import Turbina
from Coord import Coord
from Estela import Estela

# calcular_u_en_coord:
# .INPUT
# modelo_deficit: instancia de Modelo, define la forma con la que se ajustara el perfil de la estela
# metodo_superposicion: forma en la que se superone la estela (lineal, dominante, etc)
# coord: instancia de Coord, es el punto del espacio en el que se busca calcular el viento u
# parque_de_turbinas: instancia de ParqueEolico, incluye toda la informacion relevante al
# parque que perturba el flujo
# u_inf: intancia de U_inf, contiene la informacion sobre el viento de entrada
# lista_coord_normalizadas: coordenadas de un disco de radio 1 ubicado en el (0,0,0)
# lista_dAi_normalizadas: areas de los diferenciales de un disco de radio 1 ubicado en el (0,0,0)
# u: viento en la coordenada coord al atravezar el parque con las condiciones de entrada definidas
# estela: instancia que contiene el metodo de superposicion utilizado


def calcular_potencia_del_parque_integral_deterministica(modelo_deficit, metodo_superposicion, parque_de_turbinas, u_inf, lista_coord_normalizadas,lista_dAi_normalizados):

    parque_de_turbinas.ordenar_turbinas_de_izquierda_a_derecha()

    # Loop para calculo de deficits en la coordenada generado por las turbinas aguas abajo
    for turbina in parque_de_turbinas.turbinas:

        turbina.desnormalizar_coord_y_areas(lista_coord_normalizadas, lista_dAi_normalizados)
        turbinas_a_la_izquierda_de_turbina = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord(turbina.coord)

        # lista que guardara los deficits generados sobre las coordenadas dentro del disco de turbina
        arreglo_deficit = []

        # separa el caso en el que la turbina es la 'mas a la izquierda', es decir, es la turbina que recibe
        # el viento limpio, sin verse afectado por otra turbina
        if len(turbinas_a_la_izquierda_de_turbina)==0:
            turbina_virtual = Turbina(turbina.d_0, Coord(np.array([turbina.coord.x,turbina.coord.y,turbina.coord.z])))
            turbina_virtual.c_T = 0
            turbinas_a_la_izquierda_de_turbina = [turbina_virtual]
            turbina_virtual.u_media = u_inf.u_perfil

        # Loop para calculo de deficits en la turbina generado por las turbinas aguas abajo
        for turbina_a_la_izquierda in turbinas_a_la_izquierda_de_turbina:

            # calculo del deficit en las coord de coord_turbina
            for coordenada in turbina.lista_coord:
                deficit_normalizado_en_coordenada = modelo_deficit.evaluar_deficit_normalizado(turbina_a_la_izquierda, coordenada)
                arreglo_deficit.append(deficit_normalizado_en_coordenada)


        # crea una instancia de Estela con los datos calculados sobre las coordenadas
        estela_sobre_turbina = Estela(arreglo_deficit, turbina.lista_coord, turbinas_a_la_izquierda_de_turbina)
        estela_sobre_turbina.merge_deterministica(metodo_superposicion, u_inf)
        turbina.u_disco = estela_sobre_turbina.vel_estela

        # Se calculan C_T C_P y Potencia de cada turbina
        turbina.calcular_c_T_Int_Det()
        turbina.calcular_c_P_Int_Det()
        turbina.calcular_P_Int_Det()
