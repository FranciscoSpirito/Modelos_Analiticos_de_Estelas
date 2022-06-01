from __future__ import division
import numpy as np
from sympy import erf

class Estela(object):
    def __init__(self, deficits, coordenadas, turbinas_izquierda):
        self.deficits = deficits
        self.coordenadas = coordenadas
        self.turbinas_izquierda = turbinas_izquierda


    """
    Utiliza metodos de superposicion de estelas que utiliza el paper
    'A momentum-conserving wake superposition method for wind farm power prediction', 
    el metodo dominante y el metodo de energia cinetica propuesto en la tesis
    """
    # SIN TERRENO
    def merge_deterministica(self, metodo, u_inf):
        self.vel_estela = np.zeros(len(self.coordenadas))

        # Metodo de superposicion lineal
        if (metodo == 'Metodo_A'):
                for i in range(len(self.coordenadas)):
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma += self.deficits[i + len(self.coordenadas) * j] * u_inf.u_perfil
                    if suma < u_inf.u_perfil:
                        self.vel_estela[i] = u_inf.u_perfil - suma
                    else:
                        self.vel_estela[i] = 0

        # Metodo de superposicion cuadratico
        elif metodo == 'Metodo_B':
                for i in range(len(self.coordenadas)):
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma += self.deficits[i + len(self.coordenadas)*j]**2 * u_inf.u_perfil**2
                    raiz_suma = np.sqrt(suma)
                    if raiz_suma < u_inf.u_perfil:
                        self.vel_estela[i] = u_inf.u_perfil - raiz_suma
                    else:
                        self.vel_estela[i] = 0

        # Metodo de superposicion lineal modificado con velocidad local
        elif (metodo=='Metodo_C'):
                for i in range(len(self.coordenadas)):
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma += self.deficits[i + len(self.coordenadas) * j] * self.turbinas_izquierda[j].u_media
                    if suma < u_inf.u_perfil:
                        self.vel_estela[i] = u_inf.u_perfil - suma
                    else:
                        self.vel_estela[i] = 0

        # Metodo de superposicion cuadratico modificado con velocidad local
        elif metodo == 'Metodo_D':
                for i in range(len(self.coordenadas)):
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma += self.deficits[i + len(self.coordenadas)*j]**2 * self.turbinas_izquierda[j].u_media**2
                    raiz_suma = np.sqrt(suma)
                    if raiz_suma < u_inf.u_perfil:
                        self.vel_estela[i] = u_inf.u_perfil - raiz_suma
                    else:
                        self.vel_estela[i] = 0

        # Metodo de superposicion dominante
        elif metodo == 'Metodo_E':
            # Usando la velocidad de entrada al parque
            if len(self.turbinas_izquierda) != 0:
                for i in range(len(self.coordenadas)):
                    grupo_def = np.zeros(len(self.turbinas_izquierda))
                    for j in range(len(self.turbinas_izquierda)):
                        grupo_def[j] = self.deficits[i + len(self.coordenadas) * j]
                    self.vel_estela[i] = u_inf.u_perfil - np.max(grupo_def) * u_inf.u_perfil

        # Metodo de superposicion analitico de conservacion del momento lineal
        # Paper: A momentum-conserving wake superposition method for wind farm predictions
        elif metodo == 'Metodo_F':
            k_estrella = 0.011506
            epsilon = 0.317822
            # Obtencion de velocidad convectiva de estela Uc
            listaucj = []
            IntA = 0
            IntB = 0
            IntC = 0

            if len(self.turbinas_izquierda) == 1:
                for i in range(len(self.coordenadas)):
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        self.vel_estela[i] = u_inf.u_perfil - self.deficits[i + len(self.coordenadas)*j] * u_inf.u_perfil

            else:
                for j in range(len(self.turbinas_izquierda)):

                    # Turbina j
                    D = self.turbinas_izquierda[j].d_0
                    ulocj = self.turbinas_izquierda[j].u_media
                    ctej2 = k_estrella * (
                            abs(self.turbinas_izquierda[j].coord.x - self.coordenadas[0].x) / D) + epsilon
                    raizj = np.sqrt(1 - self.turbinas_izquierda[j].c_T / (8 * ctej2 ** 2))
                    ctej1 = (1 - raizj)

                    # velocidad convectiva local uc
                    ucj = ulocj * (0.5 + 0.5 * raizj)
                    listaucj.append(ucj)

                    # Integrales
                    Aj = 2*np.pi*D**2*ctej2**2
                    Bj = Aj
                    Cjj = (np.pi*D**2*ctej2**2)
                    Cj1 = (ucj*ulocj*ctej1)**2 * Cjj
                    IntA += ucj * ulocj * ctej1 * Aj
                    IntB += u_inf.u_perfil * ucj * ulocj * ctej1 * Bj
                    IntC += Cj1
                    # Turbina k
                    for k in range(j+1, len(self.turbinas_izquierda)):
                        if k <= len(self.turbinas_izquierda):
                            # Turbina k
                            ulock = self.turbinas_izquierda[k].u_media
                            ctek2 = k_estrella * (
                                    abs(self.turbinas_izquierda[k].coord.x - self.coordenadas[0].x) / D) + epsilon
                            raizk = np.sqrt(1 - self.turbinas_izquierda[k].c_T / (8 * ctek2 ** 2))
                            ctek1 = (1 - raizk)
                            uck = ulock * (0.5 + 0.5 * raizk)
                            y0 = float(abs(self.turbinas_izquierda[j].coord.y - self.turbinas_izquierda[k].coord.y))
                            if y0 == 0:
                                Cjk2 = np.sqrt(2)*np.pi*D**2*ctej2/(np.sqrt(1/(2*ctek2**2) + 1/(2*ctej2**2))*np.sqrt(ctej2**2/ctek2**2 + 1))
                            else:
                                Cjk2 = -np.sqrt(2)*D**3*ctej2*ctek2**2*(-np.pi*ctej2*y0*np.exp(ctej2**2*y0**2/(4*D**2*ctek2**2*(ctej2**2/2 + ctek2**2/2)))*erf(ctej2*y0/(2*D*ctek2*np.sqrt(ctej2**2/2 + ctek2**2/2)))/(2*D*ctek2*np.sqrt(ctej2**2/2 + ctek2**2/2)) - np.pi*ctej2*y0*np.exp(ctej2**2*y0**2/(4*D**2*ctek2**2*(ctej2**2/2 + ctek2**2/2)))/(2*D*ctek2*np.sqrt(ctej2**2/2 + ctek2**2/2)))*np.exp(-y0**2/(2*D**2*ctek2**2))/(y0*np.sqrt(ctej2**2/ctek2**2 + 1)) + np.sqrt(2)*D**3*ctej2*ctek2**2*(-np.pi*ctej2*y0*np.exp(ctej2**2*y0**2/(4*D**2*ctek2**2*(ctej2**2/2 + ctek2**2/2)))*erf(ctej2*y0/(2*D*ctek2*np.sqrt(ctej2**2/2 + ctek2**2/2)))/(2*D*ctek2*np.sqrt(ctej2**2/2 + ctek2**2/2)) + np.pi*ctej2*y0*np.exp(ctej2**2*y0**2/(4*D**2*ctek2**2*(ctej2**2/2 + ctek2**2/2)))/(2*D*ctek2*np.sqrt(ctej2**2/2 + ctek2**2/2)))*np.exp(-y0**2/(2*D**2*ctek2**2))/(y0*np.sqrt(ctej2**2/ctek2**2 + 1))
                            Cj2 = 2 * ucj*uck*ulocj*ulock*ctej1*ctek1 * Cjk2
                            IntC += Cj2
                # a, b, c = IntA, -IntB, IntC
                a, b, c = 1, -u_inf.u_perfil,  IntC / IntA
                Uc1 = (-b + np.sqrt(float(b**2 - 4*a*c))) / (2 * a)
                a, b, c = IntA, -IntB, IntC
                Uc11 = (-b + np.sqrt(float(b ** 2 - 4 * a * c))) / (2 * a)
                # Uc2 = (-b - np.sqrt(float(b**2 - 4*a*c))) / (2 * a)
                Uc = Uc1
                # print(Uc1, Uc2)

                # Superposicion
                for i in range(len(self.coordenadas)):
                    suma = 0
                    for j in range(len(self.turbinas_izquierda)):
                        suma += (listaucj[j]/Uc) * self.deficits[i + len(self.coordenadas)*j]
                    if suma <= 1:
                        self.vel_estela[i] = u_inf.u_perfil - suma * u_inf.u_perfil
                    else:
                        self.vel_estela[i] = 0

        # Metodo del deficit de energia cinetica de estela.
        elif metodo == 'Metodo_G':
            # Utilizando solo el deficit mas grande y la velocidad local
            # if len(self.turbinas_izquierda) != 0:
            #     for i in range(len(self.coordenadas)):
            #         grupo_def = np.zeros(len(self.turbinas_izquierda))
            #         for j in range(len(self.turbinas_izquierda)):
            #             grupo_def[j] = self.deficits[i + len(self.coordenadas) * j]
            #         i_def_max = np.where(grupo_def == np.max(grupo_def))
            #         i_def_max = int(i_def_max[0])
            #         U = self.turbinas_izquierda[i_def_max].u_media
            #         D = grupo_def[i_def_max]
            #         self.vel_estela[i] = np.sqrt((-D*(2-D)*0.5) * 2 * U**2 + U**2)

            # Utilizando solo el deficit mas grande y la velocidad de entrada al parque
            # if len(self.turbinas_izquierda) != 0:
            #     for i in range(len(self.coordenadas)):
            #         grupo_def = np.zeros(len(self.turbinas_izquierda))
            #         for j in range(len(self.turbinas_izquierda)):
            #             grupo_def[j] = self.deficits[i + len(self.coordenadas) * j]
            #         U = u_inf.u_perfil
            #         D = np.max(grupo_def)
            #         self.vel_estela[i] = np.sqrt((-D*(2-D)*0.5) * 2 * U**2 + U**2)

            # Utilizando una suma de los deficits y la velocidad de entrada al parque
            # for i in range(len(self.coordenadas)):
            #     suma = 0
            #     for j in range(len(self.turbinas_izquierda)):
            #         D = self.deficits[i + len(self.coordenadas) * j]
            #         suma += -D*(2-D)*0.5
            #     if abs(suma*2*u_inf.u_perfil**2) < u_inf.u_perfil**2:
            #         self.vel_estela[i] = np.sqrt(suma * 2 * u_inf.u_perfil**2 + u_inf.u_perfil**2)
            #     else:
            #         self.vel_estela[i] = 0

            # Utilizando una suma de los deficits y la velocidad local
            for i in range(len(self.coordenadas)):
                suma = 0
                for j in range(len(self.turbinas_izquierda)):
                    D = self.deficits[i + len(self.coordenadas) * j]
                    uloc = self.turbinas_izquierda[j].u_media
                    suma += -D*(2-D)*0.5 * uloc**2
                if abs(suma * 2) < u_inf.u_perfil**2:
                    self.vel_estela[i] = np.sqrt(suma * 2 + u_inf.u_perfil**2)
                else:
                    self.vel_estela[i] = 0






    # CON TERRENO
    def merge_terreno(self, metodo, iso_s):
        self.vel_estela = np.zeros(len(self.coordenadas))
        if metodo == 'Metodo_C':
            for i in range(len(self.coordenadas)):
                suma = 0
                u_0 = iso_s.calc_mod(self.coordenadas[i])
                for j in range(len(self.turbinas_izquierda)):
                    suma +=  self.deficits[i + len(self.coordenadas) * j] * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)
                if suma < u_0:
                    self.vel_estela[i] = u_0 - suma
                else:
                    self.vel_estela[i] = 0

        elif metodo == 'Metodo_D':
            for i in range(len(self.coordenadas)):
                suma = 0
                u_0 = iso_s.calc_mod(self.coordenadas[i])
                for j in range(len(self.turbinas_izquierda)):
                    suma += self.deficits[i + len(self.coordenadas) * j]**2 * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)**2
                raiz_suma = np.sqrt(suma)
                if raiz_suma < u_0:
                    self.vel_estela[i] = u_0 - raiz_suma
                else:
                    self.vel_estela[i] = 0

        elif metodo == 'Metodo_F':
            if len(self.turbinas_izquierda) != 0:
                    for i in range(len(self.coordenadas)):
                        grupo_def = np.zeros(len(self.turbinas_izquierda))
                        grupo_vel = np.zeros(len(self.turbinas_izquierda))
                        for j in range(len(self.turbinas_izquierda)):
                            grupo_def[j] = self.deficits[i + len(self.coordenadas)*j]
                            grupo_vel[j] = grupo_def[j] * np.linalg.norm(self.turbinas_izquierda[j].U_f_base)
                        i_def_max = np.where(grupo_def == np.max(grupo_def))
                        self.vel_estela[i] = iso_s.calc_mod(self.coordenadas[i]) - grupo_vel[i_def_max[0].item()]
                        print(self.vel_estela[i])
            else:
                self.vel_estela = iso_s.calc_mod(self.coordenadas[0])



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
