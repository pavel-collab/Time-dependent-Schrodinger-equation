'''examples of potential pit'''
# the method is a x function
# use 
# V_dense = np.array([V(x) for x in x_dense])

# box pit
# x -- x range, x0 -- center of pit, d -- width of pit, V0 -- depth
def BoxPotential(x, x0, d, V0):
    if (x <= x0 - d/2 or x >= x0 + d/2):
        return 0
    else:
        return V0

# Oscillator
def ParabolaPotential(x, omega):
    return 0.5 * omega**2 * x**2