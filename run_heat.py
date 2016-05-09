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

from scipy import ndimage, random
import numpy as np


np.set_printoptions(linewidth=120,
                    formatter={'float_kind': lambda x : '%6.4F' % x})


GRID_SHAPE = (11, 11)
GRID_SPACING = (1., 1.)
ALPHA = .1
STOP_TIME = 100.

time_step = min(GRID_SPACING) ** 2 / (4. * ALPHA) * 0.5

inv_dY2, inv_dX2 = 1. / GRID_SPACING[0] ** 2, 1. / GRID_SPACING[1] ** 2
stencil = ALPHA * time_step * (
    np.array([[     0.,                   inv_dY2,      0.],
              [inv_dX2, -2. * (inv_dX2 + inv_dY2), inv_dX2],
              [     0.,                   inv_dY2,      0.]]))

temperature = random.random(GRID_SHAPE)
delta_temperature = np.empty_like(temperature)

temperature = np.zeros(GRID_SHAPE)
temperature[GRID_SHAPE[0] / 2, GRID_SHAPE[1] / 2] = 1.

n_steps = int(STOP_TIME / time_step)
for step in range(n_steps + 1):
    if step % (n_steps // 5) == 0:
        print('Time = {time}'.format(time=step * time_step))
        print(temperature)

    ndimage.convolve(temperature, stencil, output=delta_temperature)
    delta_temperature[(0, -1), :] = 0.
    delta_temperature[:, (0, -1)] = 0.

    temperature += delta_temperature
