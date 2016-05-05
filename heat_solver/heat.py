#! /usr/bin/env python
import numpy as np

from solve_2d import solve_2d


class HeatSolver(object):

    def __init__(self, shape=(10, 20), spacing=(1., 1.), alpha=1.):
        self._shape = tuple(shape)
        self._spacing = tuple(spacing)
        self._alpha = float(alpha)

        self._time_step = min(self.spacing) ** 2 / (4. * self.alpha)
        self._time_step /= 2.

        self._temperature = np.zeros(self.shape)
        self._delta_temperature = np.empty_like(self.temperature)

    @property
    def time_step(self):
        return self._time_step

    @property
    def shape(self):
        return self._shape

    @property
    def spacing(self):
        return self._spacing

    @property
    def alpha(self):
        return self._alpha

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_temp):
        self._temperature[:] = new_temp

    def solve(self):
        solve_2d(self.temperature, spacing=self.spacing,
                 alpha=self.alpha, time_step=self.time_step,
                 out=self._delta_temperature)
        self._temperature += self._delta_temperature
