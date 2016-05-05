#! /usr/bin/env python
import numpy as np
from scipy import ndimage


def solve_2d(temperature, spacing=(1., 1.), alpha=1., time_step=None,
             out=None):
    """Solve for the change in temperature.

    Parameters
    ----------
    temperature : ndarray of shape `(M, N)`
        Initial temperature values.
    spacing : tupe of float, optional
        Spacing between grid rows and columns.
    alpha : float, optional
        Thermal conductivity.
    temp_step : float, optional
        Time step to take for the new temperatures.
    out : ndarray of shape `(M, N)`, optional
        If provided, a buffer for output temperature changes.

    Returns
    -------
    delta_temperature : ndarray of shape `(M, N)`
        Temperature changes after the time step.
    """
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
