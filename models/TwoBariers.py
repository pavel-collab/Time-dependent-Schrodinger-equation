#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from matplotlib.animation import PillowWriter
from datetime import datetime
import json
import argparse

from include import ShrodingerEquation, PotentialBarriers

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="set config file with model settings")

parser.add_argument("-wf", "--wavefunction", help="plot the wave function (if this key is not used there will be plot only wave package)", action="store_true")
parser.add_argument("-i", "--info", help="add the information on the plot (information about average coordinate, momentum and package sigma)", action="store_true")

parser.add_argument("-v", type=float, help="set a depth of potential pit")
parser.add_argument("-a", type=float, help="set a width of potential pit")

parser.add_argument("-s", "--sigma", type=float, help="set an initial sigma of wave package")
parser.add_argument("-e", "--energy", type=float, help="set an initial energy of wave package")
args = parser.parse_args()

config_file_name = "./configs/TwoBarriers.json"
if args.config != None:
    config_file_name = args.config

with open(config_file_name, 'r') as config_file:
    info = config_file.read()

JsonData = json.loads(info)

#----------------------------------------Plot settings----------------------------------------
# set the number of points on the space grid
N = JsonData[0]['N']
# set the grid of space range
x_start = JsonData[0]['x_start']
x_end = JsonData[0]['x_end']

x_dense, dx = np.linspace(x_start, x_end, N, retstep=True)

#----------------------------------------Wave package settings----------------------------------------
# initial coordinate
x0 = JsonData[1]['x0']
# width of wave package
if args.sigma != None:
    sigma0 = args.sigma
else:
    sigma0 = JsonData[1]['sigma0']
# initial energy and momentum (note: m = 1)
if args.energy != None:
    E0 = args.energy
else:
    E0 = JsonData[1]['E0']
p0 = math.sqrt(2*E0)

#----------------------------------------Potential barrier settings----------------------------------------
V_x0 = JsonData[1]['x0']

if args.v != None:
    V0 = args.v
else:
    V0 = JsonData[2]['V0']
if args.a != None:
    a = args.a
else:
    a = JsonData[2]['a']
    
V_dense = np.array([PotentialBarriers.BoxPotential(x, V_x0, a, V0) for x in x_dense])

# set an initial type of wave package like a Gauss wave package
psi0 = ShrodingerEquation.GaussWavePackage(x_dense, x0, sigma0, p0)

#----------------------------------------Set a psi function----------------------------------------
psi = ShrodingerEquation.WaveFunction(psi0, x_dense, V_dense)

#----------------------------------------Plot settings----------------------------------------
# set the figure, axes limits and title
fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ax.set_xlim(x_start, x_end)
ax.set_ylim(0.0, 0.12)

plt.title('Two Barriers')
plt.xlabel('x')
plt.ylabel(r'$|\psi|^2$')

# create and initial empty frame
ln1, = plt.plot([], [], label='wave package')
ln2, = plt.plot([], [], label='potential barrier')
if args.wavefunction != None:
    ln3, = plt.plot([], [], label='wave function')

# initial text box
ax.text(
    x_start+30, 0.1, '',
    size = 8,
    bbox=dict(facecolor='white', edgecolor='black', pad=10.0)
)
plt.legend(loc='upper right')

# fps and total number of frames
fps = JsonData[0]['fps']
total_frames_n = JsonData[0]['total_frames_n']

#----------------------------------------Animation function----------------------------------------
# function animate define how frames will be changed during the time
def animate(i):
    '''
    Lets explain what does it for. In matplotlib animation the animate function really wants to
    depend of i (number of frame), so, if the interpritator see that i is not used,
    it will be a warning, but in pur case we don't need to use the number of frame, so we make an
    artificial using of variable i to avoid a warnings.
    '''
    I = i
    psi.PsiTimeEvolute()
    psi_norm_factor = max(psi.WaveFunctioProbability()) / max(psi.psi.real)

    # update information about plot
    ln1.set_data(x_dense, psi.WaveFunctioProbability())
    ln2.set_data(x_dense, V_dense)
    if args.wavefunction:
        ln3.set_data(x_dense, psi.psi.real * psi_norm_factor)
    
    # update the information (if it need to be)
    if args.info != False:
        avrg_cordinate = psi.GetAvrgCordinate()
        avrg_momentum = psi.GetAvrgMomentum()
        sigma = sigma0 * math.sqrt(1 + (i/sigma0**2)**2)
        
        #update information in text box
        ax.text(
            x_start+30, 0.1, r'$\langle x \rangle =$ %0.2lf, $\langle p \rangle =$ %0.2lf, $\sigma = $ %0.2lf' 
            %(avrg_cordinate, avrg_momentum, sigma),
            size = 8,
            bbox=dict(facecolor='white', edgecolor='black', pad=10.0)
        )

def main():
    start_time = datetime.now()
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    try:
        ani = animation.FuncAnimation(fig, animate, frames=total_frames_n, interval=fps)
        # here we can save the animation like a video
        f_mp4 = r"../video/two_bariers_" + date + r"_.mp4" 
        f_gif = r"../video/two_bariers_" + date + r"_.gif"
        writervideo = animation.FFMpegWriter(fps=fps) 
        
        # We can save it as a video .mp4
        ani.save(f_mp4, writer=writervideo)
        # Or we can save it as a gif .gif
        # ani.save(f_gif, writer='pillow', dpi=500)

        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('TwoBariers.py exec time:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()
    except:
        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('TwoBariers.py exec time:\n')
        log_file.write('Program was terminated or there was some error:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()

if __name__ == '__main__':
    main()