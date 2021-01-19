"""
Module graphs
"""

import collections
import math

import matplotlib.pyplot as plt
import numpy as np

import sars.graphics.relational


# noinspection PyUnresolvedReferences,PyProtectedMember
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

        self.relational = sars.graphics.relational.Relational()
        self.RelationalGraphLabels = collections.namedtuple(
            typename='RelationalGraphLabels', field_names=['title', 'xlabel', 'ylabel'])

    def together(self, ylabel: str = 'y', xlabel: str = 'x'):
        """

        :param ylabel:
        :param xlabel:
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

        # Annotations
        ax_.tick_params(axis='x', labelrotation=90)
        self.relational.annotation(handle=ax_, labels=self.RelationalGraphLabels._make(
            ['\ndata curves\n', '\n{}'.format(xlabel), '{}\n'.format(ylabel)]))
        ax_.legend(loc='lower right', fontsize='small')

    def get_separate(self, handle, index: int, xlabel: str = 'x'):
        """

        :param handle: The graph handle
        :param index: The subplot figure identifier
        :param xlabel: The name of the x-axis variates
        :return:
        """

        # Colours
        cc_ = ['k', 'b', 'r']

        # The curves
        handle.plot(self.fields.extended, self.predictions.lines[:, :, index].T,
                    '#cccc4d', alpha=0.6, label=None)

        handle.plot(self.fields.initial, self.data.dependent[:, index][:, None],
                    '{}o'.format(cc_[index]), alpha=0.15, markersize=4.25, label='observations')

        handle.plot(self.fields.extended, self.predictions.line[:, index][:, None],
                    '{}-'.format(cc_[index]), linewidth=0.95, label='est. (via Mean)')

        # Attributes of ticks
        handle.tick_params(axis='both', labelsize='small')
        handle.tick_params(axis='x', labelrotation=90)

        # Annotations
        handle.set_xlabel('\n{}'.format(xlabel), fontsize='small')
        handle.set_ylabel('{}\n'.format(self.titles[index]), fontsize='small')
        handle.legend(loc='upper left', fontsize='small')

    def separate(self, adjust: np.ndarray, layout: np.ndarray, xlabel: str):
        """
        plt.subplots(nrows=1, ncols=ncols, figsize=(9.1, 2.1), constrained_layout=False)

        :param adjust:
        :param layout:
        :param xlabel:
        :return:
        """

        # The number of curves
        nlines = self.predictions.line.shape[1]

        # Proceed
        fig, handle = plt.subplots(nrows=math.ceil(nlines / 2), ncols=2)
        fig.subplots_adjust(hspace=adjust[0], wspace=adjust[1])
        fig.tight_layout(h_pad=layout[0], w_pad=layout[1])

        for i in range(nlines):
            self.get_separate(handle=handle[i // 2, i % 2], index=i, xlabel=xlabel)

        # Delete the final/empty subplot
        if (nlines // 2) > 0:
            plt.delaxes(handle[nlines // 2, nlines % 2])

        return fig, handle
