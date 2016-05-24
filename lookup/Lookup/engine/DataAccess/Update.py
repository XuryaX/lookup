'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''

from dataStore import Warehouse
from dataStore.dataModels import Index, Schema, Entry


class Update(object):
    '''
    This Class will create and update database documents. Since there would be no direct editing of Index & Schema,
    only creation methods have been specified.
    '''

    def __init__(self):
        self.warehouse = Warehouse()

    def createIndex(self, indexName):
        index = Index(indexName)

        self.warehouse.createDocument(
            document=index,
            entry=None,
            schema=None,
            index=index.getIndexName(),
            prop=None)

    def createSchema(self, schemaName, indexName):
        schema = Schema(schemaName)

        self.warehouse.createDocument(
            document=schema,
            entry=None,
            schema=schema.getSchemaName(),
            index=indexName,
            prop=None)

    def createEntry(self, entryName, schemaName,
                    indexName, fieldValueDict=None):
        entry = Entry(entryName, fieldValueDict)

        self.warehouse.createDocument(
            document=entry,
            entry=entry.getEntryName(),
            schema=schemaName,
            index=indexName,
            prop=None)

    def editEntry(self, entryName, schemaName, indexName, fieldValueDict):
        self.warehouse.editDocument(
            fieldValueDict,
            Entry,
            "add",
            entry=entryName,
            schema=schemaName,
            index=indexName,
            prop=None)
