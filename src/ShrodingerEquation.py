import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.sparse import diags, spdiags
from scipy.linalg import expm

#TODO: переписать уравнение Шредингера через классы, основные функции реализовать в качетве методов класса
#TODO: написать комментарии к функциям и методам там, где это необходимо
#TODO: сейчас мы в один момент времени храним лишь одно значение вектора psi. Подумать о том, чтобы хранить массив значений (множество векторов в различные моменты времени)
# хотя, вероятно, это будет затратно по памяти, так что это задача низкого приоритета
#? если выводить графики модуля psi и действительной части, то они не отнормированы между собой (имеют разную высоту). 
# понять, так ли это должно быть, если нет -- исправить, если да, придумать, как отнормировать так, 
# чтобы можно было их смотреть на одном графике
#TODO: переписать куски кода с вычислениями в обртке numba для оптимизации
#? можно ли использовать обертку numba прямо в функции animate
#TODO: придумать несколько потенциальных барьеров и потенциальных ям, посмотреть, как волновой пакет ведет себя в этих ситуациях

def GaussWavePackage(x, x0, sigma0, p0):
    A = (2*np.pi*sigma0**2)**(-0.25)
    return A*np.exp(1j*p0*x - ((x-x0)/(2*sigma0))**2)

class WaveFunction:
    __slots__ = ['__x', '__V', '__N', '__dx', 'psi']

    # инициализируем уравнение начальным значением функции
    # пространственым интервалом
    # и видом потенциального барьера
    def __init__(self, psi0, x_dense, V):
        self.psi = psi0
        self.__x = x_dense
        self.__V = V

        self.__N = np.shape(x_dense)[0]
        # предполагаем, что сетка равномерная
        self.__dx = x_dense[1] - x_dense[0]

    # return a matrix (like a mtrix operator)
    # здесь предполагаем нормировку постоянной планка на 1
    # массу частицы m = 1 
    def __Hamiltonian(self):
        N = self.__N
        dx = self.__dx

        L = diags([1, -2, 1], offsets=[-1, 0, 1], shape=(N, N))
        V = spdiags(self.__V, 0, N, N)

        H = - (1 / (2* dx**2)) * L + V
        return H.toarray()

    def __TimeEvolution(self, dt=1):
        H = self.Hamiltonian()

        U = expm(-1j*H*dt)
        # задаем точность -- отрубаем слишком малые элементы матрицы
        U[(U.real**2 + U.imag**2) < 1e-10] = 0
        return U

    def WaveFunctioProbability(self):
        return self.psi.real**2 + self.psi.imag**2  

    def PsiTimeEvolute(self):
        U = self.__TimeEvolution()
        self.psi = U @ self.psi