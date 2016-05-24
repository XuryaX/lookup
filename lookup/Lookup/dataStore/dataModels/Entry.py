'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''

import json

from ..helpers import JsonLoader


class Entry(object):
    '''
    This is the model of Indices which will store different types of Entrys
    '''

    def __init__(self, EntryName=None, fields=None, jsonrep=None):
        '''
        Constructor
        '''
        self.version = 1
        self.EntryName = None
        self.fields = dict()

        if not jsonrep:
            if EntryName and fields:
                self.EntryName = EntryName
                self.fields = fields
            elif EntryName:
                self.IndexName = EntryName
            else:
                raise Exception("Entry name or JSON representation needed")
        else:
            dataDictionary = JsonLoader(jsonrep)

            if len(dataDictionary.keys()) != 3:
                raise Exception("Invalid Json Format")
            for key in dataDictionary.keys():
                if key not in self.__dict__:
                    raise Exception("Invalid Json Format")

            self.__dict__ = dataDictionary

    def getEntryName(self):
        return self.EntryName

    def updateField(self, fieldValueDict):
        if(not isinstance(fieldValueDict, dict)):
            raise TypeError(
                "Value Must be a dictionary with Field as Key and its Value as Value")

        for field in fieldValueDict.keys():
            self.fields[field] = fieldValueDict[field]

        self.version = self.version + 1

    def delFields(self, fields):
        for field in fields:
            try:
                del self.fields[str(field)]
            except KeyError:
                pass
        self.version = self.version + 1

    def delField(self, field):
        try:
            del self.fields[str(field)]
            self.version = self.version + 1
        except KeyError:
            pass

    def getFieldValueDict(self):
        return self.fields

    def getFields(self):
        return self.fields.keys()

    def getJson(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.getJson())

    def __repr__(self):
        return self.__str__()
