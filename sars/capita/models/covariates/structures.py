import numpy as np

import sars.functions.scaler


class Structures:

    def __init__(self):
        """

        """

    @staticmethod
    def scale():
        return sars.functions.scaler.Scaler()

    def exc(self, tensor: np.ndarray):
        """

        :param tensor:
        :return:
        """

        scaler = self.scale()

        scaled = scaler.fit_transform(tensor=tensor)

        return scaler, scaled
