'''
Created on 25 de mar de 2017

@author: rubemkalebe
'''

import data_helper
from bokeh.charts import Bar
from bokeh.charts.operations import blend
from bokeh.charts.attributes import cat
from bokeh.models.formatters import NumeralTickFormatter

class EmissionByCountryPlot(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor receiving the data
        '''
        self.__data = data
        self.__emission = {}
        self.__samples = {}
        self.__table = {}
        self.__title = ''
        
    '''
    Process data to generate relevant information
    Works on all countries
    '''
    def process(self):
        # Reset
        self.__emission.clear()
        self.__samples.clear()
        
        # Process
        for emission, regs, ct in zip(self.__data.data[data_helper.data_field['emission']],\
                               self.__data.data[data_helper.data_field['registrations']],\
                               self.__data.data[data_helper.data_field['country']]):
            if ct in self.__emission and regs != '' and emission != '':
                self.__emission[ct] += (int(regs) * float(emission))
                self.__samples[ct] += int(regs)
            elif ct != '' and ct not in self.__emission and regs != '' and emission != '':
                self.__emission[ct] = (int(regs) * float(emission))
                self.__samples[ct] = int(regs)
                
        # Update
        self.updateTable()
        
    '''
    Update fuel_table
    '''
    def updateTable(self):
        self.__table = {
            'country' : sorted(self.__emission.keys()),
            'total' : [self.__emission[x] for x in sorted(self.__emission.keys())],
            'average' : [(self.__emission[x] / self.__samples[x]) for x in sorted(self.__emission.keys())]
        }
    
    '''
    Generate average chart
    '''
    def plotAverage(self):
        bar = Bar(\
                self.__table,
                values = blend('average', name = 'average', labels_name = 'average'),\
                label = cat(columns = 'country', sort = False),\
                stack = cat(columns = 'average'),\
                agg = 'mean',\
                title = 'Average of CO2 emissions in European Union',\
                legend = False,\
                tooltips = [('Average', '@average{1.11}' + ' g/km')])
        return bar
    
    '''
    Generate total chart
    '''    
    def plotTotal(self):
        bar = Bar(\
                self.__table,
                values = blend('total', name = 'total', labels_name = 'total'),\
                label = cat(columns = 'country', sort = False),\
                stack = cat(columns = 'total'),\
                agg = 'mean',\
                title = 'Total of CO2 emissions in European Union',\
                legend = False,\
                tooltips = [('Total', '@total{1,1}' + ' g/km')])
        bar._yaxis.formatter = NumeralTickFormatter(format = '0,0')
        return bar
        
            
