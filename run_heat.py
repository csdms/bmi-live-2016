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

from heat_solver import BmiHeat


if __name__ == '__main__':
    heat = BmiHeat()
    heat.initialize('heat.yaml')

    grid_id = heat.get_var_grid('plate_surface__temperature')
    grid_shape = heat.get_grid_shape(grid_id)

    temperature = np.zeros(grid_shape)
    temperature[grid_shape[0] / 2, grid_shape[1] / 2] = 1.

    heat.set_value('plate_surface__temperature', temperature)

    for time in np.linspace(0., 100., 5):
        print('Time = {time}'.format(time=time))
        np.savetxt(sys.stdout, heat.get_value('plate_surface__temperature'),
                   fmt='%6.4F')

        heat.update_until(time)
