#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from datetime import datetime
import json
import argparse

from include import ShrodingerEquation, PotentialBarriers

'''
Как показали эксперементы, оптимальное значение omega примерно 1/20, 1/24, 1/28
Но при этом надо сделать подходящий масштаб графика (чтобы была видна вершина волнового пакета)
'''

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="set config file with model settings")

parser.add_argument("-o", "--omega", type=float, help="set an initial 1/omega value")
# parser.add_argument("-s", "--sigma", type=float, help="set an initial sigma of wave package")
# parser.add_argument("-e", "--energy", type=float, help="set an initial energy of wave package")
args = parser.parse_args()

config_file_name = "./configs/HarmonicOscillator.json"
if args.config != None:
    config_file = args.config

with open(config_file_name, 'r') as config_file:
    info = config_file.read()

JsonData = json.loads(info)

# зададим количество точек на пространственной сетке
N = JsonData[0]['N']
# зададим сетку пространственного диапазона
x_start = JsonData[0]['x_start']
x_end = JsonData[0]['x_end']

x_dense, dx = np.linspace(x_start, x_end, N, retstep=True)

# зададим параметры волнового пакета
# начальное положение
x0 = JsonData[1]['x0']
# ширина
sigma0 = JsonData[1]['sigma0']
# начальная энергия и импульс (считаем что m = 1)
E0 = JsonData[1]['E0']
p0 = math.sqrt(2*E0)

# Потерциальную параболическую потенциальную яму
if args.omega != None:
    omega = 1 / args.omega
else:    
    omega = 1 / JsonData[2]['~omega']
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
total_frames_n = 700

#! сделаем нормировку графиков при отрисовке
psi_norm_factor = np.max(V_dense) / max(psi.WaveFunctioProbability())

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
    ln1.set_data(x_dense, psi.WaveFunctioProbability() * psi_norm_factor)
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