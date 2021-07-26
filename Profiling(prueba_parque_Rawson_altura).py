from __future__ import division
import numpy as np
from numpy import exp
import matplotlib.pyplot as plt
# coding=utf-8
import io
from Frandsen import Frandsen
from Larsen import Larsen
from Jensen import Jensen
from Gaussiana import Gaussiana
from Parque_de_turbinas import Parque_de_turbinas
from Turbina_Rawson import Turbina_Rawson
from Coord import Coord
from Estela import Estela
from U_inf import U_inf
from calcular_u_en_coord_integral_de_montecarlo import calcular_u_en_coord_integral_de_montecarlo

"""

EJEMPLO DE PROFILING CON LA INTEGRAL DE MONTECARLO
Abajo se encuentra comentado como hacerlo despues de llamar la funcion calcular_u_en_coord_integral_de_montecarlo

"""

frandsen=Frandsen()
larsen=Larsen()
jensen = Jensen()
gaussiana = Gaussiana()

u_inf = U_inf()
u_inf.coord_mast = 8.2
u_inf.perfil = 'log'

N = 300

z_ground = 154

turbina_0 = Turbina_Rawson(Coord(np.array([(0),(0),260 - z_ground])))
turbina_1 = Turbina_Rawson(Coord(np.array([(-204.9),(286.1),269 - z_ground])))
turbina_2 = Turbina_Rawson(Coord(np.array([(41.9),(565.7),256 - z_ground])))
turbina_3 = Turbina_Rawson(Coord(np.array([(8.1),(870),247 - z_ground])))
turbina_4 = Turbina_Rawson(Coord(np.array([(27.2),(1195.9),241 - z_ground])))
turbina_5 = Turbina_Rawson(Coord(np.array([(-7),(1527),236 - z_ground])))
turbina_6 = Turbina_Rawson(Coord(np.array([(190.3),(1894.2),234 - z_ground])))
turbina_7 = Turbina_Rawson(Coord(np.array([(-78.8),(2222.6),234 - z_ground])))
turbina_8 = Turbina_Rawson(Coord(np.array([(414.8),(2380.9),233 - z_ground])))
turbina_9 = Turbina_Rawson(Coord(np.array([(602.4),(86.7),253 - z_ground])))
turbina_10 = Turbina_Rawson(Coord(np.array([(795.1),(386.7),253 - z_ground])))
turbina_11 = Turbina_Rawson(Coord(np.array([(965.4),(676.2),246 - z_ground])))
turbina_12 = Turbina_Rawson(Coord(np.array([(1043.8),(988.5),239 - z_ground])))
turbina_13 = Turbina_Rawson(Coord(np.array([(1202.3),(1269),235 - z_ground])))
turbina_14 = Turbina_Rawson(Coord(np.array([(1313.8),(1580.7),235 - z_ground])))
turbina_15 = Turbina_Rawson(Coord(np.array([(1362.8),(1919.5),230 - z_ground])))
turbina_16 = Turbina_Rawson(Coord(np.array([(1424.8),(2225.1),223 - z_ground])))
turbina_17 = Turbina_Rawson(Coord(np.array([(711.8),(-766.6),255 - z_ground])))
turbina_18 = Turbina_Rawson(Coord(np.array([(1107.7),(-503.6),250 - z_ground])))
turbina_19 = Turbina_Rawson(Coord(np.array([(1350.9),(-206.8),246 - z_ground])))
turbina_20 = Turbina_Rawson(Coord(np.array([(1705.8),(50.9),239 - z_ground])))
turbina_21 = Turbina_Rawson(Coord(np.array([(1949.7),(315.4),241 - z_ground])))
turbina_22 = Turbina_Rawson(Coord(np.array([(2045.2),(603.6),237 - z_ground])))
turbina_23 = Turbina_Rawson(Coord(np.array([(2256.4),(890.3),234 - z_ground])))
turbina_24 = Turbina_Rawson(Coord(np.array([(2331.4),(1210.7),229 - z_ground])))
turbina_25 = Turbina_Rawson(Coord(np.array([(2451),(1517.1),226 - z_ground])))
turbina_26 = Turbina_Rawson(Coord(np.array([(2548.5),(1800.4),224 - z_ground])))
turbina_27 = Turbina_Rawson(Coord(np.array([(2682.7),(2068.3),223 - z_ground])))
turbina_28 = Turbina_Rawson(Coord(np.array([(2816.2),(2348.8),220 - z_ground])))
turbina_29 = Turbina_Rawson(Coord(np.array([(1946.5),(-1595.2),274 - z_ground])))
turbina_30 = Turbina_Rawson(Coord(np.array([(2201.9),(-1358.8),269 - z_ground])))
turbina_31 = Turbina_Rawson(Coord(np.array([(2357.1),(-1060.7),262 - z_ground])))
turbina_32 = Turbina_Rawson(Coord(np.array([(2500.9),(-787.6),257 - z_ground])))
turbina_33 = Turbina_Rawson(Coord(np.array([(2650.9),(-516.6),251 - z_ground])))
turbina_34 = Turbina_Rawson(Coord(np.array([(2802.7),(-212.6),245 - z_ground])))
turbina_35 = Turbina_Rawson(Coord(np.array([(2909.2),(102.8),241 - z_ground])))
turbina_36 = Turbina_Rawson(Coord(np.array([(2982.2),(372.5),237 - z_ground])))
turbina_37 = Turbina_Rawson(Coord(np.array([(3173.6),(690.7),230 - z_ground])))
turbina_38 = Turbina_Rawson(Coord(np.array([(3283.3),(997.4),224 - z_ground])))
turbina_39 = Turbina_Rawson(Coord(np.array([(3432.1),(1310.3),220 - z_ground])))
turbina_40 = Turbina_Rawson(Coord(np.array([(3562.9),(1629.4),219 - z_ground])))
turbina_41 = Turbina_Rawson(Coord(np.array([(3785.2),(1931.9),214 - z_ground])))
turbina_42 = Turbina_Rawson(Coord(np.array([(3947.6),(2337.7),214 - z_ground])))

