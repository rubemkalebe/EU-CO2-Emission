'''
Created on 25 de mar de 2017

@author: rubemkalebe
'''

from data import data_helper
from bokeh.charts import Bar
from bokeh.charts.operations import blend
from bokeh.charts.attributes import cat

class EmissionByMakePlot(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor receiving the data
        '''
        self.__data = data
        self.__makes = {}
        self.__table = {}
        self.__title = ''
        
    '''
    Process data to generate relevant information
    Works on all countries
    '''
    def process(self):
        # Reset
        self.__makes.clear()
        
        # Process
        for emission, regs, make in zip(self.__data.data[data_helper.data_field['emission']],\
                               self.__data.data[data_helper.data_field['registrations']],\
                               self.__data.data[data_helper.data_field['make']]):
            if make in self.__makes and emission != '':
                self.__makes[make] += (int(regs) * float(emission))
            elif make != '' and make not in self.__makes and emission != '':
                self.__makes[make] = (int(regs) * float(emission))
                
        # Update
        self.updateTable()
        self.__title = 'Emission by make in European Union'

    '''
    Process data by country to generate relevant information
    '''
    def processByCountry(self, country):
        # Reset
        self.__makes.clear()
        
        # Process
        for emission, regs, make, ct in zip(self.__data.data[data_helper.data_field['emission']],\
                               self.__data.data[data_helper.data_field['registrations']],\
                               self.__data.data[data_helper.data_field['make']],\
                               self.__data.data[data_helper.data_field['country']]):
            if make in self.__makes and ct == country and emission != '':
                self.__makes[make] += (int(regs) * float(emission))
            elif make != '' and make not in self.__makes and ct == country and emission != '':
                self.__makes[make] = (int(regs) * float(emission))
                
        # Update
        self.updateTable()
        self.__title = 'Emission by make in ' + data_helper.country[country]
        
    '''
    Update fuel_table
    '''
    def updateTable(self):
        self.__table = {
            'make' : sorted(self.__makes.keys()),
            'emission' : [self.__makes[x] for x in sorted(self.__makes.keys())]
        }
    
    '''
    Generate chart
    '''
    def plot(self):
        bar = Bar(\
                self.__table,
                values = blend('emission', name = 'emission', labels_name = 'emission'),\
                label = cat(columns = 'make'),\
                stack = cat(columns = 'emission'),\
                agg = 'mean',\
                title = self.__title,\
                legend = False,\
                tooltips = [('Emission', '@emission')])
        return bar