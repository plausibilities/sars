import collections
import logging

import numpy as np
import pandas as pd


class Focus:

    def __init__(self, baseline: pd.DataFrame, variables: collections.namedtuple, futures: collections.namedtuple):
        """

        :param baseline:
        :param variables:
        :param futures:
        """

        self.baseline = baseline
        self.variables = variables
        self.futures = futures

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.Data = collections.namedtuple(typename='Data',
                                           field_names=['abscissae', 'independent', 'dependent'])

        self.Parameters = collections.namedtuple(typename='Parameters',
                                                 field_names=['N', 'M', 'P'])

    @staticmethod
    def filter(blob: pd.DataFrame):
        """
        Filters-out records wherein 'hospitalizedRate' & 'hospitalizedCumulative' are not greater than zero

        :param blob: A data set
        :return:
        """

        data = blob[(blob['hospitalizedRate'] > 0) & (blob['hospitalizedCumulative'] > 0)].copy()
        data.sort_values(by='datetimeobject', ascending=True, inplace=True)
        data.reset_index(drop=True, inplace=True)

        return data

    def tensors(self, blob: pd.DataFrame):
        """
        Creates the matrix/vector forms of the independent & dependent variables

        :param blob: The data excerpt in focus
        :return:
        """

        self.logger.info('\n{}\n'.format(blob[self.variables.dependent].tail()))

        independent = blob[self.variables.independent].values \
            if len(self.variables.independent) > 0 else blob[self.variables.independent].values[:, None]

        dependent = blob[self.variables.dependent].values \
            if len(self.variables.dependent) > 0 else blob[self.variables.dependent].values[:, None]

        assert independent.shape[0] == dependent.shape[0], 'The length of the independent & dependent ' \
                                                           'variables must be equal'

        return independent, dependent

    def abscissae(self, independent):
        """

        :param independent: An array of features values
        :return:
        """

        lowerlimit = np.amax(independent, axis=0) + self.futures.steps
        upperlimit = lowerlimit + (self.futures.ahead * self.futures.steps)

        supplement = np.linspace(start=lowerlimit, stop=upperlimit, num=self.futures.ahead, axis=0, endpoint=False)

        extended = np.concatenate((independent, supplement))

        return extended.astype(independent.dtype)

    def exc(self, stusps: str):
        """

        :param stusps: The STUSPS code of the U.S.A state of interest
        :return:
        """

        data = self.baseline[self.baseline['STUSPS'] == stusps]

        if any(i.startswith('hospitalized') for i in self.variables.independent + self.variables.dependent):
            data = self.filter(blob=data.copy())

        independent, dependent = self.tensors(blob=data.copy())
        abscissae = self.abscissae(independent=independent)

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.Data._make([abscissae, independent, dependent]), self.Parameters._make(
            [independent.shape[0], independent.shape[1], dependent.shape[1]])
