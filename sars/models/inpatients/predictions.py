"""
Module predictions
"""
import collections

import numpy as np


class Predictions:
    """
    Class Predictions
    """

    def __init__(self, iag: collections.namedtuple, samplings: int,
                 scaled: collections.namedtuple, parameters: collections.namedtuple):
        """

        :param iag: A named tuple of intercepts & gradients => iag.intercepts & iag.gradients
        :param samplings:
        :param scaled:
        :param parameters: A named tuple of parameters including the number of dependent variables P
        """

        self.iag = iag
        self.samplings = samplings
        self.scaled = scaled
        self.parameters = parameters

        self.Predictions = collections.namedtuple(
            typename='Predictions',
            field_names=['line', 'lines'])  # pylint: disable=C0103

    def line(self):
        """

        :return:
        """

        pc_ = self.iag.intercepts.mean(axis=0)
        pm_ = self.iag.gradients.mean(axis=0)

        # self.scaled.xscale.transform(self.futures)
        points = pc_ + pm_ * self.scaled.abscissae

        return self.scaled.yscale.inverse_transform(points)

    def lines(self, size: int):
        """

        :param size: The number of estimated regression lines to randomly select
        :return:
        """

        indices = np.random.randint(0, high=self.samplings, size=size)

        pc_ = self.iag.intercepts[indices, :]
        pm_ = self.iag.gradients[indices, :]

        # self.scaled.xscale.transform(self.futures)
        points = pc_ + (pm_ * np.repeat(self.scaled.abscissae, repeats=self.parameters.P, axis=1))

        return self.scaled.yscale.inverse_transform(points)

    def exc(self, size: int):
        """

        :param size: The number of estimated regression lines to randomly select
        :return:
        """

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.Predictions._make([self.line(), self.lines(size=size)])
