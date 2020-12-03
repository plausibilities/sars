import numpy as np
import pandas as pd


class Segmentation:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    @staticmethod
    def filter(excerpt: pd.DataFrame):
        """
        Filters-out records wherein 'hospitalizedRate' is not greater that zero

        :param excerpt: The data excerpt in focus
        :return:
        """

        blob = excerpt[excerpt['hospitalizedRate'] > 0].copy()

        blob.sort_values(by='datetimeobject', ascending=True, inplace=True)

        blob.reset_index(drop=True, inplace=True)

        return blob

    def futures(self, features: np.ndarray, steps: np.ndarray, ahead: int):
        """

        :param features: An array of features values
        :param steps: The step-size of each feature
        :param ahead: The number of steps ahead for which observations will be predicted
        :return:
        """

        lowerlimit = np.amax(features, axis=0) + steps
        upperlimit = lowerlimit + (ahead * steps)

        supplement = np.linspace(start=lowerlimit, stop=upperlimit, num=ahead, axis=0, endpoint=False)

        extended = np.concatenate((features, supplement))

        return extended.astype(features.dtype)

    @staticmethod
    def tensors(excerpt: pd.DataFrame, independent: list, dependent: list):
        """
        Creates the matrix/vector forms of the independent & dependent variables

        :param excerpt: The data excerpt in focus
        :param independent: The independent variable/s list
        :param dependent: The dependent variable/s list
        :return:
        """

        features = excerpt[independent].values \
            if len(independent) > 0 else excerpt[independent].values[:, None]

        observations = excerpt[dependent].values \
            if len(dependent) > 0 else excerpt[dependent].values[:, None]

        assert features.shape[0] == observations.shape[0], 'The length of the independent & dependent ' \
                                                           'variables must be equal'

        return features, observations, excerpt[independent + dependent]

    def exc(self, stusps: str, independent: list, dependent: list):
        """

        :param stusps: The STUSPS code of the U.S.A state of interest
        :param independent: The independent variable/s list
        :param dependent: The dependent variable/s list
        :return:
        """

        excerpt = self.data[self.data['STUSPS'] == stusps]

        if 'hospitalizedRate' in independent + dependent:
            excerpt = self.filter(excerpt=excerpt.copy())

        return self.tensors(excerpt=excerpt.copy(), independent=independent, dependent=dependent)
