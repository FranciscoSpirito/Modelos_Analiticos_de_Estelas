import matplotlib.pyplot as plt
import numpy as np
from Turbina import Turbina
from Coord import Coord

turbina_0 = Turbina(90, Coord(np.array([(0),(0),250])))
lista_n_espesores = np.arange(1,1000,10)
lista_e = []
for n in lista_n_espesores:
    lista_e.append(turbina_0.definicion_de_espesor(n))
plt.plot(lista_n_espesores,lista_e, 'o')
plt.title('Espesor Normalizado')
plt.xlabel('N')
plt.ylabel('e')
plt.show()


lista_n_coord = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
for n in lista_n_coord:
    e = turbina_0.definicion_de_espesor(n)
    lista_coord, lista_dAi = turbina_0.coordenadas_y_areas_normalizadas(n,e)
    lista_coord_y = [coordenada.y for coordenada in lista_coord]
    lista_coord_z = [coordenada.z for coordenada in lista_coord]
    plt.plot(lista_coord_y, lista_coord_z, 'o', linewidth=3)
    plt.title('N = %s'%n)
    plt.show()
plt.plot(lista_coord_y, lista_coord_z, 'o', linewidth=3)
plt.title('N = %s' % n)
plt.show()