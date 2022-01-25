from __future__ import division
import numpy as np
# coding=utf-8

class Estela(object):
    def __init__(self, deficits, coordenadas, turbinas_izquierda):
        self.deficits = deficits
        self.coordenadas = coordenadas
        self.turbinas_izquierda = turbinas_izquierda


    """
    Utiliza metodos de superposicion de estelas que utiliza el paper
    'A momentum-conserving wake superposition method for wind farm power prediction'
    """
    # SIN TERRENO
    def merge_deterministica(self, metodo, u_inf):
        self.vel_estela = np.zeros(len(self.coordenadas))

        if (metodo=='Metodo_C'):
                for i in range(len(self.coordenadas)):
                    suma_verif = 0
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma_verif += self.deficits[i + len(self.coordenadas) * j]
                        suma += self.deficits[i + len(self.coordenadas) * j] * self.turbinas_izquierda[j].U_f_base
                    if suma_verif < 1:
                        self.vel_estela[i] = u_inf.u_perfil - suma
                    else:
                        self.vel_estela[i] = 0

        elif metodo == 'Metodo_D':
                for i in range(len(self.coordenadas)):
                    suma_verif = 0
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma_verif += np.sqrt((self.deficits[i + len(self.coordenadas)*j])**2)
                        suma += np.sqrt((self.deficits[i + len(self.coordenadas)*j])**2) * self.turbinas_izquierda[j].U_f_base
                    if suma_verif < 1:
                        self.vel_estela[i] = u_inf.u_perfil - suma
                    else:
                        self.vel_estela[i] = 0

        elif metodo == 'Metodo_Largest':
            if len(self.turbinas_izquierda) != 0:
                    for i in range(len(self.coordenadas)):
                        grupo_def = np.zeros(len(self.turbinas_izquierda))
                        grupo_vel = np.zeros(len(self.turbinas_izquierda))
                        for j in range(len(self.turbinas_izquierda)):
                            grupo_def[j] = self.deficits[i + len(self.coordenadas)*j]
                            grupo_vel[j] = grupo_def[j] * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)
                        i_def_max = np.where(grupo_def == np.max(grupo_def))
                        self.vel_estela[i] = u_inf.u_perfil - float(grupo_vel[i_def_max])

    # CON TERRENO
    def merge_terreno(self, metodo, iso_s):
        self.vel_estela = np.zeros(len(self.coordenadas))

        if metodo == 'Metodo_C':
            for i in range(len(self.coordenadas)):
                suma_verif = 0
                suma = 0
                for j in range(len(self.turbinas_izquierda)):
                    suma_verif += self.deficits[i + len(self.coordenadas) * j]
                    suma +=  self.deficits[i + len(self.coordenadas) * j] * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)
                if suma_verif < 1:
                    self.vel_estela[i] = iso_s.calc_mod(self.coordenadas[i]) - suma
                else:
                    self.vel_estela[i] = 0

        elif metodo == 'Metodo_D':
            for i in range(len(self.coordenadas)):
                suma_verif = 0
                suma = 0
                for j in range(len(self.turbinas_izquierda)):
                    suma_verif += self.deficits[i + len(self.coordenadas) * j]
                    suma += np.sqrt(self.deficits[i + len(self.coordenadas) * j]) * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)
                if suma_verif < 1:
                    self.vel_estela[i] = iso_s.calc_mod(self.coordenadas[i]) - suma
                else:
                    self.vel_estela[i] = 0

        elif metodo == 'Metodo_Largest':
            if len(self.turbinas_izquierda) != 0:
                    for i in range(len(self.coordenadas)):
                        grupo_def = np.zeros(len(self.turbinas_izquierda))
                        grupo_vel = np.zeros(len(self.turbinas_izquierda))
                        for j in range(len(self.turbinas_izquierda)):
                            grupo_def[j] = self.deficits[i + len(self.coordenadas)*j]
                            grupo_vel[j] = grupo_def[j] * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)
                        i_def_max = np.where(grupo_def == np.max(grupo_def))
                        self.vel_estela[i] = iso_s.calc_mod(self.coordenadas[i]) - float(grupo_vel[i_def_max])

    # def metodo_CLog(self, u_inf):
    #     for i in range(len(self.coordenadas)):
    #         suma_verif = 0
    #         suma = 0
    #         for j in range(len(self.turbinas_izquierda)):
    #             suma_verif += self.deficits[i + len(self.coordenadas) * j]
    #             suma += self.deficits[i + len(self.coordenadas) * j] * self.turbinas_izquierda[j].U_f_base
    #         if suma_verif < 1:
    #             self.vel_estela[i] = u_inf.u_perfil - suma
    #         else:
    #             self.vel_estela[i] = 0
    #
    # def metodo_DLog(self, u_inf):
    #         for i in range(len(self.coordenadas)):
    #             suma = 0
    #             for j in range(len(self.turbinas_izquierda)):
    #                 suma += np.sqrt((self.deficits[i + len(self.coordenadas)*j])**2)
    #             if suma < 1:
    #                 self.vel_estela[i] =u_inf.u_perfil - suma * u_inf.u_perfil
    #             else:
    #                 self.vel_estela[i] = 0
    # def merge(self, metodo):
    #     # guardara los datos de la estela luego de utilizar el metodo de merge especificado
    #     self.mergeada = np.zeros(len(self.coordenadas))
    #
    #     if (metodo=='linear'):
    #         # Itera con i j de manera de sumar los deficits*u de cada coordenada
    #         for i in range(len(self.coordenadas)):
    #             suma = 0
    #             for j in range(len(self.turbinas_izquierda)):
    #                 suma += self.deficits[i + len(self.coordenadas)*j]
    #             if suma < 1:
    #                 self.mergeada[i] = suma
    #             else:
    #                 self.mergeada[i] = 1
    #
    #     elif (metodo=='rss'):
    #         for i in range(len(self.coordenadas)):
    #             suma = 0
    #             for j in range(len(self.turbinas_izquierda)):
    #                 suma += (self.deficits[i + len(self.coordenadas)*j])**2
    #             if (suma)**0.5 < 1:
    #                 self.mergeada[i] = (suma)**0.5
    #             else:
    #                 self.mergeada[i] = 1
    #
    #     elif (metodo=='largest'):
    #         if len(self.turbinas_izquierda) != 0:
    #             for i in range(len(self.coordenadas)):
    #                 grupo = np.zeros(len(self.turbinas_izquierda))
    #                 for j in range(len(self.turbinas_izquierda)):
    #                     grupo[j] = self.deficits[i + len(self.coordenadas)*j]
    #                 self.mergeada[i] = np.max(grupo)
