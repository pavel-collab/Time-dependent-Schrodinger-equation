#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from datetime import datetime
import json
import argparse

from include import ShrodingerEquation, PotentialBarriers

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="set config file with model settings")

parser.add_argument("-wf", "--wavefunction", help="plot the wave function (if this key is not used there will be plot only wave package)", action="store_true")

parser.add_argument("-v0", type=float, help="set an initial level of potential")
parser.add_argument("-v1", type=float, help="set the first level of potential")
parser.add_argument("-v2", type=float, help="set the second level of potential")
parser.add_argument("-a", type=float, help="set a width of potential pit")

parser.add_argument("-s", "--sigma", type=float, help="set an initial sigma of wave package")
parser.add_argument("-e", "--energy", type=float, help="set an initial energy of wave package")
args = parser.parse_args()

config_file_name = "./configs/TwoLevelBoxPotential.json"
if args.config != None:
    config_file_name = args.config

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
if args.sigma != None:
    sigma0 = args.sigma
else:
    sigma0 = JsonData[1]['sigma0']
# начальная энергия и импульс (считаем что m = 1)
if args.energy != None:
    E0 = args.energy
else:
    E0 = JsonData[1]['E0']

p0 = math.sqrt(2*E0)

# Потенциальный барьер
V_x0 = JsonData[2]['V_x0']

if args.v0 != None:
    V0 = args.v0
else:
    V0 = JsonData[2]['V0']
if args.a != None:
    a = args.a
else:
    a = JsonData[2]['a']
if args.v1 != None:
    V1 = args.v1
else:
    V1 = JsonData[2]['V1']
if args.v2 != None:
    V2 = args.v2
else:
    V2 = JsonData[2]['V2']

V_dense = np.array([PotentialBarriers.TwoLevelBoxPotential(x, V_x0, a, V0, V1, V2) for x in x_dense])

# зададим новую волновую функцию
# зададим начальный вид волновой функции, как гаусовский полновой пакет
psi0 = ShrodingerEquation.GaussWavePackage(x_dense, x0, sigma0, p0)
psi = ShrodingerEquation.WaveFunction(psi0, x_dense, V_dense)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
# don't forget to set an axis limits
ax.set_xlim(x_start, x_end)
ax.set_ylim(-0.007, 0.12)


# next we need to create and initial empty frame
ln1, = plt.plot([], [], label='wave package')
ln2, = plt.plot([], [], label='potential barrier')
if args.wavefunction != None:
    ln3, = plt.plot([], [], label='wave function')

'''
Notes:
Я все еще не вполне понял, как количество фрэймов и количество фрэймов в единицу времени связаны 
со скоростью воспроизведения, потому что результаты изменения параметров крайне нелогичные.
Когда я увеличил количество отрисовываемых фрэймов, скорость пакета уменьшилась, как и надо (кажется)

Нужно еще поэксперементировать с этим.
В крайнем случае сделаю видео со скоростью 0.5-0.25 от оригинальной
'''

# number of frames per second
fps = JsonData[0]['fps']
total_frames_n = JsonData[0]['total_frames_n']

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
    psi_norm_factor = max(psi.WaveFunctioProbability()) / max(psi.psi.real)

    # вычисляем среднюю координату и средний импульс
    avrg_cordinate = psi.GetAvrgCordinate()
    avrg_momentum = psi.GetAvrgMomentum()
    # вычисляем ширину волнового пакета
    #! здесь используем номер фрэйма как меру времени
    #! изначально в методе __TimeEvolution мы учли, что dt = 1
    #! нужно выяснить, справедливо ли это
    sigma = sigma0 * math.sqrt(1 + (i/sigma0**2)**2)

    # update information about 1st plot
    ln1.set_data(x_dense, psi.WaveFunctioProbability())
    ln2.set_data(x_dense, V_dense)
    if args.wavefunction != None:
        ln3.set_data(x_dense, psi.psi.real * psi_norm_factor)

def main():
    start_time = datetime.now()
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    try:
        ani = animation.FuncAnimation(fig, animate, frames=total_frames_n, interval=fps)
        # here we can save the animation like a video
        f = r"../video/two_level_box_potential_" + date + r"_.mp4" 
        writervideo = animation.FFMpegWriter(fps=fps) 
        ani.save(f, writer=writervideo)

        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('TwoLevelBoxPotential.py exec time:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()
    except:
        exec_time = datetime.now() - start_time
        log_file = open('info.log', 'a')
        log_file.write('TwoLevelBoxPotential.py exec time:\n')
        log_file.write('Program was terminated or there was some error:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()

if __name__ == '__main__':
    main()