turbinas_list = [turbina_0, turbina_1, turbina_2, turbina_3, turbina_4, turbina_5,
turbina_6, turbina_7, turbina_8, turbina_9, turbina_10, turbina_11,
turbina_12, turbina_13, turbina_14, turbina_15, turbina_16, turbina_17,
turbina_18, turbina_19, turbina_20, turbina_21, turbina_22, turbina_23,
turbina_24, turbina_25, turbina_26, turbina_27, turbina_28, turbina_29,
turbina_30, turbina_31, turbina_32, turbina_33, turbina_34, turbina_35,
turbina_36, turbina_37, turbina_38, turbina_39, turbina_40, turbina_41,
turbina_42]

z_mast = turbina_7.coord.z
# z_0 de la superficie
z_0 = 0.01
parque_de_turbinas = Parque_de_turbinas(turbinas_list, z_0, z_mast)

x_o = 4200
y_o = 3000
z_o = 250

coord = Coord(np.array([x_o, y_o, z_o]))




# #Aca comienza el profiling (mas abajo esta definida una funcion que hace lo mismo y es mas facil de usar)
# import cProfile, pstats
#
# profiler=cProfile.Profile()
# profiler.enable()
# profiler.runcall(calcular_u_en_coord_integral_de_montecarlo,gaussiana, 'linear', coord, parque_de_turbinas, u_inf, N)
# stats = pstats.Stats(profiler)
# #Le saca los datos del directorio en las stats pq lo hacen dificil de leer
# stats.strip_dirs()
# #Los ordenas segun alguna de las columnas (ejemplo ncalls o cumtime)
# stats.sort_stats('cumtime')
# #imprime
# stats.print_stats()
# #imprime quien llamo a... y a quien llamo tal respectivamente.
# stats.print_callers()
# stats.print_callees()


#Aca comienza el profiling
import cProfile, pstats

def profileador(deficit,metodo,NombreDelArchivo):
    profiler = cProfile.Profile()
    profiler.enable()
    profiler.runcall(calcular_u_en_coord_integral_de_montecarlo, deficit, metodo, coord, parque_de_turbinas, u_inf, N)
    # s es para escribir el txt
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
    # Le saca los datos del directorio
    stats.strip_dirs()
    stats.print_stats()
    # Escribe el txt
    with open('%s.txt'%(NombreDelArchivo), 'w+') as f:
        f.write(s.getvalue())

profileador(gaussiana,'linear','cProfile_Gaussiana_linear.txt')
# profileador(gaussiana,'rss','cProfile_Gaussiana_rss.txt')
# profileador(gaussiana,'largest','cProfile_Gaussiana_largest.txt')
# profileador(jensen, 'linear', 'cProfile_Jensen_Linear.txt')
# profileador(jensen, 'rss', 'cProfile_Jensen_Linear.txt')
# profileador(jensen, 'largest', 'cProfile_Jensen_Linear.txt')
# profileador(larsen, 'linear', 'cProfile_Larsen_Linear.txt')
# profileador(larsen, 'rss', 'cProfile_Larsen_Linear.txt')
# profileador(larsen, 'largest', 'cProfile_Larsen_Linear.txt')
# profileador(frandsen, 'linear', 'cProfile_Frandsen_Linear.txt')
# profileador(frandsen, 'rss', 'cProfile_Frandsen_Linear.txt')
# profileador(frandsen, 'largest', 'cProfile_Frandsen_Linear.txt')


