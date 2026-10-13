"""Render the five selected scattering experiments, including outgoing packets.

Uses the same complete eigendecomposition of the finite-difference Hamiltonian
as WaveFunction. Frames are evaluated at absolute times, so export cannot skip
or repeat evolution steps. FFmpeg encodes on disk instead of retaining RGB frames.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from types import SimpleNamespace

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy as np
from scipy.linalg import eigh_tridiagonal

from include import AnimationStyle as style, PotentialBarriers as potentials
from include.ShrodingerEquation import GaussWavePackage, WaveFunction

ROOT = Path(__file__).resolve().parents[1]
# name, Russian title, physical end time, playback seconds, view, contact interval
SCENES = [
    ('QuantumTunnelling', 'Квантовое туннелирование', 330, 16, (-230, 300), (150, 260)),
    ('BoxPit', 'Прохождение потенциальной ямы', 250, 14, (-210, 340), (105, 205)),
    ('TwoLevelBoxPotential', 'Двухуровневый барьер', 200, 14, (-180, 320), (35, 140)),
    ('StepPotential', 'Потенциальная ступенька', 240, 16, (-330, 180), (20, 130)),
    ('TwoWall', 'Прохождение через два барьера', 400, 24, (-460, 530), (70, 210)),
]


def setup(name):
    config = json.loads((ROOT / 'models' / 'configs' / f'{name}.json').read_text())
    wave, b = config[1:]
    # Larger domain prevents spurious hard-wall reflections during long runs.
    # Keep the original mesh spacing and anchor, preserving sampled potentials.
    dx = (config[0]['x_end'] - config[0]['x_start']) / (config[0]['N'] - 1)
    x = config[0]['x_start'] + np.arange(-1110, 2500) * dx
    if name in ('QuantumTunnelling', 'BoxPit'):
        v = np.array([potentials.BoxBarier(z, b['V_x0'], b['a'], b['V0']) for z in x])
        left, right = b['V_x0']-b['a']/2, b['V_x0']+b['a']/2
    elif name == 'TwoLevelBoxPotential':
        v = np.array([potentials.TwoLevelBoxPotential(z, b['V_x0'], b['a'], b['V0'], b['V1'], b['V2']) for z in x])
        left, right = b['V_x0']-b['a']/2, b['V_x0']+b['a']/2
    elif name == 'StepPotential':
        v = np.where(x <= b['V_x0'], b['V1'], b['V2'])
        left = right = b['V_x0']
    else:
        v = np.array([potentials.TwoWall(z, b['x1'], b['x2'], b['d1'], b['d2'], b['V1'], b['V2']) for z in x])
        left, right = b['x1']-b['d1']/2, b['x2']+b['d2']/2
    packet = GaussWavePackage(x, wave['x0'], wave['sigma0'], np.sqrt(2*wave['E0']))
    return x, dx, v, packet, left, right


def simulate(name, times):
    x, dx, v, packet, left, right = setup(name)
    energies, q = eigh_tridiagonal(1/dx**2+v, np.full(len(x)-1, -1/(2*dx**2)))
    initial = packet.GetWavePackage()
    coeff = q.T @ initial.real + 1j*(q.T @ initial.imag)
    density = np.empty((len(times), len(x)))
    for start in range(0, len(times), 64):
        c = coeff[:, None] * np.exp(-1j*energies[:, None]*times[None, start:start+64])
        real, imag = q @ c.real, q @ c.imag
        density[start:start+64] = (real**2+imag**2).T
    # Independent check against the existing public solver at the final time.
    reference = WaveFunction(packet, x, v)
    reference.PsiTimeEvolute(float(times[-1]))
    error = float(np.max(abs(density[-1] - reference.WaveFunctioProbability())))
    assert error < 1e-10, error
    assert np.max(abs(density.sum(axis=1)*dx-1)) < 1e-9
    return x, dx, v, density, left, right, error


def metrics(x, dx, density, left, right, view):
    masks = {'left': x < left, 'interaction': (x >= left) & (x <= right),
             'right': x > right, 'near_potential': (x >= left-20) & (x <= right+20),
             'boundary': (x < x[0]+50) | (x > x[-1]-50),
             'outside_view': (x < view[0]) | (x > view[1])}
    return {key: (density[:, mask].sum(axis=1)*dx).tolist() for key, mask in masks.items()}


def render(scene, output, fps, probe=False):
    name, title, end, seconds, view, contact = scene
    times = np.linspace(0, end, 81 if probe else seconds*fps+1)
    x, dx, v, density, left, right, error = simulate(name, times)
    stats = metrics(x, dx, density, left, right, view)
    report = {'name': name, 'physical_end': end, 'playback_seconds': seconds+2.0,
              'times': times.tolist(), 'solver_max_error': error,
              'norm_max_error': float(np.max(abs(density.sum(axis=1)*dx-1))),
              'max_boundary_mass': max(stats['boundary']),
              'max_outside_view_mass': max(stats['outside_view']),
              'final': {k: val[-1] for k, val in stats.items()}, 'probabilities': stats}
    (output/f'{name}.json').write_text(json.dumps(report, indent=2))
    print(name, json.dumps({k:report[k] for k in ('physical_end','max_boundary_mass','max_outside_view_mass','final')}), flush=True)
    assert report['max_boundary_mass'] < 1e-5
    assert report['max_outside_view_mass'] < 0.002
    if probe:
        return
    style.SetStyle()
    fig, ax = plt.subplots(figsize=(32/3, 6))
    ax.set_xlim(*view)
    ax.set_title(title)
    line, = ax.plot([], [], label='wave package')
    args = SimpleNamespace(style='presentation')
    info = style.StyleAxes(ax, x, v, args, peak=max(density[0].max(), density.max()/2.3))
    style.LayoutFigure(fig, args)
    # Make the schematic potential disclaimer understandable in Russian.
    for txt in ax.texts:
        if 'potential height is schematic' in txt.get_text():
            txt.set_text(txt.get_text().replace('potential height is schematic', 'высота потенциала условная'))
    phase = ax.text(0, -.065, '', transform=ax.transAxes, color=style.TEXT, fontsize=10)
    amounts = ax.text(0, -.13, '', transform=ax.transAxes, color='#b7c7db', fontsize=9)
    # Tunnelling is only ~2% for the original barrier: show it on a labelled inset.
    inset = None
    if name == 'QuantumTunnelling':
        inset = ax.inset_axes([.67, .52, .31, .30])
        inset.set_xlim(right, view[1]); inset.set_ylim(0, (ax.get_ylim()[1]-ax.get_ylim()[0])*.30/15)
        inset.set_axis_off()
        inset.set_title('Прошедшая часть ×15', fontsize=10, pad=8)
        small, = inset.plot([], [], color=style.WAVE, linewidth=1.4)
    fill = ax._wave_fill[1]
    def update(i):
        p = density[i]
        line.set_data(x, p)
        fill.set_verts([np.column_stack((np.r_[x[0], x, x[-1]], np.r_[0, p, 0]))])
        mean = np.sum(x*p)*dx
        sigma = np.sqrt(np.sum((x-mean)**2*p)*dx)
        info.set_text(f't = {times[i]:.1f}     ⟨x⟩ = {mean:.1f}     σ = {sigma:.1f}')
        label = 'Приближение пакета' if times[i] < contact[0] else 'Взаимодействие с потенциалом' if times[i] < contact[1] else 'Отражённая и прошедшая части расходятся'
        if name == 'TwoWall' and times[i] >= contact[1]:
            label = 'Прошедшая часть и повторные отражения между барьерами'
        phase.set_text(label)
        amounts.set_text(f"Вероятность: слева {stats['left'][i]:.1%}   |   в области потенциала {stats['interaction'][i]:.1%}   |   справа {stats['right'][i]:.1%}")
        if name == 'StepPotential':
            amounts.set_text(f"Вероятность: слева от ступеньки {stats['left'][i]:.1%}   |   справа {stats['right'][i]:.1%}")
        if inset is not None:
            small.set_data(x, p)
    # Contact sheets make beginning, collision and outgoing states reviewable.
    for label, t in [('start',0), ('collision',sum(contact)/2), ('final',end)]:
        update(int(np.argmin(abs(times-t))))
        fig.savefig(output/f'{name}_{label}.png', dpi=120)
    with tempfile.TemporaryDirectory(prefix='scattering-') as temp:
        movie = Path(temp)/'frames.mkv'
        palette = Path(temp)/'palette.png'
        writer = FFMpegWriter(fps=fps, codec='ffv1', extra_args=['-level','3'])
        with writer.saving(fig, str(movie), dpi=120):
            update(0)
            for _ in range(fps): writer.grab_frame()
            for i in range(len(times)):
                update(i); writer.grab_frame()
                if i % (fps*4) == 0: print(f'{name}: {i}/{len(times)} кадров', flush=True)
            for _ in range(fps-1): writer.grab_frame()
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(movie),'-vf','palettegen=stats_mode=diff','-frames:v','1',str(palette)],check=True)
        target = output/f'{name}.gif'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(movie),'-i',str(palette),'-lavfi','paletteuse=dither=bayer:bayer_scale=3','-loop','0',str(target)],check=True)
    plt.close(fig)
    # Decode the entire deliverable, not just its header or first frame.
    from PIL import Image
    with Image.open(target) as gif:
        duration = 0
        for i in range(gif.n_frames):
            gif.seek(i); gif.load(); duration += gif.info['duration']
        assert abs(duration/1000-(seconds+2)) < .05
        assert gif.size == (1280,720)
        report['gif'] = {'frames':gif.n_frames, 'seconds':duration/1000, 'size':list(gif.size)}
    (output/f'{name}.json').write_text(json.dumps(report, indent=2))
    print(f'Готово: {target} ({duration/1000:.2f} с)',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe', action='store_true')
    parser.add_argument('--fps',type=int, choices=(25,50),default=50)
    parser.add_argument('--only', choices=[s[0] for s in SCENES])
    parser.add_argument('--output',type=Path,default=ROOT/'video'/'selected')
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    for scene in SCENES:
        if not args.only or scene[0]==args.only:
            render(scene,args.output,args.fps,args.probe)

if __name__=='__main__':
    main()
