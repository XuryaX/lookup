'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''

from dataStore import Warehouse
from dataStore.dataModels import Index, Schema, Entry, Property


class Search(object):
    '''
    This class will search for data in the warehouse.
    '''

    def __init__(self, index=None, schema=None):
        '''
        Constructor
        '''
        self.warehouse = Warehouse()
        self.index = index
        self.schema = schema

    def setSchema(self, schema):
        self.schema = schema

    def setIndex(self, index):
        self.index = index

    def checkSchema(self, schemaName):
        if not schemaName:
            if not self.schema:
                raise Exception(
                    "Please provide a schema name during obejct creation or method call")
            schemaName = self.schema
        return schemaName

    def checkIndex(self, indexName):
        if not indexName:
            if not self.index:
                raise Exception(
                    "Please provide a schema name during obejct creation or method call")
            indexName = self.index
        return indexName

    def entryInSchema(self, entryName, schemaName=None, indexName=None):

        schemaName, indexName = self.checkSchema(
            schemaName), self.checkIndex(indexName)

        schema = self.warehouse.getDocument(
            Schema,
            entry=None,
            schema=schemaName,
            index=indexName,
            prop=None)

        if schema.hasEntry(entryName):
            return True
        else:
            return False

    def schemaHasProperty(self, propertyName, schemaName=None, indexName=None):

        schemaName, indexName = self.checkSchema(
            schemaName), self.checkIndex(indexName)

        schema = self.warehouse.getDocument(
            Schema,
            entry=None,
            schema=schemaName,
            index=indexName,
            prop=None)

        fields = schema.getFields()

        if propertyName in fields:
            return True
        else:
            return False

    '''Getter Methods that would get specific documents as specified by the client'''

    def getSchemaListOfIndex(self, indexName=None):

        indexName = self.checkIndex(indexName)

        index = self.warehouse.getDocument(
            Index, entry=None, schema=None, index=indexName, prop=None)

        return index.getSchemaList()

    def getEntryListofSchema(self, schemaName=None, indexName=None):

        schemaName, indexName = self.checkSchema(
            schemaName), self.checkIndex(indexName)

        schema = self.warehouse.getDocument(
            Schema,
            entry=None,
            schema=schemaName,
            index=indexName,
            prop=None)

        return schema.getEntryList()

    def getEntry(self, entryName, schemaName=None, indexName=None):

        schemaName, indexName = self.checkSchema(
            schemaName), self.checkIndex(indexName)

        return self.warehouse.getDocument(
            Entry, entry=entryName, schema=schemaName, index=indexName, prop=None)

    # Search that will result entries with same value, for Full Text Search as
    # well as Integer & Boolean Searches

    '''Search Methods'''

    def SearchEntryInProperty(self, value, operator,
                              propertyName, schemaName=None, indexName=None):

        schemaName, indexName = self.checkSchema(
            schemaName), self.checkIndex(indexName)

        prop = self.warehouse.getDocument(
            Property,
            entry=None,
            schema=schemaName,
            index=indexName,
            prop=propertyName)

        if operator == "==":
            searchFunction = self.searchInPropertyByValue
        elif operator == "<":
            searchFunction = self.searchLowerValue
        elif operator == "<=":
            searchFunction = self.searchEqualLowerValue
        elif operator == ">":
            searchFunction = self.searchGreaterValue
        elif operator == ">=":
            searchFunction = self.searchEqualGreaterValue
        elif operator == "!=":
            searchFunction = self.searchNotEqual
        elif operator == "has":
            searchFunction = self.searchHas
        elif operator == "in":
            searchFunction = self.searchIn
        elif operator == "hasnot":
            searchFunction = self.searchHasNot
        elif operator == "notin":
            searchFunction = self.searchNotIn
        else:
            raise Exception("Invalid Comparison Operand")

        return searchFunction(value, prop)

    def searchHasNot(self, value, prop):

        hasSet = set()
        otherValSet = set()

        value = value.split(',')

        propEntryDict = prop.getEntryDict()
        for val in propEntryDict.keys():
            if val in value:
                if hasSet:
                    hasSet.intersection_update(set(propEntryDict[val]))
                else:
                    hasSet.update(set(propEntryDict[val]))
            else:
                otherValSet.update(set(propEntryDict[val]))

        resultSet = otherValSet.difference(hasSet)

        return resultSet

    def searchNotIn(self, value, prop):

        inSet = set()

        otherValSet = set()

        value = value.split(',')

        propEntryDict = prop.getEntryDict()
        for val in propEntryDict:
            if val in value:
                inSet.update(set(propEntryDict[val]))
            else:
                otherValSet.update(set(propEntryDict[val]))

        resultSet = otherValSet.difference(inSet)
        return resultSet

    def searchHas(self, value, prop):

        resultSet = set()

        value = value.split(',')

        propEntryDict = prop.getEntryDict()
        for val in value:
            if val in propEntryDict.keys():
                if resultSet:
                    resultSet.intersection_update(set(propEntryDict[val]))
                else:
                    resultSet.update(set(propEntryDict[val]))

        return resultSet

    def searchIn(self, value, prop):

        resultSet = set()

        value = value.split(',')

        propEntryDict = prop.getEntryDict()
        for val in value:
            if val in propEntryDict.keys():
                resultSet.update(set(propEntryDict[val]))

        return resultSet

    def searchInPropertyByValue(self, value, prop):

        propEntryDict = prop.getEntryDict()

        if value in propEntryDict.keys():
            return propEntryDict[value]
        else:
            return []

    def searchNotEqual(self, value, prop):

        propEntryDict = prop.getEntryDict()

        elementList = list()

        for fieldValue in propEntryDict.keys():
            if value != fieldValue:
                elementList.extend(propEntryDict[fieldValue])

        return elementList

    '''Methods which would be used for Searches with comparison operators for Number type data types.'''

    def searchGreaterValue(self, value, prop):
        propEntryDict = prop.getEntryDict()
        entryList = list()
        propType = prop.getType()

        for propValue in propEntryDict:

            if propType(propValue) > propType(value):
                entryList.extend(propEntryDict[propValue])

        return entryList

    def searchLowerValue(self, value, prop):
        propEntryDict = prop.getEntryDict()
        entryList = list()
        propType = prop.getType()

        for propValue in propEntryDict:

            if propType(propValue) < propType(value):
                entryList.extend(propEntryDict[propValue])

        return entryList

    def searchEqualGreaterValue(self, value, prop):
        propEntryDict = prop.getEntryDict()
        entryList = list()
        propType = prop.getType()

        for propValue in propEntryDict:

            if propType(propValue) >= propType(value):
                entryList.extend(propEntryDict[propValue])

        return entryList

    def searchEqualLowerValue(self, value, prop):
        propEntryDict = prop.getEntryDict()
        entryList = list()
        propType = prop.getType()

        for propValue in propEntryDict:

            if propType(propValue) <= propType(value):
                entryList.extend(propEntryDict[propValue])

        return entryList

    ''' Methods to retrieve Index & Schema Documents '''

    def getSchema(self, schemaName=None, indexName=None):
        schemaName, indexName = self.checkSchema(
            schemaName), self.checkIndex(indexName)

        return self.warehouse.getDocument(
            Schema, entry=None, schema=schemaName, index=indexName, prop=None)

    def getIndex(self, indexName=None):
        indexName = self.checkIndex(indexName)

        return self.warehouse.getDocument(
            Index, entry=None, schema=None, index=indexName, prop=None)

    def getAllIndexNames(self):
        return self.warehouse.getAllIndexName()
