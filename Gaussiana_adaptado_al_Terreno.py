import numpy as np
from Modelo import Modelo
from Iso_Superficie import Iso_Superficie


class Gaussiana_adaptado_al_Terreno(Modelo):

    def __init__(self):
        super(Gaussiana_adaptado_al_Terreno, self).__init__()

        self.k_estrella = 0.0297
        self.epsilon = 0.3281

    # turbina_a_la_izquierda: turbina aguas abajo
    # coordenada: coord dentro del disco de la turbina_selec
    # Interseecion: entre ldc de la turbina_a_la_izq y la zona influyente de la turbina_selec
    # s: longitud de la linea de corriente desde el hub de la turbina aguas arriba hasta el plano yz en la coordenada.x
    # r: distancia desde la linea central de la ldc hasta coordenada
    # sigma_dividido_d0: parametro del paper de Gaussiana sirve para dividir la cuenta en partes y quede mas legible
    # c: division de la cuenta para que quede mas legible

    def evaluar_deficit_normalizado(self, turbina_a_la_izquierda, coordenada, iso_s, samp_l_int, rmax, v0, u0, muv, coord_xy):

        # Verificamos que este dentro de la zona influyente de la turbina_selec
        if np.isnan(samp_l_int) != True:


            interseccion = (np.vstack((samp_l_int * rmax * -v0 / muv,
                                       samp_l_int * rmax * u0 / muv)).T + coord_xy).T
            s = iso_s._interp_s(coordenada.x, coordenada.y).item() - iso_s._interp_s(turbina_a_la_izquierda.coord.x, turbina_a_la_izquierda.coord.y).item()
            centro_ldc = np.array((float(interseccion[0]), float(interseccion[1]),
               iso_s._interp_z(interseccion[0], interseccion[1]).item()
               + iso_s._interp_dz(interseccion[0], interseccion[1]).item()
               - iso_s._interp_dz(turbina_a_la_izquierda.coord.x, turbina_a_la_izquierda.coord.y).item()
               + turbina_a_la_izquierda.coord.z)).T
            r = np.sqrt((coordenada.x - centro_ldc[0]) ** 2 + (coordenada.y - centro_ldc[1]) ** 2 +
                        (coordenada.z - centro_ldc[2]) ** 2)

            sigma_n_divido_d0 = (self.k_estrella * (s/turbina_a_la_izquierda.d_0) + self.epsilon)
            c = 1 - np.sqrt(1 - (turbina_a_la_izquierda.c_T / (8 * (sigma_n_divido_d0 ** 2))))
            return c * np.exp(- ((r / turbina_a_la_izquierda.d_0) ** 2) / (2 * (sigma_n_divido_d0 ** 2)))

        else:
            return 0

