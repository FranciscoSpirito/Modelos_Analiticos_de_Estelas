import numpy as np

def calculo_de_desplazamiento_vertical(x,y):




























# from scipy import interpolate
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def f(x, y):
#     return x**2 + x*y + y*2 + 1
#
# xl = np.linspace(-1.5, 1.5, 101)
# X, Y = np.meshgrid(xl, xl)
# Z = f(X, Y)
#
# titta = np.linspace(0, 1, 360)
# xt = 1*np.cos(titta)
# yt = 1*np.sin(titta)
# verzravel = Z.ravel()
# XY = np.stack([X.ravel(), Y.ravel()]).T
# S = interpolate.LinearNDInterpolator(XY, Z.ravel())
#
# xyt = np.stack([xt, yt]).T
# St = S(xyt)
#
# Sd = np.cumsum(np.sqrt(np.sum(np.diff(xyt, axis=0)**2, axis=1)))
#
# axe = plt.axes(projection='3d')
# axe.plot_surface(X, Y, Z, cmap='jet', alpha=0.5)
# axe.plot(xt, yt, 0)
# axe.plot(xt, yt, St)
# axe.view_init(elev=25, azim=-45)
#
#
# fig, axe = plt.subplots()
# axe.plot(Sd, St[:-1])
# axe.fill_between(Sd, St[:-1], alpha=0.5)
# axe.grid()
# plt.show()
#
# I = np.trapz(St[:-1], Sd)
# print(I)