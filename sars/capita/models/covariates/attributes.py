import collections

import numpy as np
import theano


class Attributes:

    def __init__(self, independent: np.ndarray, dependent: np.ndarray,
                 sections_: int, instances_: np.ndarray):
        """

        :param independent:
        :param dependent:
        """

        assert independent.shape[0] == dependent.shape[0], 'The number of independent & dependent ' \
                                                           'instances must be equal'

        self.independent = independent
        self.dependent = dependent

        self.sections_ = sections_
        self.instances_ = instances_

    def measures(self):
        """

        N: The number of records
        M: The number of independent variables
        P: The number of dependent variables

        :return:
        """

        Measures = collections.namedtuple(typename='Measures', field_names=['N', 'M', 'P'])

        # noinspection PyUnresolvedReferences
        return Measures._make((self.independent.shape[0], self.independent.shape[1],
                               self.dependent.shape[1]))

    def sections(self):
        """

        sections_: The number of sections
        instances_: The number of instances per section, therefore length(instances_) = sections_
        indices: Indices

        :return:
        """

        sections_ = self.sections_
        instances_ = self.instances_
        indices = theano.shared(
            np.repeat(np.arange(sections_), repeats=instances_))

        Sections = collections.namedtuple(typename='Sections',
                                          field_names=['sections_', 'instances_', 'indices'])

        # noinspection PyUnresolvedReferences
        return Sections._make((sections_, instances_, indices))
