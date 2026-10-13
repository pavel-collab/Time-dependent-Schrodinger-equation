import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.sparse import diags, spdiags
from scipy.linalg import eigh_tridiagonal
from scipy import integrate

'''
Class makes a type of form of psi function like a Gauss wave package.
'''
class GaussWavePackage:
    __slots__ = ['__x', '__x0', '__sigma0', '__p0']

    def __init__(self, x_dense, x0, sigma0, p0):
        self.__x = x_dense
        self.__x0 = x0
        self.__sigma0 = sigma0
        self.__p0 = p0

    # Note, that h = 1 (where h is a Planc constant)
    def GetWavePackage(self):
        A = (2*np.pi*self.__sigma0**2)**(-0.25)
        return A*np.exp(1j*self.__p0*self.__x - ((self.__x-self.__x0)/(2*self.__sigma0))**2)   

    @property 
    def sigma(self):
        return self.__sigma0

'''
Class define the psi fucntion and methods that defines how psi fucntion
changed during the time.
'''
class WaveFunction:
    __slots__ = ['__x', '__V', '__N', '__dx', '__energies', '__states', '__phase', '__dt', 'psi']

    # Define the object by initial psi function, space range and potential barrier 
    # Note, that all three initial values are arrays
    def __init__(self, psi0, x_dense, V):
        self.psi = psi0.GetWavePackage()
        self.__x = x_dense
        self.__V = V
        self.__energies = None
        self.__states = None
        self.__phase = None
        self.__dt = None

        self.__N = np.shape(x_dense)[0]
        # Note, that we use a uniform grid
        self.__dx = x_dense[1] - x_dense[0]

    # Privet method return a matrix (like a matrix operator)
    # Note, that m = 1 and h = 1 
    def __Hamiltonian(self):
        N = self.__N
        dx = self.__dx

        L = diags([1, -2, 1], offsets=[-1, 0, 1], shape=(N, N), dtype=float)
        V = spdiags(self.__V, 0, N, N)

        H = - (1 / (2* dx**2)) * L + V
        return H.toarray()

    def __TimeEvolution(self, dt=1):
        # Сохраняем разностный гамильтониан из работы (m = hbar = 1):
        # H[j,j] = 1/dx**2 + V[j], H[j,j+1] = H[j+1,j] = -1/(2*dx**2).
        # При вещественном стационарном потенциале H симметричен и трёхдиагонален.
        # Поэтому H = Q diag(E) Q.T, где столбцы Q — собственные состояния.
        # Разложение достаточно найти один раз, передав только две диагонали.
        if self.__states is None:
            diagonal = 1 / self.__dx**2 + self.__V
            off_diagonal = np.full(self.__N - 1, -1 / (2*self.__dx**2))
            self.__energies, self.__states = eigh_tridiagonal(diagonal, off_diagonal)

        # Это та же матричная экспонента, что и в работе:
        # exp(-i*H*dt) = Q diag(exp(-i*E*dt)) Q.T.
        # Все N состояний сохраняются; малые элементы оператора не обнуляем,
        # поскольку такое обнуление нарушает унитарность и сохранение нормы.
        if self.__phase is None or self.__dt != dt:
            self.__phase = np.exp(-1j*self.__energies*dt)
            self.__dt = dt

        # c = Q.T @ psi — коэффициенты текущей волны в собственном базисе.
        # Проецируем текущую psi на каждом шаге, чтобы сохранить возможность
        # менять её извне, в том числе на месте через psi[:].
        # Q вещественна: отдельные произведения для Re и Im позволяют
        # не создавать комплексную копию матрицы размера N x N на каждом кадре.
        Q = self.__states
        coefficients = Q.T @ self.psi.real + 1j*(Q.T @ self.psi.imag)
        coefficients *= self.__phase

        # Возвращаемся к пространственной сетке: psi(t+dt) = Q @ c(t+dt).
        # Полная плотная матрица exp(-i*H*dt) больше не нужна.
        return Q @ coefficients.real + 1j*(Q @ coefficients.imag)

    def WaveFunctioProbability(self):
        return self.psi.real**2 + self.psi.imag**2  

    # Method define how psi function changed during the time
    def PsiTimeEvolute(self, dt=1):
        self.psi = self.__TimeEvolution(dt)

    @property 
    def Hamiltonian(self):
        H = self.__Hamiltonian()
        return H

    # Return an average coordinate of wave package
    def GetAvrgCordinate(self):
        # value for integration
        intgr_val = self.psi.conjugate() * self.__x * self.psi
        intgr_val = intgr_val.real

        average_x = integrate.simpson(intgr_val, x=self.__x)
        return average_x

    # Return an average momentum of wave package
    def GetAvrgMomentum(self):
        # Note, that h = 1
        momentum_operator2psi_funtion = -1j * (np.diff(self.psi, 1) / self.__dx)
        '''
        As we use a function np.diff the result array less for 1 than
        the initial, than means we have to multiply it for an array with lenght
        that less for 1 than the lenght of initial array.
        This trick don't influence for a result, cause we use this arrays to get a number
        '''
        intgr_val = self.psi.conjugate()[:-1] * momentum_operator2psi_funtion
        intgr_val = np.sqrt(intgr_val.real**2 + intgr_val.imag**2)

        average_momentum = integrate.simpson(intgr_val, x=self.__x[:-1])
        return average_momentum