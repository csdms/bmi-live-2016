"""Solve the heat equation of a uniform rectilinear grid.

Solve the heat equation of a rectilinear grid with shape (*GRID_NY*,
*GRID_NX*) and row and column spacing (*GRID_DY*, *GRID_DX*). The thermal
conductivity is given by *ALPHA*.

In cartesian coordinates, the heat equation is the following parabolic
differential equation,

    del u / del t - alpha (del^2 u / del x^2 + del^2 u / del y^2) = 0

This becomes the following finite-difference problem,

    Delta u = alpha Delta t ((u_i-1,j + u_i+1,j) / Delta x^2 +
                             (u_i,j-1 + u_i,j+1) / Delta y^2 -
                             2 u_i,j / (Delta x^2 + Delta y^2))
"""

from __future__ import print_function

import sys

from scipy import ndimage, random
import numpy as np

GRID_NY, GRID_NX = 11, 11
GRID_DY, GRID_DX = 1., 1.
ALPHA = 1.
N_STEPS = 5

TIME_STEP = min((GRID_DX, GRID_DY)) ** 2 / (4. * ALPHA)
TIME_STEP /= 2. # For safety
INV_DY2, INV_DX2 = 1. / GRID_DY ** 2, 1. / GRID_DY ** 2
STENCIL = ALPHA * TIME_STEP * (
    np.array([[     0.,                   INV_DY2,      0.],
              [INV_DX2, -2. * (INV_DX2 + INV_DY2), INV_DX2],
              [     0.,                   INV_DY2,      0.]]))

time = 0.
temperature = np.zeros((GRID_NY, GRID_NX))
temperature[5, 5] = 1.
delta_temperature = np.empty_like(temperature)

print('Using dt = {dt}'.format(dt=TIME_STEP))

for step in xrange(N_STEPS):
    if step % 1 == 0:
        print('Step = {step}'.format(step=step))
        np.savetxt(sys.stdout, temperature, fmt='%6.4F')

    ndimage.convolve(temperature, STENCIL, output=delta_temperature)
    delta_temperature[(0, -1), :] = 0.
    delta_temperature[:, (0, -1)] = 0.

    temperature += delta_temperature

    time += TIME_STEP

print('Step = {step}'.format(step=step))
np.savetxt(sys.stdout, temperature, fmt='%6.4F')
