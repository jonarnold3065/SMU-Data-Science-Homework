import pandas as pd
import numpy as np
from sqlhelper_climate import SQLFactoryHelper

class SQL_C_factory():
    def __init__(self):
        self.SQL_C_factory = SQLFactoryHelper()

    ##################################################################
    ################## QUERY FUNCTIONS ##############################
    ##################################################################

    def precipitation(self):
        query = self.sqlhelper_climate.readSQLQuery('precipitation.sql')
        data = self.sqlhelper_climate.executeQuery(query) # read in using helper function
        return(data)

    def tempature(self):
        query = self.sqlhelper_climate.readSQLQuery('most_active_station.sql')
        data = self.sqlhelper_climate.executeQuery(query) # read in using helper function
        return(data)

    def start_date(self, invoiceId):
        query = self.sqlhelper_climate.readSQLQueryWithReplacement('active_stations.sql', invoiceId)
        data = self.sqlhelper_climate.executeQuery(query) # read in using helper function
        return(data)