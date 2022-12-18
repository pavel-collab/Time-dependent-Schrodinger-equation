import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from datetime import datetime

import ShrodingerEquation, PotentialBarriers

# зададим количество точек на пространственной сетке
N = 1000
# зададим сетку пространственного диапазона
x_start = -64
x_end = 64

x_dense, dx = np.linspace(x_start, x_end, N, retstep=True)

# зададим параметры волнового пакета
# начальное положение
x0 = -32
# ширина
sigma0 = 1
# начальная энергия и импульс (считаем что m = 1)
E0 = 0.0
p0 = math.sqrt(2*E0)

# Потерциальную параболическую потенциальную яму
omega = 1/32
V_dense = np.array([PotentialBarriers.ParabolaPotential(x, omega) for x in x_dense]) 

# зададим новую волновую функцию
# зададим начальный вид волновой функции, как гаусовский полновой пакет
psi0 = ShrodingerEquation.GaussWavePackage(x_dense, x0, sigma0, p0)
psi = ShrodingerEquation.WaveFunction(psi0, x_dense, V_dense)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
# don't forget to set an axis limits
ax.set_xlim(x_start, x_end)
ax.set_ylim(0.0, 0.5)


# next we need to create and initial empty frame
ln1, = plt.plot([], [])
ln2, = plt.plot([], [])

# number of frames per second
fps = 60
total_frames_n = 500

# define the animation function
# this function describe how we will change our frame
# i -- is a number of frame
# it's obvious that the nember of frame consists of time
def animate(i):
    # Lets explain what does it for
    # in matplotlib animation the animate function really wants to
    # depend of i (number of frame)
    # so, if the interpritator see that i is not used
    # it waise a warning
    # but in pur case we don't need to use the number of frame, so we make  an
    # artificial using of variable i to avoid a wornings
    I = i
    psi.PsiTimeEvolute()
    # update information about 1st plot
    ln1.set_data(x_dense, psi.WaveFunctioProbability())
    ln2.set_data(x_dense, V_dense)

def main():
    start_time = datetime.now()
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    try:
        ani = animation.FuncAnimation(fig, animate, frames=total_frames_n, interval=fps)
        # here we can save the animation like a video
        f = r"../video/harmonic_oscillator_" + date + r"_.mp4"  
        writervideo = animation.FFMpegWriter(fps=fps) 
        ani.save(f, writer=writervideo)

        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('HarmonicOscillator.py exec time:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()
    except:
        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('HarmonicOscillator.py exec time:\n')
        log_file.write('Program was terminated or there was some error:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()

if __name__ == '__main__':
    main()