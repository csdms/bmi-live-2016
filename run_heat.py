from __future__ import print_function

import sys

from scipy import ndimage, random
import numpy as np


GRID_SHAPE = (10, 10)
GRID_SPACING = (1., 2.)
GRID_ORIGIN = (0., 0.)
ALPHA = 1.
N_STEPS = 10

time = 0.
time_step = min(GRID_SPACING) ** 2 / (4. * ALPHA)
temperature = random.random(GRID_SHAPE)
next_temperature = np.empty_like(temperature)

print('Using dt = {dt}'.format(dt=time_step))

for step in xrange(N_STEPS):
    if step % 5 == 0:
        print('Step = {step}'.format(step=step))
        np.savetxt(sys.stdout, temperature, fmt='%6.3G')

    dy2, dx2 = GRID_SPACING[0] ** 2, GRID_SPACING[1] ** 2
    stencil = np.array([[0., dy2, 0.],
                        [dx2, -2. * (dx2 + dy2), dx2],
                        [0., dy2, 0.]]) * ALPHA * time_step / (dx2 * dy2)

    ndimage.convolve(temperature, stencil, output=next_temperature)
    next_temperature[(0, -1), :] = 0.
    next_temperature[:, (0, -1)] = 0.
    next_temperature += temperature

    np.copyto(temperature, next_temperature)

    time += time_step

print('Step = {step}'.format(step=step))
np.savetxt(sys.stdout, temperature, fmt='%6.3G')
