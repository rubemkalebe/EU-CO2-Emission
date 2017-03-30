'''
Created on 25 de mar de 2017

@author: rubemkalebe
'''

import data_helper
from bokeh.charts import Bar
from bokeh.charts.operations import blend
from bokeh.charts.attributes import cat
from bokeh.models.formatters import NumeralTickFormatter

class EmissionByFuelPlot(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor receiving the data
        '''
        self.__data = data
        self.__fuel = {}
        self.__table = {}
        self.__samples = {}
        self.__title = ''
        
    '''
    Process data to generate relevant information
    Works on all countries
    '''
    def process(self):
        # Reset
        self.__samples.clear()
        self.__fuel.clear()
        
        # Process
        for emission, regs, ftype in zip(self.__data.data[data_helper.data_field['emission']],\
                               self.__data.data[data_helper.data_field['registrations']],\
                               self.__data.data[data_helper.data_field['fuel_type']]):
            if ftype in self.__fuel and regs != '' and emission != '':
                self.__fuel[ftype] += (int(regs) * float(emission))
                self.__samples[ftype] += int(regs)
            elif ftype != '' and ftype not in self.__fuel and regs != '' and emission != '':
                self.__fuel[ftype] = (int(regs) * float(emission))
                self.__samples[ftype] = int(regs)
                
        # Update
        self.updateTable()
        self.__title = 'European Union'
        
    '''
    Process data by country to generate relevant information
    '''
    def processByCountry(self, country):
        # Reset
        self.__samples.clear()
        self.__fuel.clear()
        
        # Process
        for emission, regs, ftype, ct in zip(self.__data.data[data_helper.data_field['emission']],\
                               self.__data.data[data_helper.data_field['registrations']],\
                               self.__data.data[data_helper.data_field['fuel_type']],\
                               self.__data.data[data_helper.data_field['country']]):
            if ftype in self.__fuel and regs != '' and emission != '' and ct == country:
                self.__fuel[ftype] += (int(regs) * float(emission))
                self.__samples[ftype] += int(regs)
            elif ftype != '' and ftype not in self.__fuel and regs != '' and\
                    emission != '' and ct == country:
                self.__fuel[ftype] = (int(regs) * float(emission))
                self.__samples[ftype] = int(regs)
                
        # Update
        self.updateTable()
        self.__title = data_helper.country[country]
        
    '''
    Update table
    '''
    def updateTable(self):
        self.__table = {
            'fuel' : sorted(self.__fuel.keys()),
            'total' : [self.__fuel[x] for x in sorted(self.__fuel.keys())],
            'average' : [(self.__fuel[x] / self.__samples[x]) for x in sorted(self.__fuel.keys())]
        }
        
    '''
    Generate chart
    '''
    def plotAverage(self):
        bar = Bar(\
                self.__table,
                values = blend('average', name = 'average', labels_name = 'average'),\
                label = cat(columns = 'fuel'),\
                stack = cat(columns = 'average'),\
                agg = 'mean',\
                title = 'Average of CO2 emissions in ' + self.__title,\
                legend = False,\
                tooltips = [('Average', '@average{1.11}' + ' g/km')])
        return bar

    '''
    Generate chart
    '''
    def plotTotal(self):
        bar = Bar(\
                self.__table,
                values = blend('total', name = 'total', labels_name = 'total'),\
                label = cat(columns = 'fuel'),\
                stack = cat(columns = 'total'),\
                agg = 'mean',\
                title = 'Total of CO2 emissions in ' + self.__title,\
                legend = False,\
                tooltips = [('Total', '@total{1,1}' + ' g/km')])
        bar._yaxis.formatter = NumeralTickFormatter(format = '0,0' + ' g/km')
        return bar
