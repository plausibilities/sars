import theano
import numpy as np

import sars.functions.scaler



class Structures:

    def __init__(self, dependents: int):
        """

        """
        self.dependents = dependents

    @staticmethod
    def scale():

        return sars.functions.scaler.Scaler()

    def share(self, tensor: np.ndarray, predictor: bool):

        if predictor:
            shared = theano.shared(np.repeat(tensor, self.dependents, axis=1))
        else:
            shared = theano.shared(tensor)
            
        return shared
            
    def exc(self, tensor: np.ndarray, predictor: bool):

        scaler = self.scale()

        transformed = scaler.fit_transform(tensor=tensor)

        shared = self.share(tensor=transformed, predictor=predictor)

        return scaler, transformed, shared
