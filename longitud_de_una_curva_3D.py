import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(x, y):
    return x**2 + x*y + y*2 + 1

xl = np.linspace(-1.5, 1.5, 101)
X, Y = np.meshgrid(xl, xl)
Z = f(X, Y)

t = np.linspace(0, 1, 1001)
xt = t**2*np.cos(2*np.pi*t**2)
yt = t**3*np.sin(2*np.pi*t**3)
verzravel = Z.ravel()
XY = np.stack([X.ravel(), Y.ravel()]).T
S = interpolate.LinearNDInterpolator(XY, Z.ravel())

xyt = np.stack([xt, yt]).T
St = S(xyt)

Sd = np.cumsum(np.sqrt(np.sum(np.diff(xyt, axis=0)**2, axis=1)))

axe = plt.axes(projection='3d')
axe.plot_surface(X, Y, Z, cmap='jet', alpha=0.5)
axe.plot(xt, yt, 0)
axe.plot(xt, yt, St)
axe.view_init(elev=25, azim=-45)


fig, axe = plt.subplots()
axe.plot(Sd, St[:-1])
axe.fill_between(Sd, St[:-1], alpha=0.5)
axe.grid()
plt.show()

I = np.trapz(St[:-1], Sd)
print(I)