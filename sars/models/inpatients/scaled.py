"""
Module scaled
"""

import collections

import sars.functions.scaler


class Scaled:
    """
    Class Scaled
    """

    def __init__(self, data):
        """

        :param data:
        """

        self.data = data

        self.Scaled = collections.namedtuple(
            typename='Scaled',
            field_names=['xscale', 'independent', 'abscissae', 'yscale', 'dependent'])  # pylint: disable=C0103

    @staticmethod
    def scale():
        """

        :return:
        """

        return sars.functions.scaler.Scaler()

    def independent_(self):
        """
        Creates the scale object for independent variables, and the scaled (a) independent tensor,
        and (b) extended independent tensor that includes prediction points.

        :return:
        """

        scale = self.scale()
        independent = scale.fit_transform(tensor=self.data.independent)
        abscissae = scale.transform(tensor=self.data.abscissae)

        return scale, independent, abscissae

    def dependent_(self):
        """
        Creates the scale object for dependent variables, and the scaled dependent tensor

        :return:
        """

        scale = self.scale()
        dependent = scale.fit_transform(tensor=self.data.dependent)

        return scale, dependent

    def exc(self):
        """

        :return:
        """

        # noinspection PyUnresolvedReferences,PyProtectedMember
        return self.Scaled._make(self.independent_() + self.dependent_())
