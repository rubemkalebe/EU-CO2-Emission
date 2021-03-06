'''
Created on 25 de mar de 2017

@author: rubemkalebe
'''

import data_helper
from bokeh.charts import Bar
from bokeh.charts.operations import blend
from bokeh.charts.attributes import cat
from bokeh.models.formatters import NumeralTickFormatter

class FuelTypePlot(object):
    '''
    Generate charts with fuel type information
    '''


    def __init__(self, data):
        '''
        Constructor receiving the data
        '''
        self.__data = data
        self.__fuel_types = {}
        self.__fuel_table = {}
        self.__samples = 0
        self.__title = ''
        
    '''
    Process data to generate relevant information
    Works on all countries
    '''
    def process(self):
        # Reset
        self.__samples = 0
        self.__fuel_types.clear()
        
        # Process
        for ftype, regs in zip(self.__data.data[data_helper.data_field['fuel_type']],\
                               self.__data.data[data_helper.data_field['registrations']]):
            if ftype in self.__fuel_types and regs != '':
                self.__fuel_types[ftype] += int(regs)
                self.__samples += int(regs)
            elif ftype != '' and ftype not in self.__fuel_types and regs != '':
                self.__fuel_types[ftype] = int(regs)
                self.__samples += int(regs)
                
        # Update
        self.updateTable()
        self.__title = 'Fuel types in use in European Union'

    '''
    Process data by country to generate relevant information
    '''
    def processByCountry(self, country):
        # Reset
        self.__samples = 0
        self.__fuel_types.clear()
        
        # Process
        for ftype, regs, ct in zip(self.__data.data[data_helper.data_field['fuel_type']],\
                               self.__data.data[data_helper.data_field['registrations']],\
                               self.__data.data[data_helper.data_field['country']]):
            if ftype in self.__fuel_types and ct == country and regs != '':
                self.__fuel_types[ftype] += int(regs)
                self.__samples += int(regs)
            elif ftype != '' and ftype not in self.__fuel_types and ct == country and regs != '':
                self.__fuel_types[ftype] = int(regs)
                self.__samples += int(regs)
                
        # Update
        self.updateTable()
        self.__title = 'Fuel types in use in ' + data_helper.country[country]
        
    '''
    Update fuel_table
    '''
    def updateTable(self):
        self.__fuel_table = {
            'fuel' : sorted(self.__fuel_types.keys()),
            'percentage' : [((self.__fuel_types[x] / self.__samples))\
                             for x in sorted(self.__fuel_types.keys())]
        }
    
    '''
    Generate chart
    '''
    def plot(self):
        bar = Bar(\
                self.__fuel_table,
                values = blend('percentage', name = 'percentage', labels_name = 'percentage'),\
                label = cat(columns = 'fuel'),\
                stack = cat(columns = 'percentage'),\
                agg = 'mean',\
                title = self.__title,\
                legend = False,\
                tooltips = [('Percentage', '@percentage{0.00%}')])
        bar._yaxis.formatter = NumeralTickFormatter(format = '0%')
        return bar
