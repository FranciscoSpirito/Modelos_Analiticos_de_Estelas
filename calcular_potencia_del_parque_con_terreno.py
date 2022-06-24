from __future__ import division
import numpy as np
from scipy.interpolate import interp1d
from Modelo import Modelo
from ParqueEolico import ParqueEolico
from Turbina import Turbina
from Coord import Coord
from Estela import Estela
from IsoSuperficie import IsoSuperficie


# calcular_u_en_coord:
# .INPUT
# modelo_deficit: instancia de Modelo, define la forma con la que se ajustara el perfil de la estela
# metodo_superposicion: forma en la que se superone la estela (lineal, dominante, etc)
# coord: instancia de Coord, es el punto del espacio en el que se busca calcular el viento u
# parque_de_turbinas: instancia de ParqueEolico, incluye toda la informacion relevante al
# parque que perturba el flujo
# iso_s: intancia de Iso_superficie, contiene la informacion sobre el flujo base
# lista_coord_normalizadas: coordenadas de un disco de radio 1 ubicado en el (0,0,0)
# lista_dAi_normalizadas: areas de los diferenciales de un disco de radio 1 ubicado en el (0,0,0)
# u_inf: instancia de U_inf, contiene la informacion del perfil de velocidades (log o cte)
# u: viento en la coordenada coord al atravezar el parque con las condiciones de entrada definidas
# estela: instancia que contiene el metodo de superposicion utilizado


def calcular_potencia_del_parque_con_terreno(modelo_deficit, metodo_superposicion, parque_de_turbinas, iso_s,
                                                lista_coord_normalizadas, lista_dAi_normalizados):

    parque_de_turbinas.ordenar_turbinas_de_izquierda_a_derecha_con_terreno()
    # Radio maximo de la "zona influyente" de interseccion con las ldc de las turbinas aguas abajo
    # (turbinas con estelas fuera de esta zona, no se tomara en cuenta su influencia)
    rmax = 500
    # Puntos dentro de la zona influyente (normalizados)
    nsamp = 21
    samp_l = np.linspace(-1, 1, nsamp)

    # Loop para calculo de deficits en la coordenada generado por las turbinas aguas abajo
    for turbina in parque_de_turbinas.turbinas:


        turbina.desnormalizar_coord_y_areas(lista_coord_normalizadas, lista_dAi_normalizados)
        turbinas_a_la_izquierda_de_turbina = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord_con_terreno(turbina.coord, iso_s)

        #  Calculo de zona influyente de la turbina seleccionada samp_xy
        coord_xy = (turbina.coord.x, turbina.coord.y)
        u0, v0 = turbina.U_f_base[0], turbina.U_f_base[1]
        muv = np.sqrt(u0 ** 2 + v0 ** 2)
        samp_xy = (np.vstack((samp_l * rmax * -v0 / muv, samp_l * rmax * u0 / muv)).T + coord_xy).T

        # lista que guardara los deficits generados sobre las coordenadas dentro del disco de turbina
        arreglo_deficit = []

        # separa el caso en el que la turbina es la 'mas a la izquierda', es decir, es la turbina que recibe
        # el viento limpio, sin verse afectado por otra turbina
        if len(turbinas_a_la_izquierda_de_turbina) == 0:
            turbina_virtual = Turbina(turbina.d_0, Coord(
                np.array([turbina.coord.x, turbina.coord.y, turbina.coord.z])))
            turbina_virtual.c_T = 0
            turbina_virtual.t = turbina.t
            turbina_virtual.U_f_base = turbina.U_f_base
            turbinas_a_la_izquierda_de_turbina = [turbina_virtual]

        # Loop para calculo de deficits en la turbina generado por las turbinas aguas abajo
        for turbina_a_la_izquierda in turbinas_a_la_izquierda_de_turbina:

            # calculo de interseccion con zona influyente de turbina, si existe interseccion samp_l_int sera un valor normalizado entre -1 y 1
            # en caso contrario sera None
            valores_x = [ iso_s._interp_t(samp_xy[0, i], samp_xy[1 , i]).item() for i in range(len(samp_xy[0]))]
            samp_l_int = interp1d(valores_x, samp_l, kind='cubic', bounds_error=False)(turbina_a_la_izquierda.t).item()

            # calculo del deficit en las coord de la turbina
            for coordenada in turbina.lista_coord:
                deficit_normalizado_en_coordenada = modelo_deficit.evaluar_deficit_normalizado(
                    turbina_a_la_izquierda, coordenada, iso_s, samp_l_int, rmax, v0, u0, muv, coord_xy)
                arreglo_deficit.append(deficit_normalizado_en_coordenada)


        # crea una instancia de Estela con los datos calculados sobre las coordenadas aleatorias
        estela_sobre_turbina = Estela(arreglo_deficit, turbina.lista_coord, turbinas_a_la_izquierda_de_turbina)
        estela_sobre_turbina.merge_terreno(metodo_superposicion, iso_s)
        turbina.u_disco = estela_sobre_turbina.vel_estela

        # Se calculan C_T C_P y Potencia de cada turbina
        turbina.calcular_c_T_Int_Det()
        turbina.calcular_c_P_Int_Det()
        turbina.calcular_P_Int_Det()

