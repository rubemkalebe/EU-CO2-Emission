'''
Created on 27 de mar de 2017

@author: rubemkalebe
'''

import data_helper
from bokeh.charts import Bar
from bokeh.charts.operations import blend
from bokeh.charts.attributes import cat
from bokeh.models.formatters import NumeralTickFormatter

class RegistrationsByCountryPlot(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor receiving the data
        '''
        self.__data = data
        self.__regs = {}
        self.__table = {}
        
    '''
    Process data to generate relevant information
    Works on all countries
    '''
    def process(self):
        # Reset
        self.__regs.clear()
        
        # Process
        for regs, ct in zip(self.__data.data[data_helper.data_field['registrations']],\
                            self.__data.data[data_helper.data_field['country']]):
            if ct in self.__regs and regs != '':
                self.__regs[ct] += int(regs)
            elif ct != '' and ct not in self.__regs and regs != '':
                self.__regs[ct] = int(regs)
                
        # Update
        self.updateTable()
        
    '''
    Update fuel_table
    '''
    def updateTable(self):
        self.__table = {
            'country' : sorted(self.__regs.keys()),\
            'registrations' : [self.__regs[x] for x in sorted(self.__regs.keys())]
        }
    
    '''
    Generate total chart
    '''    
    def plot(self):
        bar = Bar(\
                self.__table,
                values = blend('registrations', name = 'registrations', labels_name = 'registrations'),\
                label = cat(columns = 'country', sort = False),\
                stack = cat(columns = 'registrations'),\
                agg = 'mean',\
                title = 'Total of new registrations in European Union',\
                legend = False,\
                tooltips = [('Registrations', '@registrations{1,1}')])
        bar._yaxis.formatter = NumeralTickFormatter(format = '0,0')
        return bar
        
            
