'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''
from dataStore import Warehouse
from dataStore.dataModels import Index, Schema, Entry
from dataStore.dataModels.Property import Property


class Delete(object):
    '''
    This class will delete data from the WareHouse
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.warehouse = Warehouse()

    def deleteIndex(self, indexName):
        self.warehouse.deleteDocument(
            Index,
            entry=None,
            schema=None,
            index=indexName,
            prop=None)

    def deleteSchema(self, schemaName, indexName):
        self.warehouse.deleteDocument(
            typ=Schema,
            entry=None,
            schema=schemaName,
            index=indexName,
            prop=None)

    def deleteEntry(self, entryName, schemaName, indexName):
        self.warehouse.deleteDocument(
            Entry,
            entry=entryName,
            schema=schemaName,
            index=indexName,
            prop=None)

    def deleteField(self, fieldName, schemaName, indexName):
        self.warehouse.deleteDocument(
            Property,
            entry=None,
            schema=schemaName,
            index=indexName,
            prop=fieldName)
