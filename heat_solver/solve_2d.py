#! /usr/bin/env python
import numpy as np
from scipy import ndimage


def solve_2d(temperature, spacing=(1., 1.), alpha=1., time_step=None,
             out=None):
    if time_step is None:
        time_step = min(spacing) ** 2 / (4. * alpha)
        time_step /= 2. # For safety

    if out is None:
        out = np.empty_like(temperature)

    inv_dy2, inv_dx2 = 1. / spacing[0] ** 2, 1. / spacing[1] ** 2

    stencil = alpha * time_step * (
        np.array([[     0.,                   inv_dy2,      0.],
                  [inv_dx2, -2. * (inv_dx2 + inv_dy2), inv_dx2],
                  [     0.,                   inv_dy2,      0.]]))

    ndimage.convolve(temperature, stencil, output=out)
    out[(0, -1), :] = 0.
    out[:, (0, -1)] = 0.

    return out
