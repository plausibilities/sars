"""
Module graphs
"""

import collections

import matplotlib.pyplot as plt
import numpy as np

import sars.graphics.relational


class Graphs:
    """
    Class Graphs
    """

    def __init__(self, data: collections.namedtuple, predictions: collections.namedtuple,
                 titles: tuple, fields: collections.namedtuple):
        """

        :param data:
        :param predictions:
        :param titles:
        :param fields: The x-axis fields
        """

        # pylint: disable=C0103

        self.data = data
        self.predictions = predictions
        self.titles = titles
        self.fields = fields

        self.colours = ['black', 'blue', 'red']
        self.cc_ = ['k', 'b', 'r']

        self.relational = sars.graphics.relational.Relational()
        self.RelationalGraphLabels = collections.namedtuple(
            typename='RelationalGraphLabels', field_names=['title', 'xlabel', 'ylabel'])

    def together(self, ylabel: str = 'y'):
        """

        :return:
        """

        ax_ = self.relational.figure(width=4.7, height=3.3)
        ax_.set_prop_cycle(color=self.colours)

        # The curves
        for i in np.arange(self.data.dependent.shape[1]):
            ax_.plot(self.fields.initial, np.log(self.data.dependent[:, i]), 'o',
                     alpha=0.15, label=None)

        for i in np.arange(self.predictions.line.shape[1]):
            ax_.plot(self.fields.extended, np.log(self.predictions.line[:, i]), '-',
                     linewidth=0.95, label=('est. ln(' + self.titles[i] + ')'))

        # Attributes of ticks
        ax_.tick_params(axis='x', labelrotation=90)

        # Annotations
        # noinspection PyProtectedMember,PyUnresolvedReferences
        self.relational.annotation(
            handle=ax_,
            labels=self.RelationalGraphLabels._make(['\ndata\n', '\ndays thus far', '{}\n'.format(ylabel)]))

        ax_.legend(loc='lower right', fontsize='small')

    def getseparate(self, handle, index: int):
        """

        :param handle:
        :param index:
        :return:
        """

        # The curves
        handle.plot(self.fields.extended, self.predictions.lines[:, :, index].T,
                    '#cccc4d', alpha=0.6, label=None)

        handle.plot(self.fields.initial, self.data.dependent[:, index][:, None],
                    '{}o'.format(self.cc_[index]), alpha=0.15, markersize=4.25, label='observations')

        handle.plot(self.fields.extended, self.predictions.line[:, index][:, None],
                    '{}-'.format(self.cc_[index]), linewidth=0.95, label='est. (via Mean)')

        # Attributes of ticks
        handle.tick_params(axis='both', labelsize='small')
        handle.tick_params(axis='x', labelrotation=90)

        # Annotations
        handle.set_xlabel('\ndays thus far', fontsize='small')
        handle.set_ylabel('{}\n'.format(self.titles[index]), fontsize='small')

        handle.legend(loc='upper left', fontsize='small')

    def separate(self, adjust: np.ndarray, layout: np.ndarray):
        """

        :return:
        """

        ncols = self.predictions.line.shape[1]
        fig, handle = plt.subplots(nrows=1, ncols=ncols, figsize=(9.1, 2.1), constrained_layout=False)

        fig.subplots_adjust(hspace=adjust[0], wspace=adjust[1])
        fig.tight_layout(h_pad=layout[0], w_pad=layout[1])

        for i in range(ncols):
            self.getseparate(handle=handle[i], index=i)

        return fig, handle
