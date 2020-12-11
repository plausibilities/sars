import collections

import arviz as az
import numpy as np
import pymc3 as pm
import theano


class Inference:

    def __init__(self, data, parameters, elements):

        self.data = data
        self.parameters = parameters
        self.elements = elements

        self.ModelFeatures = collections.namedtuple(
            typename='ModelFeatures',
            field_names=['model', 'trace', 'maximal', 'arviztrace', 'likelihood'])

    @staticmethod
    def share(tensor: np.ndarray, repeat: bool, repeats: int = None):

        if repeat:
            shared = theano.shared(np.repeat(tensor, repeats, axis=1))
        else:
            shared = theano.shared(tensor)

        return shared

    def exc(self):

        independent = self.share(tensor=self.data.independent, repeat=True, repeats=self.parameters.P)
        dependent = self.share(tensor=self.data.dependent, repeat=False)

        with pm.Model() as model:
            """
            The model
            """

            # Intercepts
            packed_l_c = pm.LKJCholeskyCov(name='packed_l_c', eta=5.0, n=self.parameters.P,
                                           sd_dist=pm.HalfStudentT.dist(nu=2.0, sigma=3.0))

            l_c = pm.expand_packed_triangular(n=self.parameters.P, packed=packed_l_c)

            c: pm.model.FreeRV = pm.MvGaussianRandomWalk(
                'intercept', shape=(self.elements.sections_, self.parameters.P), chol=l_c)

            cr = c[self.elements.indices]

            # Gradients
            packed_l_m = pm.LKJCholeskyCov(name='packed_l_m', eta=5.0, n=self.parameters.P,
                                           sd_dist=pm.HalfStudentT.dist(nu=2.0, sigma=3.0))
            l_m = pm.expand_packed_triangular(n=self.parameters.P, packed=packed_l_m)

            m: pm.model.FreeRV = pm.MvGaussianRandomWalk(
                'gradient', shape=(self.elements.sections_, self.parameters.P), chol=l_m)

            mr = m[self.elements.indices]

            # Regression
            # regression = cr + mr * self.independent
            regression = pm.Deterministic('regression', cr + mr * independent)

            # Hyper-parameters
            sigma: pm.model.TransformedRV = pm.Gamma(name='sigma', alpha=3.0, beta=2.5,
                                                     shape=(self.parameters.N, self.parameters.P))

            # Hence, likelihood ...
            # noinspection PyTypeChecker
            likelihood = pm.Normal(name='y', mu=regression, sigma=sigma, observed=dependent)

            # Inference
            # Drawing posterior samples using NUTS sampling
            # Beware, if the number of cores isn't set the function will use min(machine cores, 4)
            trace = pm.sample(draws=1000, cores=2, target_accept=0.8, tune=1000)
            maximal = pm.find_MAP()

            # The trace generated from Markov Chain Monte Carlo sampling
            arviztrace = az.from_pymc3(trace=trace)

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.ModelFeatures._make([model, trace, maximal, arviztrace, likelihood])
