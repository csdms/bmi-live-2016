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

import yaml
import numpy as np

from heat_solver import BmiHeat


np.set_printoptions(linewidth=120,
                    formatter={'float_kind': lambda x : '%6.4F' % x})


if __name__ == '__main__':
    heat = BmiHeat()
    heat.initialize('heat.yaml')

    with open('heat.yaml', 'r') as file_obj:
        params = yaml.load(file_obj)

    print('shape: [{ny}, {nx}]'.format(ny=params['shape'][0],
                                       nx=params['shape'][1]))
    print('spacing: [{dy}, {dx}]'.format(dy=params['spacing'][0],
                                         dx=params['spacing'][1]))
    print('alpha: {alpha}'.format(alpha=params['alpha']))

    grid_id = heat.get_var_grid('plate_surface__temperature')
    grid_shape = heat.get_grid_shape(grid_id)

    temperature = np.zeros(grid_shape)
    temperature[grid_shape[0] / 2, grid_shape[1] / 2] = 1.

    heat.set_value('plate_surface__temperature', temperature)

    for time in np.linspace(0., 100., 6):
        heat.update_until(time)

        print('time: {time}'.format(time=time))
        print('temperature:\n{t}'.format(
            t=heat.get_value('plate_surface__temperature')))
