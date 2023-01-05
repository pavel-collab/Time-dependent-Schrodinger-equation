#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from datetime import datetime
import json
import argparse

from include import ShrodingerEquation, PotentialBarriers

#----------------------------------------ArgumentParser----------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="set config file with model settings")

parser.add_argument("-wf", "--wavefunction", help="plot the wave function (if this key is not used there will be plot only wave package)", action="store_true")
parser.add_argument("-i", "--info", help="add the information on the plot (information about average coordinate, momentum and package sigma)", action="store_true")

args = parser.parse_args()

config_file_name = "./configs/BoxPitCompare.json"
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
#========================================Object 1========================================
# initial coordinate
x10 = JsonData[1]['x10']
# width of wave hackage
sigma10 = JsonData[1]['sigma10']
# initial energy and momentum (note: m = 1)
E10 = JsonData[1]['E10']
p10 = math.sqrt(2*E10)

#========================================Object 2========================================
# initial coordinate
x20 = JsonData[1]['x20']
# width of wave hackage
sigma20 = JsonData[1]['sigma20']
# initial energy and momentum (note: m = 1)
E20 = JsonData[1]['E20']
p20 = math.sqrt(2*E20)

#----------------------------------------Potential barrier settings----------------------------------------
#========================================Object 1========================================
V_x10 = JsonData[2]['V_x10']
V10 = JsonData[2]['V10']
a1 = JsonData[2]['a1']
V_dense1 = np.array([PotentialBarriers.BoxBarier(x, V_x10, a1, V10) for x in x_dense])

#========================================Object 2========================================
V_x20 = JsonData[2]['V_x20']
V20 = JsonData[2]['V20']
a2 = JsonData[2]['a2']
V_dense2 = np.array([PotentialBarriers.BoxBarier(x, V_x20, a2, V20) for x in x_dense])

# set an initial type of wave package like a Gauss wave package
psi01 = ShrodingerEquation.GaussWavePackage(x_dense, x10, sigma10, p10)
psi02 = ShrodingerEquation.GaussWavePackage(x_dense, x20, sigma20, p20)

#----------------------------------------Set a psi function----------------------------------------
psi1 = ShrodingerEquation.WaveFunction(psi01, x_dense, V_dense1)
psi2 = ShrodingerEquation.WaveFunction(psi02, x_dense, V_dense2)

#----------------------------------------Plot settings----------------------------------------
# set the figure, axes limits and title
fig = plt.figure(figsize=(8, 12))
ax1 = plt.subplot(2, 1, 1)
ax2 = plt.subplot(2, 1, 2)

ax1.set_xlim(x_start, x_end)
ax1.set_ylim(-0.05, 0.12)
ax2.set_xlim(x_start, x_end)
ax2.set_ylim(-0.05, 0.12)

# create and initial empty frame
ln1, = ax1.plot([], [], label='wave package')
ln2, = ax1.plot([], [], label='potential pit')
ln3, = ax2.plot([], [], label='wave package')
ln4, = ax2.plot([], [], label='potential pit')
if args.wavefunction != False:
    ln5, = ax1.plot([], [], label='wave function')
    ln6, = ax2.plot([], [], label='wave function')

# initial text box
ax1.text(
    x_start, 1, '',
    size = 8,
    bbox=dict(facecolor='white', edgecolor='black', pad=10.0)
)
# initial text box
ax2.text(
    x_start, 1, '',
    size = 8,
    bbox=dict(facecolor='white', edgecolor='black', pad=10.0)
)

plt.subplot(2, 1, 1)
plt.title('Box Pit')
plt.xlabel('x')
plt.ylabel(r'$|\psi|^2$')
plt.subplot(2, 1, 2)
plt.title('Box Pit')
plt.xlabel('x')
plt.ylabel(r'$|\psi|^2$')

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
    psi1.PsiTimeEvolute()
    psi2.PsiTimeEvolute()
    psi_norm_factor1 = max(psi1.WaveFunctioProbability()) / max(psi1.psi.real)
    psi_norm_factor2 = max(psi2.WaveFunctioProbability()) / max(psi2.psi.real)

    # update information about plot
    ln1.set_data(x_dense, psi1.WaveFunctioProbability())
    ln2.set_data(x_dense, V_dense1)
    ln3.set_data(x_dense, psi2.WaveFunctioProbability())
    ln4.set_data(x_dense, V_dense2)
    if args.wavefunction:
        ln5.set_data(x_dense, psi1.psi.real * psi_norm_factor1)
        ln6.set_data(x_dense, psi2.psi.real * psi_norm_factor2)
    
    # update the information (if it need to be)
    if args.info != False:
        avrg_cordinate1 = psi1.GetAvrgCordinate()
        avrg_momentum1 = psi1.GetAvrgMomentum()
        sigma1 = sigma10 * math.sqrt(1 + (i/sigma10**2)**2)
        
        avrg_cordinate2 = psi2.GetAvrgCordinate()
        avrg_momentum2 = psi2.GetAvrgMomentum()
        sigma2 = sigma20 * math.sqrt(1 + (i/sigma20**2)**2)

        #update information in text box
        ax1.text(
            x_start, 0.1, r'$\langle x \rangle =$ %0.2lf, $\langle p \rangle =$ %0.2lf, $\sigma = $ %0.2lf' 
            %(avrg_cordinate1, avrg_momentum1, sigma1),
            size = 8,
            bbox=dict(facecolor='white', edgecolor='black', pad=10.0)
        )
        ax2.text(
            x_start, 0.1, r'$\langle x \rangle =$ %0.2lf, $\langle p \rangle =$ %0.2lf, $\sigma = $ %0.2lf' 
            %(avrg_cordinate2, avrg_momentum2, sigma2),
            size = 8,
            bbox=dict(facecolor='white', edgecolor='black', pad=10.0)
        )

def main():
    start_time = datetime.now()
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    try:
        ani = animation.FuncAnimation(fig, animate, frames=total_frames_n, interval=fps)
        # here we can save the animation like a video
        f = r"../video/box_pit_compare_" + date + r"_.mp4" 
        writervideo = animation.FFMpegWriter(fps=fps) 
        ani.save(f, writer=writervideo)

        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('BoxPitCompare.py exec time:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()
    except:
        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('BoxPitCompare.py exec time:\n')
        log_file.write('Program was terminated or there was some error:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()

'''
Прямоугольная потенциальная яма -- оптический аналог оптически более плотной среды
То есть после ее прохождения мы должны видеть 2 волны -- которая прошла и которая отразилась
'''
if __name__ == '__main__':
    main()