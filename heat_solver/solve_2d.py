#! /usr/bin/env python
import numpy as np
from scipy import ndimage


def solve_2d(temperature, spacing=(1., 1.), alpha=1., time_step=None,
             out=None):
    """Solve the 2D heat equation for temperature change.

    Parameters
    ----------
    temperature : ndarray of float, shape `(M, N)`
        Starting temperature.
    spacing : tuple of int, optional
        Grid spacing as `(dy, dx)`.
    alpha : float, optional
        Thermal diffusivity.
    time_step : float, optional
        Time step to use. If not provided, the time step will be calculated
        as one half of the stability condition.
    out : ndarray of float, shape `(M, N)`
        Buffer into which to place the temperature changes. If not provided,
        a new-created array will be used.

    Returns
    -------
    out : ndarray of float, shape `(M, N)`
        The temperature changes.
    """
    if time_step is None:
        time_step = min(spacing) ** 2 / (4. * alpha)
        time_step *= .5 # For safety

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
