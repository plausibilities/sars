import numpy as np
import pandas as pd


class Data:

    def __init__(self):

        self.url = 'https://raw.githubusercontent.com/briefings/sars/develop/fundamentals/' \
                   'atlantic/warehouse/hospitalizations.csv'

        self.fields = ['datetimeobject', 'STUSPS',
                       'positiveRate', 'testRate', 'deathRate', 'hospitalizedRate', 'icuRate', 'ndays']

        self.dtype = {'STUSPS': 'str',
                      'positiveRate': np.float64, 'testRate': np.float64, 'deathRate': np.float64,
                      'hospitalizedRate': np.float64, 'icuRate': np.float64, 'ndays': np.int64}

        self.parse_dates = ['datetimeobject']

    def read(self):

        try:
            return pd.read_csv(filepath_or_buffer=self.url, header=0, usecols=self.fields,
                               dtype=self.dtype, encoding='utf-8', parse_dates=self.parse_dates)
        except OSError as err:
            raise Exception(err.strerror)
