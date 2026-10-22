"""Figures for the markdown pages: python tools/make_figures.py -> figures/*.png"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / 'figures'
OUT.mkdir(exist_ok=True)
INK, MUTED, ACC, ACC2, BG = '#1d2421', '#5d6762', '#1f6f5c', '#b5651d', '#f3f6f4'


def box(ax, x, y, w, h, title, lines, color):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.02,rounding_size=0.06',
                                fc='white', ec=color, lw=1.6))
    ax.text(x, y + h / 2 - 0.13, title, ha='center', va='top', fontsize=10.5, weight='bold', color=color)
    ax.text(x, y + h / 2 - 0.42, '\n'.join(lines), ha='center', va='top', fontsize=8.6, color=INK, linespacing=1.45)


def arrow(ax, p, q, text='', color=MUTED, rad=0.0, off=(0, 0)):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=13, lw=1.3, color=color,
                                 connectionstyle=f'arc3,rad={rad}', shrinkA=2, shrinkB=2))
    if text:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], text, ha='center', va='center',
                fontsize=8.2, color=color, style='italic')


# 1. one time step of coupling.py
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis('off')
box(ax, 1.25, 3.3, 2.1, 1.1, 'case.yaml', ['chemistry:  transport:', 'coupling:  output:'], INK)
box(ax, 1.25, 1.0, 2.1, 1.5, 'output.py', ['profiles.csv', 'mass_balance.csv', 'summary.txt'], MUTED)
box(ax, 4.8, 2.15, 2.7, 3.9, 'coupling.py', ['time loop, every step:', '', '1  immobile = total − aqueous', '2  transport the aqueous part',
                                          '3  total = immobile + aqueous', '4  equilibrate total, cell by cell', '5  update φ and De',
                                          '6  check the mass balance', '7  write output'], INK)
box(ax, 8.8, 3.3, 2.2, 1.5, 'transport.py', ['FEniCSx, 1D DG0', 'diffusion + advection', 'backward Euler'], ACC)
box(ax, 8.8, 1.0, 2.2, 1.5, 'chemistry.py', ['GEMS3K via xgems', 'local equilibrium', 'per cell'], ACC2)
arrow(ax, (2.3, 3.3), (3.45, 3.3), 'read', INK, off=(0, 0.16))
arrow(ax, (3.45, 1.0), (2.3, 1.0), 'state', MUTED, off=(0, 0.16))
arrow(ax, (6.15, 3.55), (7.7, 3.55), 'aqueous, φ, De', ACC, off=(0, 0.17))
arrow(ax, (7.7, 3.05), (6.15, 3.05), 'aqueous', ACC, off=(0, -0.17))
arrow(ax, (6.15, 1.25), (7.7, 1.25), 'total', ACC2, off=(0, 0.17))
arrow(ax, (7.7, 0.75), (6.15, 0.75), 'aqueous, minerals, solids', ACC2, off=(0, -0.2))
plt.savefig(OUT / 'coupling_loop.png', dpi=170, bbox_inches='tight', facecolor='white')
plt.close()

# 2. what is stored per cell
fig, ax = plt.subplots(figsize=(8.4, 2.5))
ax.set_xlim(0, 8.4); ax.set_ylim(0, 2.5); ax.axis('off')
x0, w = 0.3, 7.8
parts = [('pore water  φ', 0.45, '#d6ebe4', 'aqueous  (mol/m³ bulk)\nmoves with transport'),
         ('minerals listed in solid_phases', 0.35, '#f3e1cd', 'immobile = total − aqueous\nGEMS can dissolve / precipitate'),
         ('inert', 0.20, '#e6e8e7', '1 − φ0 − initial solids\nnever changes')]
x = x0
for name, f, c, note in parts:
    ax.add_patch(plt.Rectangle((x, 1.2), w * f, 0.8, fc=c, ec=INK, lw=1))
    ax.text(x + w * f / 2, 1.6, name, ha='center', va='center', fontsize=9.5, color=INK)
    ax.text(x + w * f / 2, 0.85, note, ha='center', va='top', fontsize=8.2, color=MUTED, linespacing=1.4)
    x += w * f
ax.text(x0, 2.2, 'one cell, 1 m³ of bulk material', fontsize=9.5, color=INK, weight='bold')
plt.savefig(OUT / 'cell_volume.png', dpi=170, bbox_inches='tight', facecolor='white')
plt.close()
print('figures written to', OUT)
