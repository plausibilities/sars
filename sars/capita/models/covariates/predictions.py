import numpy as np


class Predictions:

    def __init__(self, intercepts_, gradients_, futures, samplings,
                 xscaler, yscaler, measures):
        """

        :param intercepts_:
        :param gradients_:
        :param futures:
        :param samplings:
        :param xscaler:
        :param yscaler:
        :param measures: A tuple of measures including the number of dependent variables P
        """

        self.intercepts_ = intercepts_
        self.gradients_ = gradients_

        self.futures = futures
        self.samplings = samplings

        self.xscaler = xscaler
        self.yscaler = yscaler

        self.measures = measures

    def line(self):
        """

        :return:
        """

        c = self.intercepts_.mean(axis=0)
        m = self.gradients_.mean(axis=0)

        points = c + m * self.xscaler.transform(self.futures)

        return self.yscaler.inverse_transform(points)

    def lines(self, size: int):
        """

        :param size: The number of regression lines to select from the total number of lines
        :return:
        """

        indices = np.random.randint(0, high=self.samplings, size=size)

        c = self.intercepts_[indices, :]
        m = self.gradients_[indices, :]

        points = c + (m * np.repeat(self.xscaler.transform(self.futures), repeats=self.measures.P, axis=1))

        return self.yscaler.inverse_transform(points)
