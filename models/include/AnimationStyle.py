from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as effects
from matplotlib import animation


BACKGROUND = '#090f1b'
PANEL = '#090f1b'
TEXT = '#e5edf7'
WAVE = '#55d6c2'
POTENTIAL = '#efb86b'
PHASE = '#b49aff'


def SetStyle():
    plt.rcParams.update({
        'figure.facecolor': BACKGROUND, 'axes.facecolor': PANEL,
        'savefig.facecolor': BACKGROUND, 'text.color': TEXT,
        'axes.labelcolor': TEXT, 'axes.edgecolor': '#43516a',
        'xtick.color': '#a6b5cb', 'ytick.color': '#a6b5cb',
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'axes.axisbelow': True,
        'grid.color': '#8191ac', 'grid.alpha': 0.13,
        'font.family': 'DejaVu Sans', 'font.size': 11,
        'axes.titlesize': 17, 'axes.titleweight': 'normal',
        'axes.titlepad': 20, 'axes.labelpad': 9,
        'lines.linewidth': 2.2, 'lines.solid_capstyle': 'round',
        'legend.facecolor': PANEL, 'legend.edgecolor': PANEL,
        'legend.fontsize': 9, 'legend.framealpha': 0.95,
    })


def AddArguments(parser):
    parser.set_defaults(info=True)
    parser.add_argument('--no-info', dest='info', action='store_false',
                        help='hide computed coordinate, momentum and sigma')
    parser.add_argument('--style', choices=('presentation', 'scientific'),
                        default='presentation', help='visual presentation or separate scientific axes')
    parser.add_argument('--pause', type=float, default=0.6,
                        help='seconds to hold the initial and final states')
    parser.add_argument('--fps', type=int, choices=(25, 50, 60), default=50,
                        help='output frames per second (GIF: 25 or 50; MP4: also 60)')
    parser.add_argument('--format', choices=('gif', 'mp4'), default='gif',
                        help='animation format (default: gif)')


def FrameSettings(settings, args):
    if args.format == 'gif' and args.fps == 60:
        raise ValueError('Use 25 or 50 FPS for GIF, or --format mp4 for 60 FPS.')
    # Keep the original physical duration and playback speed from the config.
    frames = max(1, round(settings['total_frames_n'] * args.fps / settings['fps']))
    dt = settings['total_frames_n'] / frames
    return args.fps, frames, dt


