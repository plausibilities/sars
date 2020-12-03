import pandas as pd
import numpy as np

import sars.graphics.relational


class Graphs:

    def __init__(self):
        """

        """

        self.relational = sars.graphics.relational.Relational()

    def baseline(self, data: pd.DataFrame, labels):

        ax = self.relational.figure(width=4.7, height=2.9)
        ax.set_prop_cycle(color=['black', 'blue', 'red'])

        ax.plot(data.ndays, np.log(data.positiveRate), '-', label='positives/100K')
        ax.plot(data.ndays, np.log(data.hospitalizedRate), '-', label='hospitalized/100K')
        ax.plot(data.ndays, np.log(data.deathRate), '-', label='deaths/100K')

        ax.tick_params(axis='x', labelrotation=90)

        self.relational.annotation(handle=ax, labels=labels)

        return ax
