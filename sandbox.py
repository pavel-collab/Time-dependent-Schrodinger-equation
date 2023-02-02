from src import ShrodingerEquation
import numpy as np
import math
import ctypes

# set the number of points on the space grid
N = 1000
# set the grid of space range
x_start = -120
x_end = 120

x_dense, dx = np.linspace(x_start, x_end, N, retstep=True)

# initial coordinate
x0 = 0
# width of wave package
sigma0 = 5.0
# initial energy and momentum (note: m = 1)
E0 = 0.5
p0 = math.sqrt(2*E0)

V_dense = np.zeros(N)

psi0 = ShrodingerEquation.GaussWavePackage(x_dense, x0, sigma0, p0)
psi = ShrodingerEquation.WaveFunction(psi0, x_dense, V_dense)

print(psi.Hamiltonian[:10])

# psi.PsiTimeEvolute()

lib = ctypes.CDLL("./libcpp.so")

# c_psi = psi.psi.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# print(c_psi)

# указываем, какие значения принимает C функция
lib.PsiTimeEvolution.argtypes = [
    ctypes.c_long,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
]

# указываем, какой тип возвращает функция
lib.PsiTimeEvolution.restype = ctypes.POINTER(ctypes.c_double)

c_N = ctypes.c_long(N)
c_dx = ctypes.c_double(dx)
c_psi_real = psi.psi.real.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
c_psi_imag = psi.psi.imag.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
c_V = V_dense.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

res = lib.PsiTimeEvolution(c_N, c_dx, c_psi_real, c_psi_imag, c_V)
print(res)

# print(psi.psi.real[:10])