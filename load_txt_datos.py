import numpy as np

def cargar_datos(tipo, ruta):
    if tipo == 'isosuperficie':
        datos_isosuperficie = np.loadtxt(ruta, skiprows=2)
        x = datos_isosuperficie[:, 0]
        y = datos_isosuperficie[:, 1]
        z = datos_isosuperficie[:, 2]
        u = datos_isosuperficie[:, 3]
        v = datos_isosuperficie[:, 4]
        w = datos_isosuperficie[:, 5]

        return x, y, z, u, v, w


"""Como cargar las turbinas, faltaria pensar como ir definiendolas"""
        # elif tipo == 'coordenadas_turbinas':
        #     coordenadas_turbinas = np.loadtxt(ruta, skiprows=2)
        #     lista_de_turbinas = []
        #     for raw in coordenadas_turbinas:
        #         turbina = Turbina_Rawson(Coord(coordenadas_turbinas[raw]))
        #         lista_de_turbinas.append(turbina)
        #     return lista_de_turbinas
        #



# ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Datos_Rawson_sin_Turbinas\U_superficie_gondolas.raw"
# #  como se encuentran ordenados los datos en columnas: x  y  z  U_x  U_y  U_z
# datos_isosuperficie = np.loadtxt(ruta, skiprows=2)
# x = datos_isosuperficie[ :, 0]
# y = datos_isosuperficie[ :, 1]
# z = datos_isosuperficie[ :, 2]
# u =  datos_isosuperficie[ :, 3]
# v =  datos_isosuperficie[ :, 4]
# w =  datos_isosuperficie[ :, 5]
