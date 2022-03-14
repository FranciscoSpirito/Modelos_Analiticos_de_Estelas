import matplotlib.pyplot as plt
import numpy as np
from load_txt_datos import cargar_datos
from scipy.optimize import curve_fit

# Se utiliza para buscar el r1/2
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

# Funcion Gaussiana se la utiliza en el ajuste
def gauss(y, a, mu, sigma):
    return a * np.exp(- ((y - mu) ** 2) / (2 * sigma ** 2))


ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Caso0\Estela_1D_U.csv"
# X = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
X = ['8', '9', '10', '11', '12', '13', '14', '15', '16']
l_ruta = list(ruta)
rmedios = []
ylargo = []
deficitsdivmax = []

for x in X:
    l_ruta[116] = x
    ruta = "".join(l_ruta)
    y, u, v, w = cargar_datos('gaussiano', ruta)
    # Movemos el centro a y=0
    y = y - 567
    # La funcion gaussiana es de deficits por ende normalizamos las velocidades
    u_inf = np.max(u)
    deficits = (u_inf - u) / u_inf

    # Para realizar el ajuste hay que brindarle una semilla aproximada de a, mu y sigma
    n = len(y)
    mean = abs(sum(y * deficits) / n)
    sigma = sum(deficits * (y - mean) ** 2) / n
    a0 = np.max(deficits)

    # popt retiene los parametros optimizados y pcov una matriz de covarianza que no utilizamos (curve fit devuelve ambas cosas)
    popt, pcov = curve_fit(gauss, y, deficits, p0=[a0, mean, sigma], bounds=(0,100000))
    # Buscamos el valor r1/2 del paper aquel que cumple Deficit(r1/2) = max(Deficit)/2
    # puntos = 5000
    # y_p_chico = np.linspace(y[0], y[-1],puntos)
    # interp_gauss = [gauss(y,*popt) for y in y_p_chico[int(puntos/2):puntos]]
    # gaussmedio, index = find_nearest(interp_gauss, max(interp_gauss)/2)
    # radiomed = y_p_chico[index]
    # rmedios.append(radiomed)
    # Armamos los vectores largos q se utilizan en el ajuste mas adelante
    for ys, deficit in zip(y[250:], deficits[250:]):
        ylargo.append(ys)
        deficitsdivmax.append(deficit/max(deficits))

    plt.plot(y[250:], deficits[250:]/max(deficits), 'o', label='x = '+str(x), markersize= 0.5)


# Funcion Gaussiana para ajuste unico dependiente de x,y con parametros k,epsilon
def gauss_ke(X, k, epsilon):
    x, y = X
    return np.exp(- (((y/126) ** 2) / (2 * (k*x+epsilon) ** 2)))

# Funcion Gaussiana dependiente de y,x con parametro unico sigma para comparacion
def gauss_mod(X, sigma):
    x, y = X
    return np.exp(- (((y/126) ** 2) / (2 * sigma ** 2)))

#  Funcion Gaussiana para media Gaussiana dependiente de y y parametri unico sigma
def gauss_med(y, sigma):
    return np.exp(- ((y) ** 2) / (2 * sigma ** 2))

# Definicion de vector xlargo para complementar ylargo
# x_norm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
x_norm = [8, 9, 10, 11, 12, 13, 14, 15, 16]
xlargo  = []
for x in x_norm:
    for i in range(251):
        xlargo.append(x*126)

# Ajuste de ley de crecimiento
popt, pcov = curve_fit(gauss_ke, (xlargo, ylargo), deficitsdivmax, p0=[0.00006, 0.0025])
plt.plot(y[250:], gauss_ke((8*126, y[250:]),*popt), label='k=%f, ϵ=%f' % tuple(popt))

# Comparacion con unicamente sigma
popt, pcov = curve_fit(gauss_med, ylargo, deficitsdivmax)
ajust_def = [gauss_med(ys, *popt) for ys in y[250:]]
plt.plot(y[250:], ajust_def, label='sigma=%f' % popt)
plt.legend()
plt.xlabel('y')
plt.ylabel(r'$ΔU/ΔU_{max}$')
plt.show()





# popt, pcov = curve_fit(gauss_mod, (xlargo, ylargo), deficitsdivmax, p0=[0.00006, 0.0025])
# plt.plot(y[250:], gauss_mod((y[250:],8*126),*popt), label='k=%f, ϵ=%f' % tuple(popt))
# popt, pcov = curve_fit(gauss_mod, (xlargo, ylargo), deficitsdivmax)
# aaa = [gauss_mod((ys,8*126), float(popt[0])) for ys in y[250:]]
# plt.plot(y[250:], aaa, label='sigma=%f' % popt)


# for x in x_norm:
#     # plt.plot(y, gauss_mod((y,x*126),*popt), label='k=%f, ϵ=%f' % tuple(popt))
#     plt.plot(y, gauss_mod((y,x*126),float(popt[0])), label='sigma=%f' % popt)
# plt.show()

# l_sigma_norm = [sigma/126 for sigma in l_sigma]
# x_norm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15, 16]
# l_sigma_norm_corto = [sigma/126 for sigma in l_sigma[3:]]
# x_norm_corto = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15, 16]
# # Ajustamos la recta y obtenemos epsilon y k nuevamente se guardan en popt
# popt, pcov = curve_fit(rect, x_norm_corto, l_sigma_norm_corto)
# l_interp = [rect(x,*popt) for x in x_norm_corto]

# Grafico
# plt.plot(x_norm_corto, l_interp, label='Ajuste Lineal: k=%5.6f, ϵ=%5.6f' % tuple(popt))
# plt.plot(x_norm_corto, l_sigma_norm_corto, 'o', label='σ/d')
# plt.legend()
# plt.ylabel('σ/d')
# plt.xlabel('x/d')
# plt.show()




