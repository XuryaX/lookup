'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''

import json

from ..helpers import JsonLoader


class Index(object):
    '''
    This is the model of Indices which will store different types of documents
    '''

    def __init__(self, IndexName=None, SchemaList=None, jsonrep=None):
        '''
        Constructor
        '''

        self.IndexName = None
        self.SchemaList = list()

        if not jsonrep:
            if IndexName and SchemaList:
                self.IndexName = IndexName
                self.SchemaList = SchemaList
            elif IndexName:
                self.IndexName = IndexName
            else:
                raise Exception("IndexName or JSON representation needed")
        else:
            dataDictionary = JsonLoader(jsonrep)

            if len(dataDictionary.keys()) != 2:
                raise Exception("Invalid Json Format")
            for key in dataDictionary.keys():
                if key not in self.__dict__:
                    raise Exception("Invalid Json Format")

            self.__dict__ = dataDictionary

    def getIndexName(self):
        return self.IndexName

    def getSchemaList(self):
        return self.SchemaList

    def addSchemaList(self, data):

        for schema in data:
            if schema in self.SchemaList:
                raise Exception(
                    "Schema " + schema + " already present in Index")

        self.SchemaList.append(list(data))

    def addSchema(self, data):
        if(data not in self.SchemaList):
            self.SchemaList.append(str(data))
        else:
            raise Exception("Schema " + data + " already present in Index")

    def delSchema(self, data):
        try:
            self.SchemaList.remove(str(data))
        except:
            raise Exception("Schema " + data + " Does not exist in Index")

    def delSchemaList(self, data):
        for schema in data:
            if schema not in self.SchemaList:
                raise Exception(
                    "Schema " + schema + " does not exist in Index")

        for schema in list(data):
            self.SchemaList.remove(schema)

    def hasSchema(self, schema):
        return schema in self.SchemaList

    def getJson(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.getJson())

    def __repr__(self):
        return self.__str__()
