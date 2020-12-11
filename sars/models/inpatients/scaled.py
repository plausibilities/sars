import collections

import sars.functions.scaler


class Scaled:

    def __init__(self, data):
        """

        """
        self.data = data

        self.T = collections.namedtuple(
            typename='T',
            field_names=['xscale', 'independent', 'abscissae', 'yscale', 'dependent'])

    @staticmethod
    def scale():
        return sars.functions.scaler.Scaler()

    def independent_(self):

        scale = self.scale()
        independent = scale.fit_transform(tensor=self.data.independent)
        abscissae = scale.transform(tensor=self.data.abscissae)

        return scale, independent, abscissae

    def dependent_(self):

        scale = self.scale()
        dependent = scale.fit_transform(tensor=self.data.dependent)

        return scale, dependent

    def exc(self):
        """

        :return:
        """

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.T._make(self.independent_() + self.dependent_())
