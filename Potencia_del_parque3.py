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
from gradient_free_optimizers import RandomSearchOptimizer
from gradient_free_optimizers import SimulatedAnnealingOptimizer
from gradient_free_optimizers import BayesianOptimizer

from sko.GA import GA, GA_TSP
from sko.operators import ranking, selection, crossover, mutation

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
coord_3 = np.array([(8.1),(870),247 - z_ground])
coord_4 = np.array([(27.2),(1195.9),241 - z_ground])
coord_5 = np.array([(-7),(1527),236 - z_ground])
coord_6 = np.array([(190.3),(1894.2),234 - z_ground])
coord_7 = np.array([(-78.8),(2222.6),234 - z_ground])
coord_8 = np.array([(414.8),(2380.9),233 - z_ground])
coord_9 = np.array([(602.4),(86.7),253 - z_ground])
coord_10 = np.array([(795.1),(386.7),253 - z_ground])
coord_11 = np.array([(965.4),(676.2),246 - z_ground])
coord_12 = np.array([(1043.8),(988.5),239 - z_ground])
coord_13 = np.array([(1202.3),(1269),235 - z_ground])
coord_14 = np.array([(1313.8),(1580.7),235 - z_ground])
coord_15 = np.array([(1362.8),(1919.5),230 - z_ground])
coord_16 = np.array([(1424.8),(2225.1),223 - z_ground])
coord_17 = np.array([(711.8),(-766.6),255 - z_ground])
coord_18 = np.array([(1107.7),(-503.6),250 - z_ground])
coord_19 = np.array([(1350.9),(-206.8),246 - z_ground])
coord_20 = np.array([(1705.8),(50.9),239 - z_ground])
coord_21 = np.array([(1949.7),(315.4),241 - z_ground])
coord_22 = np.array([(2045.2),(603.6),237 - z_ground])
coord_23 = np.array([(2256.4),(890.3),234 - z_ground])
coord_24 = np.array([(2331.4),(1210.7),229 - z_ground])
coord_25 = np.array([(2451),(1517.1),226 - z_ground])
coord_26 = np.array([(2548.5),(1800.4),224 - z_ground])
coord_27 = np.array([(2682.7),(2068.3),223 - z_ground])
coord_28 = np.array([(2816.2),(2348.8),220 - z_ground])
coord_29 = np.array([(1946.5),(-1595.2),274 - z_ground])
coord_30 = np.array([(2201.9),(-1358.8),269 - z_ground])
coord_31 = np.array([(2357.1),(-1060.7),262 - z_ground])
coord_32 = np.array([(2500.9),(-787.6),257 - z_ground])
coord_33 = np.array([(2650.9),(-516.6),251 - z_ground])
coord_34 = np.array([(2802.7),(-212.6),245 - z_ground])
coord_35 = np.array([(2909.2),(102.8),241 - z_ground])
coord_36 = np.array([(2982.2),(372.5),237 - z_ground])
coord_37 = np.array([(3173.6),(690.7),230 - z_ground])
coord_38 = np.array([(3283.3),(997.4),224 - z_ground])
coord_39 = np.array([(3432.1),(1310.3),220 - z_ground])
coord_40 = np.array([(3562.9),(1629.4),219 - z_ground])
coord_41 = np.array([(3785.2),(1931.9),214 - z_ground])
coord_42 = np.array([(3947.6),(2337.7),214 - z_ground])

coord_turbinas = [coord_0, coord_1, coord_2, coord_3, coord_4, coord_5,
coord_6, coord_7, coord_8, coord_9, coord_10, coord_11,
coord_12, coord_13, coord_14, coord_15, coord_16, coord_17,
coord_18, coord_19, coord_20, coord_21, coord_22, coord_23,
coord_24, coord_25, coord_26, coord_27, coord_28, coord_29,
coord_30, coord_31, coord_32, coord_33, coord_34, coord_35,
coord_36, coord_37, coord_38, coord_39, coord_40, coord_41,
coord_42]

lista_x=[]
lista_z=[]
for i in range(len(coord_turbinas)):
    lista_x.append(coord_turbinas[i][0])
    lista_x.append(coord_turbinas[i][1])
    lista_z.append(coord_turbinas[i][2])

for i in range(len(coord_turbinas)):
    lista_x.append(coord_turbinas[i][1])

z_mast = coord_0[2]
# z_0 de la superficie
z_0 = 0.01

#parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)
#lista_turbinas = turbinas_list
#print(len(lista_x))
#print(lista_x)

k=0
'''
'OPTIMIZADOR'
lista_evolucion_de_potencia=[]

for k in range(len(coord_turbinas)):
    semilla = coord_turbinas[k]
    z=semilla[2]
    paso = 2
    turbina_optimizada = k
    search_space = {
        "x1": np.arange(-10 + semilla[0], 10 + semilla[0], paso),
        "x2": np.arange(-10 + semilla[1], 10 + semilla[1], paso),
    }

    optimizacion = RandomSearchOptimizer(search_space)
    #optimizacion = SimulatedAnnealingOptimizer(search_space)
    #optimizacion = BayesianOptimizer(search_space)
    optimizacion.search(Potencia_Parque_3, n_iter=2)
    x_optim=optimizacion.best_value[0]
    y_optim=optimizacion.best_value[1]
    lista_evolucion_de_potencia.append(optimizacion.best_score)
    #actualizacion de la lista
    coord_turbinas[k]=np.array([x_optim, y_optim, z])


print(optimizacion.best_score)
puntos=np.arange(43)
plt.plot(puntos, lista_evolucion_de_potencia, 'o', label='evolucion de potencia', linewidth=3)
plt.legend(fontsize=10)
plt.xlabel(u'nro de T optimizadas', fontsize=10)
plt.ylabel(r'Potencia', fontsize=10)
plt.grid()
plt.show()
'''

lower_bound=[]
upper_bound=[]
pres=[]

iteraciones=10
poblacion=10

for i in range(86):
    lower_bound.append(min(lista_x))
    upper_bound.append(max(lista_x))
    pres.append(100)

ga = GA(func=Potencia_Parque_3, n_dim=86, size_pop=poblacion, max_iter=iteraciones, prob_mut=0.1,
        lb=lower_bound, ub=upper_bound, precision=pres)

# %% Run ga
best_x, best_y, all_y = ga.run()

#print(best_x)
print(best_y)
print(all_y)

puntos=np.arange(iteraciones)

plt.plot(puntos, all_y, 'o', label='evolucion de potencia', linewidth=3)
plt.legend(fontsize=10)
plt.xlabel(u'nro de T optimizadas', fontsize=10)
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

plt.plot(graf_pos_x, graf_pos_y, 'o', label='evolucion de potencia', linewidth=3)
plt.legend(fontsize=10)
plt.xlabel(u'X', fontsize=10)
plt.ylabel(r'Y', fontsize=10)
plt.grid()
plt.show()