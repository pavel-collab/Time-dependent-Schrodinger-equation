import numpy as np

def GaussWavePackage(x, x0, sigma0, p0):
    A = (2*np.pi*sigma0**2)**(-0.25)
    return A*np.exp(1j*p0*x - ((x-x0)/(2*sigma0))**2)

class ShrodingerEquation:
    def __init__(self, psi0, U):
        self.psi0 = psi0
        self.U = U