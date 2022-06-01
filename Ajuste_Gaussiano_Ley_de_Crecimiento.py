import matplotlib.pyplot as plt
import numpy as np
from load_txt_datos import cargar_datos
from scipy.optimize import curve_fit

# Siempre se trabaja con y normalizado y x normalizado cuando llamamos las funciones sino habria q dividir por 126
# Funcion Gaussiana se la utiliza en el ajuste
def gauss(y, a, sigma):
    return a * np.exp(- (y ** 2) / (2 * sigma ** 2))


# ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\files.Uinf12.Uref12_unif_2\postProcessing.Uinf12.Uref12\Estela_1D_U.csv"
ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\files.Uinf12.Uref12_adap\postProcessing.Uinf12.Uref12\Estela_1D_U.csv"
X = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
l_ruta = list(ruta)
rmedios = []
ylargo = []
deficitsdivmax = []

for x in X:
    # l_ruta[166] = x
    l_ruta[164] = x
    ruta = "".join(l_ruta)
    y, u, v, w = cargar_datos('gaussiano', ruta)
    # Movemos el centro a y=0 y normalizamos
    ynorm = (y - 567)/126
    # La funcion gaussiana es de deficits por ende normalizamos las velocidades
    u_inf = 12
    deficits = (u_inf - u) / u_inf

    # Para realizar el ajuste hay que brindarle una semilla aproximada de a, mu y sigma
    n = len(ynorm)
    sigma = sum(deficits * (ynorm ** 2)) / n
    a0 = np.max(deficits)

    # popt retiene los parametros optimizados y pcov una matriz de covarianza que no utilizamos (curve fit devuelve ambas cosas)
    popt, pcov = curve_fit(gauss, ynorm, deficits, p0=[a0, sigma], bounds=(-1,10))

    # Armamos los vectores largos q se utilizan en el ajuste mas adelante
    for ys, deficit in zip(ynorm[250:], deficits[250:]):
        ylargo.append(ys)
        deficitsdivmax.append(deficit/max(deficits))

    plt.plot(ynorm[250:], deficits[250:]/max(deficits), 'o', label='x = '+str(x), markersize= 0.5)


# Funcion Gaussiana para ajuste unico dependiente de x,y con parametros k,epsilon
def gauss_ke(X, k, epsilon):
    x, y = X
    return np.exp(- ((y ** 2) / (2 * (k*x+epsilon) ** 2)))

# Definicion de vector xlargo para complementar ylargo
x_norm = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
xlargo  = []
for x in x_norm:
    for i in range(251):
        xlargo.append(x)

# Ajuste de ley de crecimiento
popt, pcov = curve_fit(gauss_ke, (xlargo, ylargo), deficitsdivmax, p0=[0.008833, 0.316166])
for xu in x_norm:
    plt.plot(ynorm[250:], gauss_ke((xu, ynorm[250:]), *popt), color='green')
plt.plot(ynorm[250:], gauss_ke((5, ynorm[250:]),*popt), color='green', label='k=%f, ϵ=%f' % tuple(popt))
plt.legend(markerscale=5)
plt.xlabel('y')
plt.ylabel(r'$ΔU/ΔU_{max}$')
plt.show()



# VERIFICACION DE CURVA DE AJUSTE A 16D
CT = 0.717722980142324 #CT para 12m/s
def gaussiana(X, k, epsilon):
    x, y = X
    sigma_n = (k * x + epsilon)
    c = 1 - np.sqrt(1 - (CT / (8 * (sigma_n ** 2))))
    return c * np.exp(-(y ** 2 / (2 * (sigma_n ** 2))))


for x in X:
    # l_ruta[166] = x
    l_ruta[164] = x
    ruta = "".join(l_ruta)
    y, u, v, w = cargar_datos('gaussiano', ruta)
    # Movemos el centro a y=0 y normalizamos
    ynorm = (y - 567)/126
    # La funcion gaussiana es de deficits por ende normalizamos las velocidades
    u_inf = 12
    deficits = (u_inf - u) / u_inf
    x = int(x)
    plt.plot(ynorm, deficits,'o', color='red', markersize=0.5, label="CFD x=%f" % x)
    plt.plot(ynorm, gaussiana((x, ynorm), *popt), color='green', label='ajuste x=%f' % x)
plt.legend(fontsize=5, markerscale=10)
plt.show()


#
# ruta  = r"C:\Users\chesp\Documents\Ingenieria Mecanica\Tesis\Modelos_Analiticos_de_Estelas\Casos_tunel_de_viento\Caso0\Estela_16D_U.csv"
# y, u, v, w = cargar_datos('gaussiano', ruta)
# # La funcion gaussiana es de deficits por ende normalizamos las velocidades
# u_inf = np.max(u)
# deficits = (u_inf - u) / u_inf
# ynorm = (y - 567) / 126
# plt.plot(ynorm, deficits, label="CFD")
# plt.plot(ynorm, gaussiana((16, ynorm), *popt), color='green',label='ajuste')
# plt.legend()
# plt.show()





