#! /usr/bin/env python
import warnings

import numpy as np

from solve_2d import solve_2d


class HeatSolver(object):

    def __init__(self, shape=(10, 10), spacing=(1., 1.), alpha=1.):
        """Solve the heat equation on a rectilinear grid.

        Parameters
        ----------
        shape : tuple of int, optional
            Number of rows and columns for the solution grid.
        spacing : tuple of float, optional
            Spacing between grid rows and columns.
        alpha : float, optional
            Thermal conductivity.
        """
        self._shape = tuple(shape)
        self._spacing = tuple(spacing)
        self._alpha = float(alpha)

        self._time_step = min(self.spacing) ** 2 / (4. * self.alpha)
        self._time_step /= 2.

        self._temperature = np.zeros(self.shape)
        self._delta_temperature = np.empty_like(self.temperature)

    @property
    def time_step(self):
        """The time step."""
        return self._time_step

    @time_step.setter
    def time_step(self, new_dt):
        if new_dt >= min(self.spacing) ** 2 / (4. * self.alpha):
            warnings.warn('using an unstable time step')
        self._time_step = new_dt

    @property
    def shape(self):
        """Number of grid rows and columns."""
        return self._shape

    @property
    def spacing(self):
        """Spacing between grid rows and columns."""
        return self._spacing

    @property
    def alpha(self):
        """Thermal conductivity."""
        return self._alpha

    @property
    def temperature(self):
        """Temperature values on the grid."""
        return self._temperature

    @temperature.setter
    def temperature(self, new_temp):
        self._temperature[:] = new_temp

    def solve(self):
        """Solve for the new temperatures."""
        solve_2d(self.temperature, spacing=self.spacing,
                 alpha=self.alpha, time_step=self.time_step,
                 out=self._delta_temperature)
        self._temperature += self._delta_temperature
