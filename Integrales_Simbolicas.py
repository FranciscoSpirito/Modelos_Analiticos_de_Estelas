from sympy import *
from sympy import integrate, oo
from sympy.abc import r,t,y,z
from sympy import exp, ln, sin
from sympy import simplify


# # Integral A
# I1 = integrate(ln(r*sin(t)/z) * exp((-(r/D)**2)/A) * r, (r,a,b))
# I2 = simplify(integrate(I1, (t,c,d)))
# print("Integral A es")
# print(I2)
#
#
# # Integral B1
# I1 = integrate(exp((-2 * (r/D)**2)/A) * r, (r,b,c))
# I2 = simplify(integrate(I1, (t,c,d)))
# print("Integral B1 es")
# print(I2)
#
#
# # Integral B2
# I1 = integrate(exp((-(r/D)**2)/A) * exp((-(r/D)**2)/B) * r, (r,b,c))
# I2 = simplify(integrate(I1, (t,c,d)))
# print("Integral B2 es")
# print(I2)
#
#
# # Integral C
# I1 = integrate(exp((-(r/D)**2)/A) * r, (r,a,b))
# I2 = simplify(integrate(I1, (t,c,d)))
# print("Integral C es")
# print(I2)
# Integral A
D = symbols('D', positive=True)
z0 = symbols('z0', positive=True)
y0 = symbols('y0')
# Rmax = oo
Rmax = symbols('Rmax', positive=True)
zmin = symbols('zmin')
zmax = symbols('zmax', positive=True)
ymin = symbols('ymin')
ymax = symbols('ymax', positive=True)
ctej2 = symbols('ctej2', positive=True)
ctek2 = symbols('ctek2', positive=True)
D = symbols('D', positive=True)
print(evaluate(pi))

# Integral Aj
I1 = integrate(exp(-(r/D)**2 / (2*ctej2**2)) * r, (t, 0, 2*pi))
I2 = integrate(I1, (r, 0, Rmax))
print("Integral Aj es")
print(I2)

# Integral Cj1
I1 = integrate((exp(-(r/D)**2 / (2*ctej2**2)))**2 * r, (t, 0, 2*pi))
I2 = integrate(I1, (r, 0, Rmax))
print("Integral Cj1 es")
print(I2)

# Integral Cjk2
z = symbols('z')
zh = symbols('zh', positive=True)
y = symbols('y')
y0 = symbols('y0')
I1 = integrate(exp(- ((z/D)**2 + (y/D)**2) / (2*ctej2**2)) * exp(- ((z/D)**2 + ((y0-y)/D)**2) / (2*ctek2**2)), (z, -oo, oo) )
I2 = integrate(I1, (y, -oo, oo))
print("Integral Cjk2 es")
print(I2)
#  Integral Cjk2 con las turbinas alineadas
I1 = integrate(exp(- ((z/D)**2 + (y/D)**2) / (2*ctej2**2)) * exp(- ((z/D)**2 + (y/D)**2) / (2*ctek2**2)), (z, -oo, oo) )
I2 = integrate(I1, (y, -oo, oo))
print("Integral Cjk2 con turbinas alineadas es")
print(I2)



# # Integral Bj
# I1 = integrate(log(r*sin(t) / z0) * exp(-(r/D)**2 / (2*ctej2**2)) * r, (t, 0, 2*pi))
# I2 = integrate(I1, (r, 0, oo))
# print("Integral Bj en polares es")
# print(I2)
#
# I1 = integrate(log(z / z0) * exp(-(y/D**2 + z/D**2) / (2*ctej2**2)), (y, -oo, oo))
# I2 = integrate(I1, (z, -oo, +oo))
# print("Integral Bj en cartecianas es")
# print(I2)
