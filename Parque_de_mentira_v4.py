import numpy as np
import matplotlib.pyplot as plt
from calcular_u_en_coord_integral_deterministica import calcular_u_en_coord_integral_deterministica
from calcular_u_en_coord_integral_de_montecarlo import calcular_u_en_coord_integral_de_montecarlo
from Turbina_Rawson import Turbina_Rawson
from Turbina import Turbina
from Parque_de_turbinas import Parque_de_turbinas
from Coord import Coord
from U_inf import U_inf
from Jensen import Jensen
from Frandsen import Frandsen
from Gaussiana import Gaussiana
from sko.PSO import PSO
from sko.GA import GA, GA_TSP
from sko.DE import DE
from sko.operators import ranking, selection, crossover, mutation
import timeit


def Potencia_Parque_3(lista_x):
    global lista_z
    lista_turbinas=[]
    for i in range(len(lista_z)):
        x=lista_x[i]
        y=lista_x[i+len(lista_z)]
        z=lista_z[i]
        lista_turbinas.append(Turbina_Rawson(Coord(np.array([(x), (y), (z)]))))

    x_o = 10000
    y_o = 10000
    z_o = 250
    coord = Coord(np.array([x_o, y_o, z_o]))

    gaussiana = Gaussiana()

    cantidad_de_puntos = 100
    turbina_0 = Turbina_Rawson(Coord(coord_turbinas[0]))
    espesor = turbina_0.definicion_de_espesor(cantidad_de_puntos)

    lista_coord_normalizadas, lista_dAi_normalizados = turbina_0.coordenadas_y_areas_normalizadas(
        cantidad_de_puntos, espesor)

    parque_de_turbinas = Parque_de_turbinas(lista_turbinas, z_0, z_mast)
    calcular_u_en_coord_integral_deterministica(gaussiana, 'rss', coord, parque_de_turbinas, u_inf,
                                                lista_coord_normalizadas, lista_dAi_normalizados)

    potencia_parque = 0
    for turbina in lista_turbinas:
        potencia_parque += turbina.potencia


    return -potencia_parque


u_inf = U_inf()
u_inf.coord_mast = 8.2
u_inf.perfil = 'log'



z_ground = 154

coord_0 = np.array([(0),(0),260 - z_ground])
coord_1 = np.array([(-204.9),(286.1),269 - z_ground])
coord_2 = np.array([(41.9),(565.7),256 - z_ground])

coord_turbinas = [coord_0, coord_1, coord_2]

lista_x=[]
lista_z=[]
for i in range(len(coord_turbinas)):
    lista_x.append(coord_turbinas[i][0])
    lista_x.append(coord_turbinas[i][1])
    lista_z.append(coord_turbinas[i][2])

z_mast = coord_0[2]
# z_0 de la superficie
z_0 = 0.01

#parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)
#lista_turbinas = turbinas_list
#print(len(lista_x))
#print(lista_x)

k=0

lower_bound=[]
upper_bound=[]
pres=[]
lista_distanciamiento=[]

iteraciones=10
poblacion=10
n = 2*len(coord_turbinas)

distanciamiento = 1



for i in range(n):
    lower_bound.append(min(lista_x))
    upper_bound.append(max(lista_x))
    pres.append(100)
'MANUALMENTE'
condicion1 = [lambda x: (((x[0]-x[1])**2)+((x[3]-x[4])**2))-(distanciamiento**2),
             lambda x: (((x[1]-x[2])**2)+((x[4]-x[5])**2))-(distanciamiento**2),
             lambda x: (((x[0]-x[2])**2)+((x[3]-x[5])**2))-(distanciamiento**2)]
'AUTOMATICAMENTE'
condicion2=[]
for i in range(len(coord_turbinas)-1):
    k=i+1
    while k<(len(coord_turbinas)):
        #print('i_x',i)
        #print('k_x',k)
        #print('i_y',i+(len(coord_turbinas)))
        #print('k_y',k+(len(coord_turbinas)))
        condicionamiento = lambda x: (((x[i]-x[k])**2)+((x[i+(len(coord_turbinas))]-x[k+(len(coord_turbinas))])**2))-(distanciamiento**2)
        condicion2.append(condicionamiento)
        k+=1
#print(len(condicion2))
#print(condicion1)
#print(condicion2)


start = timeit.default_timer() #TEMPORIZADOR

np.random.seed(0)

ga = GA(func=Potencia_Parque_3, n_dim=n, size_pop=poblacion, max_iter=iteraciones, prob_mut=0.1,
        lb=lower_bound, ub=upper_bound, constraint_ueq=condicion1, precision=pres)
#de = DE(func=Potencia_Parque_3, n_dim=n, size_pop=poblacion, max_iter=iteraciones, prob_mut=0.1,
#        lb=lower_bound, ub=upper_bound)


# %% Run ga
best_x, best_y, all_y = ga.run()
#best_x, best_y = ga.run()




stop = timeit.default_timer()



print('Time: ', stop - start)
print(best_x)
print(best_y)
#print(all_y)

#print(Potencia_Parque_3(best_x))  #checkeo que el optimizador está haciendo lo que creo

puntos=np.arange(iteraciones)

plt.plot(puntos, all_y, 'o', label='evolucion de potencia', linewidth=3)
plt.legend(fontsize=10)
plt.xlabel(u'iteraciones', fontsize=10)
plt.ylabel(r'Potencia', fontsize=10)
plt.grid()
plt.show()


graf_pos_x=[]
graf_pos_y=[]

for i in range(len(lista_z)):
    x = best_x[i]
    y = best_x[i + len(lista_z)]
    z = lista_z[i]
    graf_pos_x.append(x)
    graf_pos_y.append(y)
    #print(i)
    #print(i + len(lista_z))

plt.plot(graf_pos_x, graf_pos_y, 'ro', label='UBICACION DE TURBINAS', linewidth=3)
plt.legend(fontsize=10)
plt.xlabel(u'X', fontsize=10)
plt.ylabel(r'Y', fontsize=10)
plt.grid()
plt.show()

prueba=((best_x[0]-best_x[1])**2)+((best_x[3]-best_x[4])**2)

print(prueba)
