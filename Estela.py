from __future__ import division
import numpy as np
# coding=utf-8

# la estela sobre un disco
class Estela(object):
    def __init__(self, arreglo, cantidad_coords_adentro_disco, cantidad_turbinas_izquierda):
        self.arreglo = arreglo
        self.cantidad_coords_adentro_disco = cantidad_coords_adentro_disco
        self.cantidad_turbinas_izquierda = cantidad_turbinas_izquierda
        self.mergeada = None

    """
    Utiliza los tres metodos de superposicion de estelas que utiliza el paper
    'Limitations to the validity of single wake superposition in wind
    farm yield assessment'
    """

    def merge(self, metodo):
        # guardara los datos de la estela luego de utilizar el metodo de merge especificado
        self.mergeada = np.zeros(self.cantidad_coords_adentro_disco)

        if (metodo=='linear'):
            for i in range(self.cantidad_coords_adentro_disco):
                suma = 0
                for j in range(self.cantidad_turbinas_izquierda):
                    suma += self.arreglo[i + self.cantidad_coords_adentro_disco*j]
                if suma < 1:
                    self.mergeada[i] = suma
                else:
                    self.mergeada[i] = 1


        elif (metodo=='rss'):
            for i in range(self.cantidad_coords_adentro_disco):
                suma = 0
                for j in range(self.cantidad_turbinas_izquierda):
                    suma += (self.arreglo[i + self.cantidad_coords_adentro_disco*j])**2
                if (suma)**0.5 < 1:
                    self.mergeada[i] = (suma)**0.5
                else:
                    self.mergeada[i] = 1

        elif (metodo=='largest'):
            if self.cantidad_turbinas_izquierda != 0:
                for i in range(self.cantidad_coords_adentro_disco):
                    grupo = np.zeros(self.cantidad_turbinas_izquierda)
                    for j in range(self.cantidad_turbinas_izquierda):
                        grupo[j] = self.arreglo[i + self.cantidad_coords_adentro_disco*j]
                    self.mergeada[i] = np.max(grupo)
