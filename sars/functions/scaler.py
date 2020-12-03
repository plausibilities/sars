"""
Module scaler
"""


class Scaler:
    """
    Class Scaler

    Scales & De-scales
    """

    def __init__(self):

        self.mean_ = None
        self.std_ = None

    def transform(self, tensor):
        """

        :param tensor:
        :return:
        """

        return (tensor - self.mean_) / self.std_

    def fit_transform(self, tensor):
        """

        :param tensor:
        :return:
        """

        self.mean_ = tensor.mean(axis=0)
        self.std_ = tensor.std(axis=0)

        return self.transform(tensor)

    def inverse_transform(self, tensor):
        """

        :param tensor:
        :return:
        """

        return tensor*self.std_ + self.mean_
