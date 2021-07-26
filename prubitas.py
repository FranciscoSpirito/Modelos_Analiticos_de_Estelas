import numpy as np
from Coord import Coord
from definicion_de_espesor import definicion_de_espesor
import matplotlib.pyplot as plt

# lista_espesores = []
# for n in range(1, 1000, 1):
#     lista_espesores.append(definicion_de_espesor(n))
#
# print(lista_espesores)
aux = np.log10(200)
lista = np.logspace(0,3,num = 100)
lista = [ round(i) for i in lista ]
print(lista)
plt.plot(lista)
plt.show()
# definicion_de_espesor(10)
