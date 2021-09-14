from __future__ import division
# coding=utf-8
import numpy as np
from Coord import Coord
from U_inf import U_inf

class Turbina(object):

    def __init__(self, d_0, coord):
        self.d_0 = d_0
        self.coord = coord
        self.lista_coord = None
        self.lista_dAi = None
        self.c_T = None
        self.c_P = None
        self.estela_de_otras_turbinas = []
        self.potencia = None

    def __repr__(self):
        return "Coordenada x y z : {} {} {} ".format(self.coord.x, self.coord.y, self.coord.z)

    def c_T_tabulado(self, u):
        pass

    def c_P_tabulado(self, u):
        pass

    def P_tabulado(self, u):
        pass


    def generar_coord_random(self, N):
        coord_random_arreglo = []
        for i in range(N):
            rand_y = np.random.uniform(self.coord.y-(self.d_0/2), self.coord.y+(self.d_0/2))
            rand_z = np.random.uniform(self.coord.z-(self.d_0/2), self.coord.z+(self.d_0/2))
            coord_random = Coord(np.array([self.coord.x, rand_y, rand_z]))
            coord_random_arreglo.append(coord_random)
        return coord_random_arreglo

    def calcular_c_T_Montecarlo(self, estela, coord_random_adentro_disco, z_0, z_mast, u_inf, N):
        # estela: instancia de clase Estela
            # contiene el arreglo de deficits en un vector de
            # len = cantidad_coords_adentro_disco * cantidad_turbinas_izquierda_de_selec
        # coord_random_adentro_disco: lista de instancias de la clase Coord
            # contiene las coord random que se encuentran adentro del disco
        # z_0: float
            # rugocidad del suelo
        # u_inf: instancia de la clase U_inf
            # usara el metodo calcular_logaritmico
        # N: int
            # numero de coordenadas random que utilizamos para hacer el montecarlo

        if self.c_T is None:

            u_adentro_disco = []
            i = 0
            for coord in coord_random_adentro_disco:
                u_inf.coord = coord
                u_inf.perfil_flujo_base(z_mast, z_0)
                u = u_inf.coord * (1 - estela.mergeada[i])
                i += 1
                u_adentro_disco = np.append(u_adentro_disco, u)
            u_adentro_disco2 = u_adentro_disco ** 2
            count = sum(u_adentro_disco2)
            u_medio_disco = np.mean(u_adentro_disco)
            c_T_tab = self.c_T_tabulado(u_medio_disco)
            volume = (self.d_0)**2
            integral_u2 = (volume * count)/N
            T_turbina = c_T_tab * integral_u2   # lo dividi por (0.5 * rho) porque luego dividire por eso
            T_disponible = (u_medio_disco)**2 * (np.pi*(self.d_0/2)**2)     # lo dividi por (0.5 * rho) porque luego multiplicare por eso
            self.c_T = T_turbina / T_disponible

    def calcular_c_P_Montecarlo(self, estela, coord_random_adentro_disco, z_0, z_mast, u_inf, N):

        # estela: instancia de clase Estela
            # contiene el arreglo de deficits en un vector de
            # len = cantidad_coords_adentro_disco * cantidad_turbinas_izquierda_de_selec
        # coord_random_adentro_disco: lista de instancias de la clase Coord
            # contiene las coord random que se encuentran adentro del disco
        # z_0: float
            # rugocidad del suelo
        # u_inf: instancia de la clase U_inf
            # usara el metodo calcular_logaritmico
        # N: int
            # numero de coordenadas random que utilizamos para hacer el montecarlo

        if self.c_P is None:

            u_adentro_disco = []
            i = 0
            for coord in coord_random_adentro_disco:
                u_inf.coord = coord
                u_inf.perfil_flujo_base(z_mast, z_0)
                u = u_inf.coord * (1 - estela.mergeada[i])
                i += 1
                u_adentro_disco = np.append(u_adentro_disco, u)
            u_adentro_disco3 = u_adentro_disco ** 3
            count = sum(u_adentro_disco3)
            u_medio_disco = np.mean(u_adentro_disco)
            c_P_tab = self.c_P_tabulado(u_medio_disco)
            volume = (self.d_0)**2
            integral_u3 = (volume * count)/N
            rho = 1.225  # densidad del aire
            self.potencia = c_P_tab * integral_u3 * 0.5 * rho   # lo dividi por (0.5 * rho) porque luego dividire por eso
            P_disponible = (u_medio_disco)**3 * (np.pi*(self.d_0/2)**2)     # lo dividi por (0.5 * rho) porque luego multiplicare por eso
            self.c_P = self.potencia / (0.5 * rho * P_disponible)

    def calcular_P_Montecarlo(self, estela, coord_random_adentro_disco, z_0, z_mast, u_inf, N):

        # estela: instancia de clase Estela
            # contiene el arreglo de deficits en un vector de
            # len = cantidad_coords_adentro_disco * cantidad_turbinas_izquierda_de_selec
        # coord_random_adentro_disco: lista de instancias de la clase Coord
            # contiene las coord random que se encuentran adentro del disco
        # z_0: float
            # rugocidad del suelo
        # u_inf: instancia de la clase U_inf
            # usara el metodo calcular_logaritmico
        # N: int
            # numero de coordenadas random que utilizamos para hacer el montecarlo

        if self.potencia is None:

            u_adentro_disco = []
            i = 0
            for coord in coord_random_adentro_disco:
                u_inf.coord = coord
                u_inf.perfil_flujo_base(z_mast, z_0)
                u = u_inf.coord * (1 - estela.mergeada[i])
                i += 1
                u_adentro_disco = np.append(u_adentro_disco, u)
            u_adentro_disco3 = u_adentro_disco ** 3
            # try:
            #     u_adentro_disco3 = u_adentro_disco**3
            # except:
            #     import pdb; pdb.set_trace()
            count = sum(u_adentro_disco3)
            u_medio_disco = np.mean(u_adentro_disco)
            c_P_tab = self.c_P_tabulado(u_medio_disco)
            volume = (self.d_0)**2
            integral_u3 = (volume * count)/N
            rho = 1.225  # densidad del aire
            self.potencia = c_P_tab * integral_u3 * 0.5 * rho   # lo dividi por (0.5 * rho) porque luego dividire por eso
            P_disponible = (u_medio_disco)**3 * (np.pi*(self.d_0/2)**2)     # lo dividi por (0.5 * rho) porque luego multiplicare por eso
            self.c_P = self.potencia / (0.5 * rho * P_disponible)
            self.potencia = (10**-3) * self.c_P * 0.5 * rho * (u_medio_disco)**3 * ((self.d_0)*0.5)**2 * np.pi



    def calcular_c_T_Int_Det(self, estela, z_0, z_mast, u_inf):
        # estela: instancia de clase Estela
        # contiene el arreglo de deficits en un vector de
        # z_0: float
        # rugocidad del suelo
        # u_inf: instancia de la clase U_inf
        # usara el metodo calcular_logaritmico

        if self.c_T is None:

            u_adentro_disco = []
            i = 0
            for coord in self.lista_coord:
                u_inf.coord = coord
                u_inf.perfil_flujo_base(z_mast, z_0)
                u = u_inf.coord * (1 - estela.mergeada[i])
                i += 1
                u_adentro_disco = np.append(u_adentro_disco, u)
            u_adentro_disco2 = u_adentro_disco ** 2
            lista_para_sumatoria = u_adentro_disco2 * self.lista_dAi
            integral_u2 = sum(lista_para_sumatoria)
            u_medio_disco = np.mean(u_adentro_disco)
            c_T_tab = self.c_T_tabulado(u_medio_disco)
            T_turbina = c_T_tab * integral_u2  # lo dividi por (0.5 * rho) porque luego dividire por eso
            T_disponible = (u_medio_disco) ** 2 * (
                        np.pi * (self.d_0 / 2) ** 2)  # lo dividi por (0.5 * rho) porque luego multiplicare por eso
            self.c_T = T_turbina / T_disponible


    def calcular_c_P_Int_Det(self, estela, z_0, z_mast, u_inf):

        # estela: instancia de clase Estela
        # contiene el arreglo de deficits en un vector de
        # z_0: float, rugocidad del suelo
        # u_inf: instancia de la clase U_inf, usara el metodo calcular_logaritmico

        if self.c_P is None:

            u_adentro_disco = []
            i = 0
            for coord in self.lista_coord:
                u_inf.coord = coord
                u_inf.perfil_flujo_base(z_mast, z_0)
                u = u_inf.coord * (1 - estela.mergeada[i])
                i += 1
                u_adentro_disco = np.append(u_adentro_disco, u)
            u_adentro_disco3 = u_adentro_disco ** 3
            lista_para_sumatoria = u_adentro_disco3 * self.lista_dAi
            integral_u3 = sum(lista_para_sumatoria)
            u_medio_disco = np.mean(u_adentro_disco)
            c_P_tab = self.c_P_tabulado(u_medio_disco)
            rho = 1.225  # densidad del aire
            self.potencia = c_P_tab * integral_u3 * 0.5 * rho   # lo dividi por (0.5 * rho) porque luego dividire por eso
            P_disponible = (u_medio_disco)**3 * (np.pi*(self.d_0/2)**2)     # lo dividi por (0.5 * rho) porque luego multiplicare por eso
            self.c_P = self.potencia / (0.5 * rho * P_disponible)

    def calcular_P_Int_Det(self, estela, z_0, z_mast, u_inf):

        # estela: instancia de clase Estela
        # contiene el arreglo de deficits en un vector de
        # z_0: float, rugocidad del suelo
        # u_inf: instancia de la clase U_inf, usara el metodo calcular_logaritmico

        if self.potencia is None:

            u_adentro_disco = []
            i = 0
            for coord in self.lista_coord:
                u_inf.coord = coord
                u_inf.perfil_flujo_base(z_mast, z_0)
                u = u_inf.coord * (1 - estela.mergeada[i])
                i += 1
                u_adentro_disco = np.append(u_adentro_disco, u)
            u_adentro_disco3 = u_adentro_disco ** 3
            lista_para_sumatoria = u_adentro_disco3 * self.lista_dAi
            integral_u3 = sum(lista_para_sumatoria)
            u_medio_disco = np.mean(u_adentro_disco)
            c_P_tab = self.c_P_tabulado(u_medio_disco)
            rho = 1.225  # densidad del aire
            self.potencia = c_P_tab * integral_u3 * 0.5 * rho   # lo dividi por (0.5 * rho) porque luego dividire por eso
            P_disponible = (u_medio_disco)**3 * (np.pi*(self.d_0/2)**2)     # lo dividi por (0.5 * rho) porque luego multiplicare por eso
            self.c_P = self.potencia / (0.5 * rho * P_disponible)
            self.potencia = (10**-3) * self.c_P * 0.5 * rho * (u_medio_disco)**3 * ((self.d_0)*0.5)**2 * np.pi


    # Define el espesor que genera los diferenciales mas cuadrados con el numero de puntos elegido
    def definicion_de_espesor(self, n):
        #  n: numero de puntos
        #  factor_de_tolerancia_porcentual es la maxima diferencia que puede haber entre los arcos y el espesor
        #  expresado como porsentaje del espesor.
        #  El metodo itera desde una tolerancia del 100% hasta 1% o corta cuando queda un unico espesor que cumple con esta tolerancia

        if n == 1:
            return 1
        n_min = 4
        cantidad_max_de_discos = round(n / n_min)
        lista_de_espesores = []
        if cantidad_max_de_discos > 2:
            for factor_tolerancia_porcentual in np.arange(100, 1, -1):
                lista_de_espesores_previa = lista_de_espesores
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

                if len(lista_de_espesores) == 0:
                    lista_de_espesores_previa.reverse()
                    lista_de_espesores = lista_de_espesores_previa
                    break

                if len(lista_de_espesores) == 1:
                    break
        else:
            lista_de_espesores.append(0.5)

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
        if n == 1:
            lista_coord_normalizadas = []
            lista_coord_normalizadas.insert(0, Coord(np.array([0, 0, 0])))
            lista_dAi_normalizados = np.array(np.pi * 1)
            return lista_coord_normalizadas, lista_dAi_normalizados
        else:
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
            titta_offset = no.pi/2
            for i in range(len(lista_ri)):
                dif_titta = (2 * np.pi) / lista_n_i[i]  # Creacion del paso angular
                j = 0
                dAi_normalizado = np.pi * lista_areas_discos_dividido_pi[i] / lista_n_i[i]
                while j < lista_n_i[i]:
                    titta = j * dif_titta
                    y_i = (lista_ri[i] * np.cos(titta + titta_offset))
                    z_i = (lista_ri[i] * np.sin(titta + titta_offset))
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

        self.lista_dAi = (self.d_0/2)**2 * lista_dAi_normalizados
        self.lista_coord = []
        for coord_aux in lista_coord_normalizadas:
            coord_turbina_xi= self.coord.x + self.d_0/2 * coord_aux.x
            coord_turbina_yi = self.coord.y + self.d_0/2 * coord_aux.y
            coord_turbina_zi = self.coord.z + self.d_0/2 * coord_aux.z
            coord_turbina_i= Coord(np.array([coord_turbina_xi,coord_turbina_yi, coord_turbina_zi]))
            self.lista_coord.append(coord_turbina_i)


    def reiniciar_turbina(self):
        self.lista_coord = None
        self.lista_dAi = None
        self.c_T = None
        self.c_P = None
        self.estela_de_otras_turbinas = []
        self.potencia = None






