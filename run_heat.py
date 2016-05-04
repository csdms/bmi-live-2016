from __future__ import print_function

import sys

from scipy import ndimage, random
import numpy as np


GRID_SHAPE = (10, 10)
GRID_SPACING = (1., 2.)
GRID_ORIGIN = (0., 0.)
ALPHA = 1.
N_STEPS = 10

TIME_STEP = min(GRID_SPACING) ** 2 / (4. * ALPHA)
DY2, DX2 = GRID_SPACING[0] ** 2, GRID_SPACING[1] ** 2
STENCIL = np.array([[0., DY2, 0.],
                    [DX2, -2. * (DY2 + DY2), DX2],
                    [0., DY2, 0.]]) * ALPHA * TIME_STEP / (DX2 * DY2)

time = 0.
temperature = random.random(GRID_SHAPE)
delta_temperature = np.empty_like(temperature)

print('Using dt = {dt}'.format(dt=TIME_STEP))

for step in xrange(N_STEPS):
    if step % 5 == 0:
        print('Step = {step}'.format(step=step))
        np.savetxt(sys.stdout, temperature, fmt='%6.3G')

    ndimage.convolve(temperature, STENCIL, output=delta_temperature)
    delta_temperature[(0, -1), :] = 0.
    delta_temperature[:, (0, -1)] = 0.

    temperature += delta_temperature

    time += TIME_STEP

print('Step = {step}'.format(step=step))
np.savetxt(sys.stdout, temperature, fmt='%6.3G')
