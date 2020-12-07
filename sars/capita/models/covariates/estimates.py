import numpy as np
import pymc3 as pm


class Estimates:

    def __init__(self, trace, ahead: int, samplings: int, measures):
        """

        :param trace: The pymc3 model trace
        :param ahead:  The number of predictions ahead
        :param samplings: The number of MC samples per observation/predictor point
        :param measures: A tuple of measures including the number of dependent variables P
        """

        self.trace = trace
        self.ahead = ahead
        self.samplings = samplings
        self.measures = measures

    def average(self, parameter):
        """

        :param parameter:
        :return:
        """

        return self.trace[parameter.name].mean(axis=0)

    def cholesky(self, parameter):
        """

        :param parameter:
        :return:
        """

        vector = self.trace[parameter.cholesky].max(axis=0)
        matrix = pm.math.expand_packed_triangular(self.measures.P, vector).eval()

        return matrix

    def tails(self, mu, chol):
        """

        :param mu:
        :param chol:
        :return:
        """

        return pm.MvNormal.dist(mu=mu, chol=chol).random(size=(self.samplings, self.ahead))

    def exc(self, parameter):
        """

        :param parameter: A named tuple -> name, cholesky
        :return:
        """

        averages = self.average(parameter)
        cholesky = self.cholesky(parameter)
        tails = self.tails(mu=averages[-1, :], chol=cholesky)

        return np.concatenate((self.trace[parameter.name], tails), axis=1)
