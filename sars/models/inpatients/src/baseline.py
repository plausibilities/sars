"""
Module baseline
"""

import numpy as np
import pandas as pd


class Baseline:
    """
    Claas Baseline
    """

    def __init__(self):
        """
        Constructor
        """

        self.url = 'https://raw.githubusercontent.com/briefings/sars/develop/fundamentals/' \
                   'atlantic/warehouse/hospitalizations.csv'

        self.fields = ['datetimeobject', 'STUSPS',
                       'positiveCumulative', 'deathCumulative', 'hospitalizedCumulative',
                       'positiveRate', 'deathRate', 'hospitalizedRate', 'ndays']

        self.dtype = {'STUSPS': 'str', 'positiveCumulative': np.float64,
                      'deathCumulative': np.float64, 'hospitalizedCumulative': np.float64,
                      'positiveRate': np.float64, 'deathRate': np.float64, 'hospitalizedRate': np.float64,
                      'ndays': np.int64}

        self.parse_dates = ['datetimeobject']

    def exc(self):
        """

        :return:
        """

        try:
            return pd.read_csv(filepath_or_buffer=self.url, header=0, usecols=self.fields,
                               dtype=self.dtype, encoding='utf-8', parse_dates=self.parse_dates)
        except OSError as err:
            raise Exception(err.strerror) from err
