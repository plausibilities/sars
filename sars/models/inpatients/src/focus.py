"""
Module focus
"""
import collections

import numpy as np
import pandas as pd


class Focus:
    """
    Class Focus
    """

    def __init__(self, baseline: pd.DataFrame, variables: collections.namedtuple, futures: collections.namedtuple):
        """

        :param baseline:
        :param variables:
        :param futures:
        """

        # pylint: disable=C0103

        self.baseline = baseline
        self.variables = variables
        self.futures = futures

        # 'abscissae_' denotes the dates of 'abscissae', tensors of equal length; similarly for 'independent_'.
        self.Data = collections.namedtuple(typename='Data', field_names=['abscissae', 'independent', 'dependent',
                                                                         'abscissae_', 'independent_'])

        # N: The number of records, M: The number of independent variables, P: The number of dependent variables
        self.Parameters = collections.namedtuple(typename='Parameters', field_names=['N', 'M', 'P'])

    @staticmethod
    def filter(blob: pd.DataFrame):
        """
        Filters-out records wherein 'hospitalizedRate' & 'hospitalizedCumulative' are not greater than zero

        :param blob: A data set
        :return:
        """

        data = blob[(blob['hospitalizedRate'] > 0) & (blob['hospitalizedCumulative'] > 0)].copy()
        data.sort_values(by='date', ascending=True, inplace=True)
        data.reset_index(drop=True, inplace=True)

        return data

    def tensors(self, blob: pd.DataFrame):
        """
        Creates the matrix/vector forms of the independent & dependent variables

        :param blob: The data excerpt in focus
        :return:
        """

        independent = blob[self.variables.independent].values \
            if len(self.variables.independent) > 0 else blob[self.variables.independent].values[:, None]

        independent_ = blob[self.variables.independent_].values

        dependent = blob[self.variables.dependent].values \
            if len(self.variables.dependent) > 0 else blob[self.variables.dependent].values[:, None]

        assert independent.shape[0] == dependent.shape[0], 'The length of the independent & dependent ' \
                                                           'variables must be equal'

        return independent, dependent, independent_

    def abscissae(self, independent: np.ndarray):
        """

        :param independent: The data
        :return:
        """

        lowerlimit = np.amax(independent, axis=0) + self.futures.steps
        upperlimit = lowerlimit + (self.futures.ahead * self.futures.steps)
        supplement = np.linspace(start=lowerlimit, stop=upperlimit, num=self.futures.ahead, axis=0, endpoint=False)
        extended = np.concatenate((independent, supplement))

        return extended.astype(independent.dtype)

    def abscissae_(self, independent_: np.ndarray):
        """

        :param independent_: The data
        :return:
        """

        start = np.amax(independent_, axis=0) + np.timedelta64(self.futures.steps[0], 'D')
        supplement = np.arange(start,
                               start + np.timedelta64(self.futures.ahead, 'D'), dtype='datetime64[D]')

        return np.concatenate((independent_, supplement))

    def exc(self, stusps: str):
        """

        :param stusps: The STUSPS code of the U.S.A state of interest
        :return:
        """

        data = self.baseline[self.baseline['STUSPS'] == stusps]

        if any(i.startswith('hospitalized') for i in self.variables.independent + self.variables.dependent):
            data = self.filter(blob=data.copy())

        independent, dependent, independent_ = self.tensors(blob=data.copy())
        abscissae = self.abscissae(independent=independent)
        abscissae_ = self.abscissae_(independent_=independent_)

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.Data._make([abscissae, independent, dependent, abscissae_[:, None], independent_[:, None]]), \
               self.Parameters._make([independent.shape[0], independent.shape[1], dependent.shape[1]])
