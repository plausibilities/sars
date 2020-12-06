import arviz as az
import numpy as np
import pymc3 as pm
import theano


class Inference:

    def __init__(self, independent, dependent, measures, sections):

        self.independent = independent
        self.dependent = dependent
        self.measures = measures
        self.sections = sections

    @staticmethod
    def share(tensor: np.ndarray, repeat: bool, repeats: int = None):

        if repeat:
            shared = theano.shared(np.repeat(tensor, repeats, axis=1))
        else:
            shared = theano.shared(tensor)

        return shared

    def exc(self):

        with pm.Model() as model:
            """
            The model
            """

            # Intercepts
            packed_l_c = pm.LKJCholeskyCov(name='packed_l_c', eta=5.0, n=self.measures.P,
                                           sd_dist=pm.HalfStudentT.dist(nu=2.0, sigma=3.0))

            l_c = pm.expand_packed_triangular(n=self.measures.P, packed=packed_l_c)

            c: pm.model.FreeRV = pm.MvGaussianRandomWalk(
                'intercept', shape=(self.sections.sections_, self.measures.P), chol=l_c)

            cr = c[self.sections.indices]

            # Gradients
            packed_l_m = pm.LKJCholeskyCov(name='packed_l_m', eta=5.0, n=self.measures.P,
                                           sd_dist=pm.HalfStudentT.dist(nu=2.0, sigma=3.0))
            l_m = pm.expand_packed_triangular(n=self.measures.P, packed=packed_l_m)

            m: pm.model.FreeRV = pm.MvGaussianRandomWalk(
                'gradient', shape=(self.sections.sections_, self.measures.P), chol=l_m)

            mr = m[self.sections.indices]

            # Regression
            # regression = cr + mr * self.independent
            regression = pm.Deterministic('regression', cr + mr * self.independent )

            # Hyper-parameters
            sigma: pm.model.TransformedRV = pm.Uniform(name='sigma', lower=0, upper=18.5,
                                                       shape=(self.measures.N, self.measures.P))

            # Hence, likelihood ...
            # noinspection PyTypeChecker
            likelihood = pm.Normal(name='y', mu=regression, sigma=sigma, observed=self.dependent)

            # Inference
            # Drawing posterior samples using NUTS sampling
            # Beware, if the number of cores isn't set the function will use min(machine cores, 4)
            trace = pm.sample(draws=2000, cores=2, target_accept=0.9, tune=2000)
            maximal = pm.find_MAP()

            # The trace generated from Markov Chain Monte Carlo sampling
            arviztrace = az.from_pymc3(trace=trace)

        return model, likelihood, trace, maximal, arviztrace
