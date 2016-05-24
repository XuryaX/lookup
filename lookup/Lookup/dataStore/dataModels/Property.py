'''
Created on May 1, 2016

@author: Shauryadeep Chaudhuri
'''

import json

from ..helpers import JsonLoader


class Property(object):
    '''
    This is the model of Indices which will store different types of Entrys
    '''

    def __init__(self, PropertyName=None, EntryDict=None, jsonrep=None):
        '''
        Constructor
        '''

        self.PropertyName = None
        self.EntryDict = {}
        self.type = None

        if not jsonrep:
            if PropertyName and EntryDict:
                self.PropertyName = PropertyName
                self.checkType(EntryDict)
                self.EntryDict = EntryDict

            else:
                if PropertyName:
                    self.PropertyName = PropertyName
                else:
                    raise Exception(
                        "Property Name is required to make a new Property")
        else:
            dataDictionary = JsonLoader(jsonrep)

            if len(dataDictionary.keys()) != 3:
                raise Exception("Invalid Json Format")
            for key in dataDictionary.keys():
                if key not in self.__dict__:
                    raise Exception("Invalid Json Format")

            self.__dict__ = dataDictionary

    def getPropertyName(self):
        self.getPropertyName()

    def checkType(self, EntryDict):
        if not self.EntryDict.keys():
            for val in EntryDict:
                if not self.type:
                    self.type = type(val)
                    break
        for val in EntryDict.keys():
            if not isinstance(val, self.type):
                raise TypeError(
                    "All Types must be of same type of a field, type of a field cannot be changed once set")

    def addEntryDict(self, EntryDict):
        if not isinstance(EntryDict, dict):
            raise TypeError(
                "Must provide a Dict in format of {propertyValue:entryName}")

        self.checkType(EntryDict)

        for field in EntryDict.keys():

            if str(field) not in self.EntryDict:
                self.EntryDict[str(field)] = list()

            if(isinstance(EntryDict[field], list)):
                self.EntryDict[str(field)].extend(EntryDict[field])
            else:
                self.EntryDict[str(field)].append(EntryDict[field])

    def delEntry(self, EntryName, propertyValue=None):
        if propertyValue:
            self.EntryDict[propertyValue].remove(EntryName)
        else:
            for value in self.EntryDict.keys():
                try:
                    self.EntryDict[value].remove(EntryName)
                except:
                    pass

    def getEntryDict(self):
        return self.EntryDict

    def getType(self):
        return self.type

    def hasValue(self, fieldValue):
        return fieldValue in self.EntryDict.keys()

    def getJson(self):
        self.type = str(self.type)
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.getJson())

    def __repr__(self):
        return self.__str__()
