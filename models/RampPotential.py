#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from datetime import datetime
import json
import argparse
from pathlib import Path

from include import ShrodingerEquation, PotentialBarriers, AnimationStyle

AnimationStyle.SetStyle()

#----------------------------------------ArgumentParser----------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="set config file with model settings")

parser.add_argument("-wf", "--wavefunction", help="plot the wave function (if this key is not used there will be plot only wave package)", action="store_true")
parser.add_argument("-i", "--info", help="add the information on the plot (information about average coordinate, momentum and package sigma)", action="store_true")

parser.add_argument("-k", type=float, help="set a 1/k value (slope of ramp potetntial)")
parser.add_argument("-s", "--sigma", type=float, help="set an initial sigma of wave package")
parser.add_argument("-e", "--energy", type=float, help="set an initial energy of wave package")
AnimationStyle.AddArguments(parser)
args = parser.parse_args()

config_file_name = Path(__file__).parent / "configs/RampPotential.json"
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
if args.k != None:   
    k = 1 / args.k
else:
    k = 1 / JsonData[2]['~k']
    
V_dense = np.array([PotentialBarriers.RampPotential(x, k) for x in x_dense])

# set an initial type of wave package like a Gauss wave package
psi0 = ShrodingerEquation.GaussWavePackage(x_dense, x0, sigma0, p0)

#----------------------------------------Set a psi function----------------------------------------
psi = ShrodingerEquation.WaveFunction(psi0, x_dense, V_dense)

#----------------------------------------Plot settings----------------------------------------
# set the figure, axes limits and title
fig, ax = plt.subplots(1, 1, figsize=(32/3, 6))

ax.set_xlim(x_start, x_end)
ax.set_ylim(0.0, 3)

plt.title('Ramp potential')
plt.xlabel('x')
plt.ylabel(r'$|\psi|^2$')

# create and initial empty frame
ln1, = plt.plot([], [], label='wave package')
ln2, = plt.plot([], [], label='potential barrier')
if args.wavefunction != False:
    ln3, = plt.plot([], [], label='wave function')

plt.legend(loc='upper right')

peak = max(psi.WaveFunctioProbability())
psi_norm_factor = peak / max(abs(psi.psi.real))
info_text = AnimationStyle.StyleAxes(ax, x_dense, V_dense, args=args, peak=peak)
AnimationStyle.LayoutFigure(fig, args)

# fps and total number of frames
fps, total_frames_n, dt = AnimationStyle.FrameSettings(JsonData[0], args)

# norm factor for wave function
psi_norm_factor = np.max(V_dense) / max(psi.WaveFunctioProbability())

#----------------------------------------Animation function----------------------------------------
# function animate define how frames will be changed during the time
def animate(i, evolve=True):
    if evolve:
        psi.PsiTimeEvolute(dt)

    # update information about plot
    ln1.set_data(x_dense, psi.WaveFunctioProbability() * psi_norm_factor)
    ln2.set_data(x_dense, V_dense)
    if args.wavefunction:
        wf_norm_factor = (max(psi.WaveFunctioProbability() * psi_norm_factor) / max(psi.psi.real))
        ln3.set_data(x_dense, psi.psi.real * wf_norm_factor)
    
    # update the information (if it need to be)
    if args.info != False:
        avrg_cordinate = psi.GetAvrgCordinate()
        avrg_momentum = psi.GetAvrgMomentum()
        sigma = sigma0 * math.sqrt(1 + ((i + 1)*dt/sigma0**2)**2)
        
        #update information in text box
        info_text.set_text(
            r'$\langle x \rangle =$ %0.2lf, $\langle p \rangle =$ %0.2lf, $\sigma = $ %0.2lf'
            %(avrg_cordinate, avrg_momentum, sigma)
        )


def main():
    start_time = datetime.now()
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    try:
        ani = AnimationStyle.CreateAnimation(fig, animate, total_frames_n, fps, args)
        # here we can save the animation like a video
        f_gif = r"../video/ramp_potential_" + date + r"_.gif" 
        AnimationStyle.SaveAnimation(ani, f_gif, args)

        exec_time = datetime.now() - start_time
        log_file = open(Path(__file__).parent / 'info.log', 'a')
        log_file.write('RampPotential.py exec time:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()
    except Exception:
        exec_time = datetime.now() - start_time
        log_file = open(Path(__file__).parent / 'info.log', 'a')
        log_file.write('RampPotential.py exec time:\n')
        log_file.write('Program was terminated or there was some error:\n')
        log_file.write(str(exec_time) + '\n\n')
        log_file.close()
        raise

if __name__ == '__main__':
    main()