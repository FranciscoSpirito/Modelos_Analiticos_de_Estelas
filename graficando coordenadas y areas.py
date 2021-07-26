from definicion_de_espesor import  definicion_de_espesor
from coordenadas_y_areas_normalizadas import coordenadas_y_areas_normalizadas
import numpy as np
import matplotlib.pyplot as plt


list_e = []
list_N = np.arange(1,1002,100)

for n in list_N:
    e = definicion_de_espesor(n)
    lista_coord, lista_areas = coordenadas_y_areas_normalizadas(n,e)
    list_e.append(e)
    lista_coord_y = [ coordenada.y for coordenada in lista_coord ]
    lista_coord_z = [ coordenada.z for coordenada in lista_coord ]
    plt.plot(lista_coord_y,lista_coord_z,'o', linewidth=3)
    plt.xlabel(u'y', fontsize=10)
    plt.ylabel(u'z', fontsize=10)
    plt.show()

# plt.plot(list_plot_x,list_plot_y,'o', linewidth=3)
# plt.xlabel(u'N', fontsize=10)
# plt.ylabel(r'espesor', fontsize=10)
# plt.grid()
# plt.show()
