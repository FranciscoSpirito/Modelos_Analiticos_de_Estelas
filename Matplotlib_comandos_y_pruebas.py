import matplotlib.pyplot as plt

lista_y = [2, 4, 3, 6]
lista_y2 = [10,8,5,4.5]
lista_x = [1,2,3,4]
"""Graficamos en el mismo grafico varias listas. Todo los primero es de la primera lista y lo segundo de la segunda, color, tipo de linea, etc"""
# plt.plot(lista_x, lista_y,'ok', lista_x, lista_y2, '-g')
# plt.xlabel('Eje x')
# plt.ylabel('Eje y')
# plt.axis([1.5,5,15,505])
# plt.show()

fig_1, axes = plt.subplots(2,2, figsize=(8, 4))
axes[0,0].scatter(lista_x,lista_y)
axes[1,1].scatter(lista_x,lista_y2)
# chart_1 = fig_1.add_subplot(121)
# chart_2 = fig_1.add_subplot(122)
# chart_1.plot(lista_x,lista_y)
# chart_2.plot(lista_x,lista_y2)
plt.show()
