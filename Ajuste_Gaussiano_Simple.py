import matplotlib.pyplot as plt
import numpy as np
from load_txt_datos import cargar_datos
from scipy.optimize import curve_fit

# Siempre se trabaja con x e y normalizados para no dividir por 126 en las funciones
# Funcion Gaussiana se la utiliza en el ajuste
def gauss(y, a, sigma):
    return a * np.exp(- (y ** 2) / (2 * sigma ** 2))
# Funcion lineal se la utiliza para obtener un ajuste que nos brinde los valores de k y epsilon
def rect(x, k, epsilon):
    return k*x + epsilon

ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\k-epsilon\Deficits\Caso0\Estela_1D_U.csv"
X = ['1','2','3','4','5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
# X = ['2','3','4','5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
# X = ['3','4','5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
# X = ['4','5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
# X = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
# X = ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
l_ruta = list(ruta)
l_sigma = []

for x in X:
    l_ruta[135] = x
    ruta = "".join(l_ruta)
    print(ruta)
    y, u, v, w = cargar_datos('gaussiano', ruta)

    # La funcion gaussiana es de deficits por ende normalizamos las velocidades
    u_inf = 12
    deficits = (u_inf - u) / u_inf
    ynorm = (y - 567)/126

    # Para realizar el ajuste hay que brindarle una semilla aproximada de a, mu y sigma
    n = len(ynorm)
    sigma = sum(deficits * (ynorm) ** 2) / n
    a0 = np.max(deficits)
    # popt retiene los parametros optimizados y pcov una matriz de covarianza que no utilizamos (curve fit devuelve ambas cosas)
    popt, pcov = curve_fit(gauss, ynorm, deficits, p0=[a0, sigma], bounds=(-1, 15))
    l_sigma.append(popt[1])


x_norm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
l_sigma_norm_corto = [sigma for sigma in l_sigma[4:]]
# x_norm_corto = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# x_norm_corto = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# x_norm_corto = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# x_norm_corto = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
x_norm_corto = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# x_norm_corto = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# Ajustamos la recta y obtenemos epsilon y k nuevamente se guardan en popt
popt, pcov = curve_fit(rect, x_norm_corto, l_sigma_norm_corto)
recta = [rect(x,*popt) for x in x_norm_corto]

# Grafico
plt.plot(x_norm_corto, recta, color='black', label='Ajuste 1: k=%5.6f, ϵ=%5.6f' % tuple(popt))
plt.plot(x_norm_corto, l_sigma_norm_corto,'o', color='slategray', label='Datos CFD')
plt.legend()
plt.ylabel('σ/d')
plt.xlabel('x/d')
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Ajustes\Ajustes_Lineal')
# Ajuste Gaussian
k = 0.007386505410848257
epsilon = 0.3364611586665993
x_norm_corto = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
ajusteLeyCrecimiento = [rect(x, k, epsilon) for x in x_norm_corto]
plt.plot(x_norm_corto, ajusteLeyCrecimiento, '-.', color='black', label='Ajuste 2: k=%5.6f, ϵ=%5.6f' % (k, epsilon))
plt.legend()
plt.ylabel('σ/d')
plt.xlabel('x/d')
plt.savefig(r'C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Imagenes\Imagenes Modelos Analiticos\Ajustes\Comparacion_Ajustes')
plt.show()

