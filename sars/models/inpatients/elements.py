import collections

import numpy as np
import theano


class Elements:

    def __init__(self, sections_: int, instances_: np.ndarray):
        """

        :param sections_:
        :param instances_:
        """

        self.sections_ = sections_
        self.instances_ = instances_

        self.Elements = collections.namedtuple(typename='Elements',
                                               field_names=['sections_', 'instances_', 'indices'])

    def exc(self):
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

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.Elements._make((sections_, instances_, indices))
