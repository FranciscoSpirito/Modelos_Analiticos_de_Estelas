import matplotlib.pyplot as plt
import numpy as np
from definicion_de_espesor import definicion_de_espesor
from coordenadas_y_areas_normalizadas import coordenadas_y_areas_normalizadas

lista_n_espesores = np.arange(1,1000,10)
lista_e = []
for n in lista_n_espesores:
    lista_e.append(definicion_de_espesor(n))
plt.plot(lista_n_espesores,lista_e, 'o')
plt.title('Espesor Normalizado')
plt.xlabel('N')
plt.ylabel('e')
plt.show()

figura_coordenadas, axes = plt.subplots(4,2)
lista_n_coord = [1, 5, 10, 50, 100, 200, 400, 1000]
for n in lista_n_coord:
    e = definicion_de_espesor(n)
    lista_coord, lista_dAi = coordenadas_y_areas_normalizadas(n,e)
    lista_coord_y = [coordenada.y for coordenada in lista_coord]
    lista_coord_z = [coordenada.z for coordenada in lista_coord]
    plt.plot(lista_coord_y, lista_coord_z, 'o', linewidth=3)
    plt.title('N = %s'%n)
    plt.show()