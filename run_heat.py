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

import numpy as np

from heat import HeatSolver

GRID_NY, GRID_NX = 11, 11
GRID_DY, GRID_DX = 1., 1.
ALPHA = 1.
N_STEPS = 5


if __name__ == '__main__':
    heat_solver = HeatSolver(shape=(GRID_NY, GRID_NX),
                             spacing=(GRID_DY, GRID_DX), alpha=ALPHA)

    for step in xrange(N_STEPS):
        if step % 1 == 0:
            print('Step = {step}'.format(step=step))
            np.savetxt(sys.stdout, heat_solver.temperature, fmt='%6.4F')

        heat_solver.advance_in_time()

    print('Step = {step}'.format(step=step))
    np.savetxt(sys.stdout, heat_solver.temperature, fmt='%6.4F')
