import numpy as np
import matplotlib.pyplot as plt

""" Esta funcion esta para hacer graficos, el metodo usado se encuentra en la clase Turbina """

# Devuelve el espesor que genera los diferenciales mas cuadrados con el numero de puntos elegido
def definicion_de_espesor(n):
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

# list_plot_y = []
# list_plot_x = np.arange(1,1002,10)
#
# for i in list_plot_x:
#     aux = definicion_de_espesor(i)
#     list_plot_y.append(aux)
#
# plt.plot(list_plot_x,list_plot_y,'o', linewidth=3)
# plt.xlabel(u'N', fontsize=10)
# plt.ylabel(r'espesor', fontsize=10)
# plt.grid()
# plt.show()

