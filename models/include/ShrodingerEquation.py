import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.sparse import diags, spdiags
from scipy.linalg import expm
from scipy import integrate
from numba import jit

class GaussWavePackage:
    __slots__ = [
        '__x', 
        '__x0',
        '__sigma0',
        '__p0'
    ]
    def __init__(self, x_dense, x0, sigma0, p0):
        self.__x = x_dense
        self.__x0 = x0
        self.__sigma0 = sigma0
        self.__p0 = p0

    #! учитываем, что h = 1
    def GetWavePackage(self):
        A = (2*np.pi*self.__sigma0**2)**(-0.25)
        return A*np.exp(1j*self.__p0*self.__x - ((self.__x-self.__x0)/(2*self.__sigma0))**2)   

    @property # <- применяется для гетеров   
    def sigma(self):
        return self.__sigma0

class WaveFunction:
    __slots__ = [
        '__x', 
        '__V', 
        '__N', 
        '__dx', 
        'psi'
    ]

    # инициализируем уравнение начальным значением функции
    # пространственым интервалом
    # и видом потенциального барьера
    def __init__(self, psi0, x_dense, V):
        self.psi = psi0.GetWavePackage() #! массив
        self.__x = x_dense
        self.__V = V

        self.__N = np.shape(x_dense)[0]
        # предполагаем, что сетка равномерная
        self.__dx = x_dense[1] - x_dense[0]

    # return a matrix (like a mtrix operator)
    # здесь предполагаем нормировку постоянной планка на 1
    # массу частицы m = 1
    @jit(nopython=True) 
    def __Hamiltonian(self):
        N = self.__N
        dx = self.__dx

        L = diags([1, -2, 1], offsets=[-1, 0, 1], shape=(N, N))
        V = spdiags(self.__V, 0, N, N)

        H = - (1 / (2* dx**2)) * L + V
        return H.toarray()

    @jit(nopython=True)
    def __TimeEvolution(self, dt=1):
        H = self.__Hamiltonian()

        U = expm(-1j*H*dt)
        # задаем точность -- отрубаем слишком малые элементы матрицы
        U[(U.real**2 + U.imag**2) < 1e-10] = 0
        return U

    def WaveFunctioProbability(self):
        return self.psi.real**2 + self.psi.imag**2  

    @jit(nopython=True)
    def PsiTimeEvolute(self):
        U = self.__TimeEvolution()
        self.psi = U @ self.psi

    @property # <- применяется для гетеров   
    def Hamiltonian(self):
        H = self.__Hamiltonian()
        return H

    @jit(nopython=True)
    def GetAvrgCordinate(self):
        # значение для интегрирования
        intgr_val = self.psi.conjugate() * self.__x * self.psi
        intgr_val = intgr_val.real

        average_x = integrate.simps(intgr_val, self.__x)
        return average_x

    @jit(nopython=True)
    def GetAvrgMomentum(self):
        # здесь учитывается, что h = 1
        momentum_operator2psi_funtion = -1j * (np.diff(self.psi, 1) / self.__dx)
        # значение для интегрирования
        # поскольку используемая функци np.diff возвращает массив
        # меньший на 1 длинны от исходного, то и умножать его следует
        # на массив соответствующей длинны
        # на конечный результат вычислений это особо не повлияет, поскольку нам все равно
        # в конечном итоге нужно число
        intgr_val = self.psi.conjugate()[:-1] * momentum_operator2psi_funtion
        intgr_val = np.sqrt(intgr_val.real**2 + intgr_val.imag**2)

        average_momentum = integrate.simps(intgr_val, self.__x[:-1])
        return average_momentum