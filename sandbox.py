from src import ShrodingerEquation
import numpy as np
import math
import ctypes

# set the number of points on the space grid
N = 2
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

# print("hamiltonian: ", psi.Hamiltonian)
# psi.PsiTimeEvolute()

#------------------------------------------------------------------------------------------------

lib = ctypes.CDLL("./libcpp.so")

# указываем, какие значения принимает C функция
lib.PsiTimeEvolution.argtypes = [
    ctypes.c_long,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
]
lib.PsiTimeEvolution.restype = ctypes.POINTER(ctypes.c_double)

# указываем, какой тип возвращает функция
lib.PsiTimeEvolution.restype = ctypes.POINTER(ctypes.c_double)

c_N = ctypes.c_long(N)
c_dx = ctypes.c_double(dx)

c_psi_real = (ctypes.c_double * N)()
c_psi_imag = (ctypes.c_double * N)()
c_V = (ctypes.c_double * N)()

for i in range(N):
    c_psi_real[i] = psi.psi.real[i]
    c_psi_imag[i] = psi.psi.imag[i]

res = lib.PsiTimeEvolution(c_N, c_dx, c_psi_real, c_psi_imag, c_V)

for i in range(10):
    print(res[i])

#------------------------------------------------------------------------------------------------

# print(psi.psi.real[:10])