def StyleAxes(ax, x, potential=None, args=None, peak=0.1):
    presentation = args.style == 'presentation'
    original_lines = list(ax.lines)
    wave = next(line for line in original_lines
                if 'potential' not in line.get_label() and line.get_label() != 'wave function')
    phase = next((line for line in original_lines if line.get_label() == 'wave function'), None)
    has_potential = potential is not None and np.any(potential != 0)
    # Масштаб фиксируется по начальному состоянию, а не меняется от кадра к кадру.
    upper = peak * (2.5 if has_potential else 1.5)
    lower = -upper * (0.65 if has_potential and np.min(potential) < 0 else
                      0.5 if phase is not None else 0.08)
    ax.set_ylim(lower, upper)
    wave.set(color=WAVE, linewidth=2.0, label=r'$|\psi|^2$', zorder=5)
    if presentation:
        wave.set_path_effects([effects.Stroke(linewidth=10, foreground=WAVE, alpha=0.035),
                               effects.Stroke(linewidth=5, foreground=WAVE, alpha=0.09),
                               effects.Normal()])
    if phase is not None:
        phase.set(color=PHASE, linewidth=1.1, alpha=0.65,
                  label=r'Re $\psi$ (fixed scale)', zorder=4)
    # Старые линии потенциала больше не используют шкалу плотности вероятности.
    for line in original_lines:
        if 'potential' in line.get_label():
            line.set_visible(False)
    handles = [wave] + ([phase] if phase is not None else [])
    if has_potential:
        if presentation:
            # Только визуальная высота условна; координаты и ширина неизменны.
            magnitude = np.max(np.abs(potential))
            displayed = np.where(potential >= 0, potential/magnitude*upper*0.72,
                                 potential/magnitude*abs(lower)*0.78)
            potential_ax = ax
        else:
            potential_ax = ax.twinx()
            potential_ax.grid(False)
            potential_ax.spines['right'].set_visible(True)
            potential_ax.spines['right'].set_color(POTENTIAL)
            potential_ax.set_ylabel('V(x)', color=POTENTIAL)
            potential_ax.tick_params(axis='y', colors=POTENTIAL)
            # Совмещаем нулевые уровни обеих шкал, сохраняя реальные значения V.
            scale = max(max(potential)/upper, min(potential)/lower) * 1.25
            potential_ax.set_ylim(lower*scale, upper*scale)
            displayed = potential
        barrier, = potential_ax.plot(x, displayed, color=POTENTIAL, linewidth=1.2,
                                     alpha=0.8, label='V(x)', zorder=2)
        potential_ax.fill_between(x, 0, displayed, color=POTENTIAL, alpha=0.10, zorder=1)
        handles.append(barrier)
        values = f'V: {np.min(potential):.3g} … {np.max(potential):.3g}'
        note = 'potential height is schematic' if presentation else 'potential: right axis'
        ax.text(1, -0.10 if presentation else -0.23, values + '   /   ' + note, transform=ax.transAxes,
                ha='right', color=POTENTIAL, alpha=0.75, fontsize=8)
    ax.axhline(0, color='#9eafc7', alpha=0.16, linewidth=0.7, zorder=0)
    title = ax.get_title()
    ax.set_title('')
    ax.text(0, 1.17, title, transform=ax.transAxes, fontsize=18, va='bottom')
    if presentation:
        ax.set_axis_off()
    ax.legend(handles=handles, loc='upper right', frameon=False, fontsize=9)
    fill = ax.fill_between(x, np.zeros_like(x), color=WAVE, alpha=0.12, zorder=3)
    # Храним один полигон заливки и обновляем его вершины без накопления объектов.
    ax._wave_fill = (wave, fill)
    return ax.text(0, 1.04, '', transform=ax.transAxes, fontsize=10,
                   color='#b7c7db', va='bottom')


def LayoutFigure(fig, args):
    top = 0.90 if sum(hasattr(ax, '_wave_fill') for ax in fig.axes) > 1 else 0.80
    if args.style == 'presentation':
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.11, top=top, hspace=0.70)
    else:
        fig.subplots_adjust(left=0.09, right=0.90, bottom=0.13, top=top, hspace=0.85)


def CreateAnimation(fig, animate, frames, fps, args):
    if not np.isfinite(args.pause) or args.pause < 0:
        raise ValueError('--pause must be a finite non-negative number')
    hold = round(args.pause * fps)

    def update_fill():
        for ax in fig.axes:
            if hasattr(ax, '_wave_fill'):
                wave, fill = ax._wave_fill
                x, y = wave.get_data()
                if len(x):
                    vertices = np.column_stack((np.r_[x[0], x, x[-1]], np.r_[0, y, 0]))
                    fill.set_verts([vertices])

    def initialize():
        animate(-1, evolve=False)
        update_fill()
        return ()

    def update(i):
        # Паузы удерживают изображение, не продвигая физическое время.
        if i < 0:
            initialize()
        elif i < frames:
            animate(i)
            update_fill()
        return ()

    return animation.FuncAnimation(fig, update, frames=range(-hold, frames + hold),
                                   interval=1000/fps, init_func=initialize,
                                   repeat=False, cache_frame_data=False)


def SaveAnimation(ani, filename, args):
    filename = Path(__file__).resolve().parents[2] / 'video' / Path(filename).name
    filename = filename.with_suffix('.' + args.format)
    filename.parent.mkdir(parents=True, exist_ok=True)
    if args.format == 'gif':
        writer = animation.PillowWriter(fps=args.fps)
    else:
        writer = animation.FFMpegWriter(fps=args.fps, codec='libx264',
                                        extra_args=['-crf', '18', '-pix_fmt', 'yuv420p'])
    ani.save(str(filename), writer=writer, dpi=120)
