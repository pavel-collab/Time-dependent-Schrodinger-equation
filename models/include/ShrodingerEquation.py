import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.sparse import diags, spdiags
from scipy.linalg import expm
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

# TODO: попробовать с помощью sympy установить нормировочный коэффициент
class BoxWavePackage:
    __slots__ = ['__x', '__x0', '__delta0', '__p0']

    def __init__(self, x_dense, x0, delta0, p0, hight=None) -> None:
        self.__x = x_dense
        self.__x0 = x0
        self.__delta0 = delta0
        self.__p0 = p0


    def GetWavePackage(self):
        N = np.shape(self.__x)[0]
        wp = np.zeros(N)
        for i in range(N):
            if self.__x0 - self.__delta0/2 <= self.__x[i] <= self.__x0 + self.__delta0 / 2:
                wp[i] = 1 / self.__delta0
            else:
                wp[i] = 0
        return wp * np.exp(1j*self.__p0*self.__x )

'''
Class define the psi fucntion and methods that defines how psi fucntion
changed during the time.
'''
class WaveFunction:
    __slots__ = ['__x', '__V', '__N', '__dx', 'psi']

    # Define the object by initial psi function, space range and potential barrier 
    # Note, that all three initial values are arrays
    def __init__(self, psi0, x_dense, V):
        self.psi = psi0.GetWavePackage()
        self.__x = x_dense
        self.__V = V

        self.__N = np.shape(x_dense)[0]
        # Note, that we use a uniform grid
        self.__dx = x_dense[1] - x_dense[0]

    # Privet method return a matrix (like a matrix operator)
    # Note, that m = 1 and h = 1 
    def __Hamiltonian(self):
        N = self.__N
        dx = self.__dx

        L = diags([1, -2, 1], offsets=[-1, 0, 1], shape=(N, N))
        V = spdiags(self.__V, 0, N, N)

        H = - (1 / (2* dx**2)) * L + V
        return H.toarray()

    def __TimeEvolution(self, dt=1):
        H = self.__Hamiltonian()

        U = expm(-1j*H*dt)
        # make a occuracy (set a tiny values to a 0)
        U[(U.real**2 + U.imag**2) < 1e-10] = 0
        return U

    def WaveFunctioProbability(self):
        return self.psi.real**2 + self.psi.imag**2  

    # Method define how psi function changed during the time
    def PsiTimeEvolute(self):
        U = self.__TimeEvolution()
        self.psi = U @ self.psi

    @property 
    def Hamiltonian(self):
        H = self.__Hamiltonian()
        return H

    # Return an average coordinate of wave package
    def GetAvrgCordinate(self):
        # value for integration
        intgr_val = self.psi.conjugate() * self.__x * self.psi
        intgr_val = intgr_val.real

        average_x = integrate.simps(intgr_val, self.__x)
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

        average_momentum = integrate.simps(intgr_val, self.__x[:-1])
        return average_momentum