'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''

import json

from ..helpers import JsonLoader


class Schema(object):
    '''
    This is the model of Schemas which will store different types of documents
    '''

    def __init__(self, SchemaName=None, FieldType=None, jsonrep=None):
        '''
        Constructor
        '''

        self.SchemaName = None
        self.FieldType = dict()
        self.EntryList = list()

        if not jsonrep:
            if SchemaName and FieldType:
                self.SchemaName = SchemaName
                self.FieldType = FieldType
            elif SchemaName:
                self.SchemaName = SchemaName
            else:
                raise Exception("IndexName or JSON representation needed")
        else:
            dataDictionary = JsonLoader(jsonrep)
            if len(dataDictionary.keys()) != 3:
                raise Exception("Invalid Json Format")
            for key in dataDictionary.keys():
                if key not in self.__dict__:
                    raise Exception("Invalid Json Format")

            self.__dict__ = dataDictionary

    def getSchemaName(self):
        return self.SchemaName

    def getEntryList(self):
        return self.EntryList

    def addEntry(self, data):
        if data not in self.EntryList:
            self.EntryList.append(str(data))

    def addField(self, data):
        try:
            self.FieldType.update(data)
        except:
            raise ValueError(
                "Data should be a dictionary with field name and field type. ex:- {\"fieldname\":\"fieldtype\"}")

    def delField(self, field):
        if field in self.FieldType.keys():
            del self.FieldType[field]

    def delEntry(self, entry):
        if entry in self.EntryList:
            self.EntryList.remove(entry)

    def delFields(self, fields):
        for field in fields:
            self.delField(field)

    def delEntries(self, entries):
        for entry in entries:
            self.delEntry(entry)

    def hasEntry(self, entry):
        return entry in self.EntryList

    def hasField(self, field):
        return field in self.FieldType.keys()

    def getFieldType(self, field):
        if self.hasField(field):
            return self.FieldType[field]

    def getFields(self):
        return self.FieldType.keys()

    def getJson(self):
        for fieldName in self.FieldType.keys():
            self.FieldType[fieldName] = str(self.FieldType[fieldName])
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.getJson())

    def __repr__(self):
        return self.__str__()
