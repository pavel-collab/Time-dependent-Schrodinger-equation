import numpy as np

'''
File contains a functions of different potential barriers. 
File should be imported to target model.
Every function return value consist of coordinate, this mean that functions work with
values, not with numpy arrays of lists.

Example how to use fucntion V(x) (x_dense -- numpy array of space range):
V_dense = np.array([V(x) for x in x_dense])
'''

#------------------------------------------------------------------------------------------

'''
Box pit.
x -- space range
x0 -- center of pit
d -- width of pit
V0 -- depth of pit. Note that in this function value V0 must be negative.
'''
def BoxBarier(x, x0, d, V0):
    if (x <= x0 - d/2 or x >= x0 + d/2):
        return 0
    else:
        return V0

'''
Parabola potential for harmonic oscillator model.
x -- space range
omega -- parabola factor
'''
def ParabolaPotential(x, omega):
    return 0.5 * omega**2 * x**2

'''
Box potential barrier for quantum tunneling.
x -- space range
x0 -- center of potential barrir
d -- width of potential barrier
V0 -- the hight of potential barrier. Note that in this fuction V0 must be positive.
'''
def BoxPotential(x, x0, d, V0):
    if (x <= x0 - d/2 or x >= x0 + d/2):
        return V0
    else:
        return 0

'''
Rump potential with start in 0.
x -- space range
k -- ramp potential factor
'''
def RampPotential(x, k):
    return k*x

'''
Step potential.
x -- space range
x0 -- coordinate of potential step
V1 -- the first value of potential
V2 -- the first value of potential
'''
def StepPotential(x, x0, V1, V2):
    if x <= x0:
        return V1
    else: 
        return V2

'''
Box potential barrier for quantum tunneling with different potential levels.
x -- space range
x0 -- center of potential barrir
d -- width of potential barrier
V0 -- the first potential level (before potential barrier)
V1 -- the second potential level (potential barrier)
V2 -- the third potential level (after potential barrier)
'''
def TwoLevelBoxPotential(x, x0, d, V0, V1, V2):
    if x <= x0 - d/2:
        return V0
    elif (x > x0 - d/2 and x < x0 + d/2):
        return V1
    else:
        return V2

'''
Two box potential parriers one by one.
x -- space range
x1 -- center of the first potential barrir
x2 -- center of the second potential barrir
d1 -- width of the first potential barrier
d2 -- width of the second potential barrier
V1 -- the hight of the first potential barrier. Note that in this fuction V0 must be positive.
V2 -- the hight of the second potential barrier.
'''
def TwoWall(x, x1, x2, d1, d2, V1, V2):
    if (x >= x1 - d1/2) and (x <= x1 + d1/2):
        return V1
    elif (x >= x2 - d2/2) and (x <= x2 + d2/2):
        return V2
    else: 
        return 0

'''
The propability of wave package to transmit the potential barrier.
The propability consists of barriers hight and width, and also of portisles energy.
E -- wave package energy
V0 -- the hight of potential barrier
a -- width of potential barrier
'''
def TransmissionProbability(E, V0, a):
    """Transmission probability of through a rectangular potential barrier."""
    k = (V0 * np.sinh(a * np.sqrt(2 * (V0 - E))))**2 / (4 * E * (V0 - E))
    return 1 / (1 + k)