"""
Module inference
"""
import collections

import arviz as az
import numpy as np
import pymc3 as pm
import theano


class Inference:
    """
    Class Inference
    """

    def __init__(self, data, parameters, elements):
        """

        :param data:
        :param parameters:
        :param elements:
        """

        # pylint: disable=C0103

        self.data = data
        self.parameters = parameters
        self.elements = elements

        # Setting disable=C0103, as above, ensures that this correct variable naming convention
        # does not raise convention errors
        self.ModelFeatures = collections.namedtuple(
            typename='ModelFeatures',
            field_names=['model', 'trace', 'maximal', 'arviztrace', 'likelihood'])

    @staticmethod
    def share(tensor: np.ndarray, repeat: bool, repeats: int = None):
        """

        :param tensor:
        :param repeat: Should the tensor be expanded along axis 1?
        :param repeats: If the tensor should be expanded, ...
        :return: A THEANO shared tensor
        """

        if repeat:
            shared = theano.shared(np.repeat(tensor, repeats, axis=1))
        else:
            shared = theano.shared(tensor)

        return shared

    def exc(self):
        """

        :return: A named tuple of model characteristics
        """

        # pylint: disable=E1136

        # self.share(tensor=self.data.independent, repeat=True, repeats=self.parameters.P)
        independent = self.data.independent

        # self.share(tensor=self.data.dependent, repeat=False)
        dependent = self.data.dependent

        with pm.Model() as model:
            # Intercepts
            packed_l_c = pm.LKJCholeskyCov(name='packed_l_c', eta=5.0, n=self.parameters.P,
                                           sd_dist=pm.HalfStudentT.dist(nu=2.0, sigma=3.0))
            l_c = pm.expand_packed_triangular(n=self.parameters.P, packed=packed_l_c)

            # pm.model.FreeRV
            ec_ = pm.MvGaussianRandomWalk(
                'intercept', shape=(self.elements.sections_, self.parameters.P), chol=l_c)
            ecr = ec_[self.elements.indices]

            # Gradients
            packed_l_m = pm.LKJCholeskyCov(name='packed_l_m', eta=5.0, n=self.parameters.P,
                                           sd_dist=pm.HalfStudentT.dist(nu=2.0, sigma=3.0))
            l_m = pm.expand_packed_triangular(n=self.parameters.P, packed=packed_l_m)

            # pm.model.FreeRV
            em_ = pm.MvGaussianRandomWalk(
                'gradient', shape=(self.elements.sections_, self.parameters.P), chol=l_m)
            emr = em_[self.elements.indices]

            # Regression
            regression = pm.Deterministic('regression', ecr + emr * independent)

            # Hyper-parameters
            # pm.model.TransformedRV
            sigma = pm.Uniform(name='sigma', lower=0, upper=18.5,
                               shape=(self.parameters.N, self.parameters.P))

            # Hence, likelihood ...
            # noinspection PyTypeChecker
            likelihood = pm.Normal(name='y', mu=regression, sigma=sigma, observed=dependent)

            # Inference
            # Drawing posterior samples using NUTS sampling
            # Beware, if the number of cores isn't set the function will use min(machine cores, 4)
            trace = pm.sample(draws=500, cores=2, target_accept=0.9, tune=1000)
            # maximal = pm.find_MAP()
            maximal = None

            # The trace generated from Markov Chain Monte Carlo sampling
            arviztrace = az.from_pymc3(trace=trace)

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.ModelFeatures._make([model, trace, maximal, arviztrace, likelihood])
