import numpy as np
import pymc3 as pm
import collections


class Estimates:

    def __init__(self, trace, futures: collections.namedtuple, samplings: int, parameters: collections.namedtuple):
        """

        :param trace: The pymc3 model trace
        :param futures:  The number of predictions ahead
        :param samplings: The number of MC samples per observation/predictor point
        :param parameters: A named tuple of parameters including the number of dependent variables P
        """

        self.trace = trace
        self.futures = futures
        self.samplings = samplings
        self.parameters = parameters

    def average(self, arguments):
        """

        :param arguments:
        :return:
        """

        return self.trace[arguments.name].mean(axis=0)

    def cholesky(self, arguments):
        """

        :param arguments:
        :return:
        """

        vector = self.trace[arguments.cholesky].max(axis=0)
        matrix = pm.math.expand_packed_triangular(self.parameters.P, vector).eval()

        return matrix

    def tails(self, mu, chol):
        """

        :param mu:
        :param chol:
        :return:
        """

        return pm.MvNormal.dist(mu=mu, chol=chol).random(size=(self.samplings, self.futures.ahead))

    def exc(self, arguments):
        """

        :param arguments: A named tuple -> name, cholesky
        :return:
        """

        averages = self.average(arguments)
        cholesky = self.cholesky(arguments)
        tails = self.tails(mu=averages[-1, :], chol=cholesky)

        return np.concatenate((self.trace[arguments.name], tails), axis=1)
