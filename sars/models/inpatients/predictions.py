import numpy as np
import collections


class Predictions:

    def __init__(self, intercepts: np.ndarray, gradients: np.ndarray, samplings: int,
                 scaled: collections.namedtuple, parameters: collections.namedtuple):
        """

        :param intercepts:
        :param gradients:
        :param samplings:
        :param scaled:
        :param parameters: A named tuple of parameters including the number of dependent variables P
        """

        self.intercepts = intercepts
        self.gradients = gradients
        self.samplings = samplings
        self.scaled = scaled
        self.parameters = parameters

        self.Predictions = collections.namedtuple(typename='Predictions', field_names=['line', 'lines'])

    def line(self):
        """

        :return:
        """

        c = self.intercepts.mean(axis=0)
        m = self.gradients.mean(axis=0)

        # self.scaled.xscale.transform(self.futures)
        points = c + m * self.scaled.abscissae

        return self.scaled.yscale.inverse_transform(points)

    def lines(self, size: int):
        """

        :param size: The number of regression lines to select from the total number of lines
        :return:
        """

        indices = np.random.randint(0, high=self.samplings, size=size)

        c = self.intercepts[indices, :]
        m = self.gradients[indices, :]

        # self.scaled.xscale.transform(self.futures)
        points = c + (m * np.repeat(self.scaled.abscissae, repeats=self.parameters.P, axis=1))

        return self.scaled.yscale.inverse_transform(points)

    def exc(self, size: int):

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.Predictions._make([self.line(), self.lines(size=size)])
