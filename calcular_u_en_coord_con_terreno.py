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
# iso_s: intancia de Iso_superficie, contiene la informacion sobre el flujo base
# lista_coord_normalizadas: coordenadas de un disco de radio 1 ubicado en el (0,0,0)
# lista_dAi_normalizadas: areas de los diferenciales de un disco de radio 1 ubicado en el (0,0,0)
# u_inf: instancia de U_inf, contiene la informacion del perfil de velocidades (log o cte)
# u: viento en la coordenada coord al atravezar el parque con las condiciones de entrada definidas
# estela: instancia que contiene el metodo de superposicion utilizado


def calcular_u_con_terreno(modelo_deficit, metodo_superposicion, coord, parque_de_turbinas, iso_s,
                                                lista_coord_normalizadas, lista_dAi_normalizados, u_inf):

    parque_de_turbinas.ordenar_turbinas_de_izquierda_a_derecha_con_terreno()
    turbinas_a_la_izquierda_de_coord = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord_con_terreno(coord, iso_s)
    # lista que guardara los deficits normalizados generados por todas las turbinas a la izquierda de coord
    deficit_normalizado_en_coord = []
    # Radio maximo de la "zona influyente" de interseccion con las ldc de las turbinas aguas abajo
    # (turbinas con estelas fuera de esta zona, no se tomara en cuenta su influencia)
    rmax = 500
    # Puntos dentro de la zona influyente (normalizados)
    nsamp = 21
    samp_l = np.linspace(-1, 1, nsamp)

    #  Calculo de puntos de la zona influyente cerca de la coord (samp_xy_coord)
    u_coord, v_coord, w_coord = iso_s._interp_u(coord.x, coord.y).item(), iso_s._interp_v(coord.x, coord.y).item(), iso_s._interp_w(coord.x, coord.y).item()
    muv_coord = np.sqrt(u_coord ** 2 + v_coord ** 2)
    samp_xy_coord = (np.vstack((samp_l * rmax * -v_coord / muv_coord, samp_l * rmax * u_coord / muv_coord)).T + (coord.x, coord.y)).T

    # Loop para calculo de deficits en la coordenada generado por las turbinas aguas abajo
    for turbina_selec in turbinas_a_la_izquierda_de_coord:
        if turbina_selec.c_T == None:
            turbina_selec.desnormalizar_coord_y_areas(lista_coord_normalizadas, lista_dAi_normalizados)
            turbinas_a_la_izquierda_de_turbina_selec = parque_de_turbinas.turbinas_a_la_izquierda_de_una_coord_con_terreno(turbina_selec.coord, iso_s)
            cantidad_turbinas_izquierda_de_selec = len(turbinas_a_la_izquierda_de_turbina_selec)

            #  Calculo de zona influyente de la turbina seleccionada samp_xy
            coord_xy = (turbina_selec.coord.x, turbina_selec.coord.y)
            u0, v0 = turbina_selec.U_f_base[0], turbina_selec.U_f_base[1]
            muv = np.sqrt(u0 ** 2 + v0 ** 2)
            samp_xy = (np.vstack((samp_l * rmax * -v0 / muv, samp_l * rmax * u0 / muv)).T + coord_xy).T

            # lista que guardara los deficits generados sobre las coordenadas dentro del disco de turbina_selec
            arreglo_deficit = []

            # separa el caso en el que la turbina es la 'mas a la izquierda', es decir, es la turbina que recibe
            # el viento limpio, sin verse afectado por otra turbina
            if cantidad_turbinas_izquierda_de_selec == 0:
                turbina_virtual = Turbina(turbina_selec.d_0, Coord(
                    np.array([turbina_selec.coord.x, turbina_selec.coord.y, turbina_selec.coord.z])))
                turbina_virtual.c_T = 0
                turbina_virtual.t = turbina_selec.t
                turbina_virtual.U_f_base  = turbina_selec.U_f_base
                turbinas_a_la_izquierda_de_turbina_selec = [turbina_virtual]

            # Loop para calculo de deficits en la turbina_selec generado por las turbinas aguas abajo
            for turbina_a_la_izquierda in turbinas_a_la_izquierda_de_turbina_selec:

                # calculo de interseccion con zona influyente de turbina_selec, si existe interseccion samp_l_int sera un valor normalizado entre -1 y 1
                # en caso contrario sera None
                valores_x = [ iso_s._interp_t(samp_xy[0, i], samp_xy[1 , i]).item() for i in range(len(samp_xy[0]))]
                samp_l_int = interp1d(valores_x, samp_l, kind='cubic', bounds_error=False)(turbina_a_la_izquierda.t).item()

                # calculo del deficit en las coord de la turbina_selec
                for coordenada in turbina_selec.lista_coord:
                    deficit_normalizado_en_coordenada = modelo_deficit.evaluar_deficit_normalizado(
                        turbina_a_la_izquierda, coordenada, iso_s, samp_l_int, rmax, v0, u0, muv, coord_xy)
                    arreglo_deficit.append(deficit_normalizado_en_coordenada)


            # crea una instancia de Estela con los datos calculados sobre las coordenadas aleatorias
            estela_sobre_turbina_selec = Estela(arreglo_deficit, turbina_selec.lista_coord, turbinas_a_la_izquierda_de_turbina_selec)
            estela_sobre_turbina_selec.merge_terreno(metodo_superposicion, iso_s)
            turbina_selec.u_disco = estela_sobre_turbina_selec.vel_estela

            # Se calculan C_T C_P y Potencia de cada turbina
            turbina_selec.calcular_c_T_Int_Det()
            turbina_selec.calcular_c_P_Int_Det()
            turbina_selec.calcular_P_Int_Det()

        # calcula el deficit generado por la turbina seleccionada (ya tiene el c_T como para hacer esto) sobre la coordenada coord
        # calculo de interseccion con zona influyente de coord, si existe interseccion samp_l_int_coord sera un valor normalizado entre -1 y 1
        # en caso contrario sera None
        valores_x_coord = [iso_s._interp_t(samp_xy_coord[0, i], samp_xy_coord[1, i]).item() for i in range(len(samp_xy_coord[0]))]
        samp_l_int_coord = interp1d(valores_x_coord, samp_l, kind='cubic',
                                    bounds_error=False)(turbina_selec.t)
        deficit_normalizado_en_coord_contribucion_turbina_selec = modelo_deficit.evaluar_deficit_normalizado(
            turbina_selec, coord, iso_s, samp_l_int_coord, rmax, v_coord, u_coord, muv_coord, (coord.x, coord.y))
        deficit_normalizado_en_coord.append(deficit_normalizado_en_coord_contribucion_turbina_selec)

    # crea una instancia de Estela con los datos calculados sobre coord generados por las coordenadas a
    # la izquierda
    estela_sobre_coord = Estela(deficit_normalizado_en_coord, [coord], turbinas_a_la_izquierda_de_coord)
    estela_sobre_coord.merge_terreno(metodo_superposicion, iso_s)

    # Calculo de velocidad en coord
    u = float(estela_sobre_coord.vel_estela)
    return u
