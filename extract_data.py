'''
Created on 23 de mar de 2017

@author: rubemkalebe
'''

import pandas
import numpy
from bokeh.models import ColumnDataSource

class ExtractData(object):
    '''
    Class responsible for reading the data file
    '''


    def __init__(self, filepath = 'dataset/CO2_passenger_cars_v12_cleaned.csv'):
        '''
        Constructor with filepath
        '''
        self.__FILEPATH = filepath
        
    '''
    It reads the data file and returns a ColumnDataSource object with no NaN
    '''
    def extract(self):
        # Interpreter claimed for low_memory parameter
        data = pandas.read_csv(self.__FILEPATH, encoding = 'latin2', low_memory = False)
        
        # Replace NaN cells with an empty string
        data = data.replace(numpy.nan, '', regex=True)
        
        return ColumnDataSource(data)
