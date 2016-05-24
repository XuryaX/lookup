'''
Created on May 5, 2016

@author: Shauryadeep Chaudhuri
'''


import Constants as c
from dataStore.WarehouseExceptions import ExistenceError
from dataStore.helpers import JsonLoader
from engine.DataAccess import Update, Search, Delete
from engine.parser import QueryParser

from .Exceptions import *


class QueryProcessor(object):
    '''
    This is a method which will parse the query which the user gives.
    '''

    def __init__(self):
        self.jsonLoader = JsonLoader
        self.creator = Update()
        self.getter = Search()

    def __call__(self, query):
        queryDict = self.jsonLoader(query)

        if c.OPERATION in queryDict.keys():
            if queryDict[c.OPERATION] == c.ADD:

                opFunction = self._add

            elif queryDict[c.OPERATION] == c.DELETE:

                opFunction = self._delete

            elif queryDict[c.OPERATION] == c.UPDATE:

                opFunction = self._update

            elif queryDict[c.OPERATION] == c.GET:

                opFunction = self._get

            else:
                raise InvalidOperation("Operation Specified is not Valid")
        else:
            raise MissingField("Operation not Specified")

        return opFunction(queryDict)

    def _add(self, queryDict):

        index = None
        schema = None
        entry = None

        try:
            index = queryDict[c.INDEX]

            if(c.SCHEMA in queryDict):
                schema = queryDict[c.SCHEMA]

            if(c.ENTRY in queryDict):
                fieldValueDict = dict()

                entry = queryDict[c.ENTRY]

                for key in queryDict.keys():
                    if key not in [c.INDEX, c.SCHEMA, c.OPERATION, c.ENTRY]:
                        fieldValueDict[key] = queryDict[key]

            else:
                for key in queryDict.keys():
                    if key not in [c.INDEX, c.SCHEMA, c.OPERATION, c.ENTRY]:
                        raise InvalidField(
                            "Additional Fields while creating Entry is not allowed")

            if index and schema and entry:
                self.creator.createEntry(
                    entryName=entry,
                    schemaName=schema,
                    indexName=index,
                    fieldValueDict=fieldValueDict)
            elif index and schema:
                self.creator.createSchema(schemaName=schema, indexName=index)
            else:
                self.creator.createIndex(indexName=index)

            return c.ADDSUCESS, []

        except ExistenceError as e:
            raise ExistenceException(
                "The Specified " +
                e.docType +
                " " +
                e.docName +
                " already exists")
        except KeyError:
            raise

    def _delete(self, queryDict):
        try:
            for key in queryDict.keys():
                if key not in [c.INDEX, c.SCHEMA,
                               c.OPERATION, c.ENTRY, c.QUERY, c.FIELD]:
                    raise InvalidField(
                        "Invalid Field in Get Query: " + str(key))

            docType, document = self._getDocumentList(queryDict)

            eraser = Delete()

            if docType == c.ENTRY:

                for entry in document:
                    eraser.deleteEntry(
                        entry, queryDict[
                            c.SCHEMA], queryDict[
                            c.INDEX])

            elif docType == c.SCHEMA:
                eraser.deleteSchema(document, queryDict[c.INDEX])
            elif docType == c.INDEX:
                eraser.deleteIndex(document)
            elif docType == c.FIELD:
                eraser.deleteField(
                    document, queryDict[
                        c.SCHEMA], queryDict[
                        c.INDEX])

            return c.DELETESUCESS, []

        except ExistenceError as e:
            raise ExistenceException(
                "The Specified " +
                e.docType +
                " " +
                e.docName +
                " does not exist")

    def _update(self, queryDict):
        try:
            index = queryDict[c.INDEX]

            _docType, docList = self._getDocumentList(queryDict)

            if(c.SCHEMA in queryDict):
                schema = queryDict[c.SCHEMA]

            if(c.ENTRY in queryDict or c.QUERY in queryDict):
                fieldValueDict = dict()

                for key in queryDict.keys():
                    if key not in [c.INDEX, c.SCHEMA,
                                   c.OPERATION, c.ENTRY, c.QUERY]:
                        fieldValueDict[key] = queryDict[key]

            else:
                raise InvalidOperation("Only Entries Can be Updated")

            if not len(fieldValueDict.keys()):
                raise MissingField("Please provide fields to update")

            for entry in docList:
                self.creator.editEntry(entry, schema, index, fieldValueDict)

            return c.UPDATESUCESS, []

        except ExistenceError as e:
            raise ExistenceException(
                "The Specified " +
                e.docType +
                " " +
                e.docName +
                " does not exist")
        except:
            raise

    def _get(self, queryDict):
        try:

            for key in queryDict.keys():
                if key not in [c.INDEX, c.SCHEMA,
                               c.OPERATION, c.ENTRY, c.QUERY, c.FIELD]:
                    raise InvalidField(
                        "Invalid Field in Get Query: " + str(key))

            docType, document = self._getDocumentList(queryDict)

            if docType == c.ENTRY:
                entryDetailList = list()

                for entry in document:
                    entryDetailList.append(
                        self.getter.getEntry(
                            entryName=entry))
                doc = entryDetailList
            elif docType == c.SCHEMA:
                doc = self.getter.getSchema(document)
            elif docType == c.INDEX:
                doc = self.getter.getIndex(document)

            if doc:
                return c.FETCHSUCCESS, doc
            else:
                return c.NONEFOUND, doc
        except ExistenceError as e:
            raise ExistenceException(
                "The Specified " +
                e.docType +
                " " +
                e.docName +
                " does not exist")

    def _getDocumentList(self, queryDict):
        index = None
        schema = None
        entry = None
        query = None
        field = None

        try:
            index = queryDict[c.INDEX]

            if(c.SCHEMA in queryDict):
                schema = queryDict[c.SCHEMA]
                if(c.FIELD in queryDict):
                    field = queryDict[c.FIELD]

            self.getter.setIndex(index)
            self.getter.setSchema(schema)

            if(c.ENTRY in queryDict):

                entry = queryDict[c.ENTRY]
            elif(c.QUERY in queryDict):
                query = queryDict[c.QUERY]

            if query and entry:
                raise InvalidOperation(
                    "Please Do not provide both query and entry name for searching")

            if entry:
                return [c.ENTRY, [entry]]
                # return self.getter.getEntry(entryName=entry)
            elif query:
                parser = QueryParser(self.getter)
                return [c.ENTRY, parser.getResults(query)]

            elif field:
                return [c.FIELD, field]
            elif schema:
                return [c.SCHEMA, schema]
            elif index:
                return[c.INDEX, index]

            else:
                raise MissingField(
                    "Please Provide Document Information -  Index,Schema,Entry or Query")
        except KeyError as e:
            raise MissingField(
                "Please Provide Document Information -  Index,Schema,Entry,Field or Query")
