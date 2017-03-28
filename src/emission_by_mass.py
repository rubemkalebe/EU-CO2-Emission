'''
Created on 25 de mar de 2017

@author: rubemkalebe
'''

from data import data_helper
from bokeh.plotting.figure import figure

class EmissionByMassPlot(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor receiving the data
        '''
        self.__data = data
        
    def plot(self):
        p = figure(x_axis_label = 'mass (kg)', y_axis_label = 'emission (g/km)',
          title = 'Mass x Emission in European Union')
        p.circle(data_helper.data_field['mass'], data_helper.data_field['emission'],\
                source = self.__data)
        return p