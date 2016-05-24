'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''


import os
import shutil

from meta import Singleton

from DataManipulator import DataManipulator
from WarehouseExceptions import ExistenceError
from WarehouseExceptions import InvalidDetailsException
import constants as c
from dataModels import Entry as Entry, Property as Property, Schema as Schema, Index as Index





class Warehouse(object):
    '''
    This is the "DataWarehouse" for the search server.
    This will contain the path to Data Files and retrieve files according to what is requested.
    '''
    __metaclass__ = Singleton

    def __init__(self, warehousePath):
        '''
        Constructor
        '''
        self.warehousePath = warehousePath

    @property
    def warehousePath(self):
        return self._warehousePath

    @warehousePath.setter
    def warehousePath(self, path):
        if(hasattr(self, "_warehousePath")):
            raise Exception("Cannot Set Warehouse Path, once it has been set")

        if not (os.path.isdir(path)):
            os.makedirs(path)

        self._warehousePath = path

    def getAllIndexName(self):
        return filter(lambda x: os.path.isdir(os.path.join(
            self.warehousePath, x)), os.listdir(self.warehousePath))

    def _checkExistence(self, docPath=None, docName=None,
                        docType=None, existReq=None):
        if docType is Property:
            docType = c.FIELD
        elif docType is Index:
            docType = c.INDEX
        elif docType is Schema:
            docType = c.SCHEMA
        elif docType is Entry:
            docType = c.ENTRY

        if os.path.exists(docPath) and existReq:
            return True
        elif not os.path.exists(docPath) and not existReq:
            return True
        else:
            if existReq is not None:
                raise ExistenceError(docPath, docName, docType, existReq)

    def _getDocPath(self, typ, entry=None, schema=None, index=None, prop=None):

        self._checkDetails(typ, entry, schema, index, prop)

        if(typ is Index):
            documentPath = os.path.join(
                self._warehousePath, index, index) + c.FILE_EXTENSION
            docName = index
        elif(typ is Schema):
            documentPath = os.path.join(
                self._warehousePath,
                index,
                schema,
                c.SCHEMAFILENAME) + c.FILE_EXTENSION
            docName = schema
        elif(typ is Property):
            documentPath = os.path.join(
                self._warehousePath,
                index,
                schema,
                c.INDICES,
                prop) + c.FILE_EXTENSION
            docName = prop
        elif (typ is Entry):
            documentPath = os.path.join(
                self._warehousePath,
                index,
                schema,
                c.DOCUMENTS,
                entry) + c.FILE_EXTENSION
            docName = entry

        return documentPath, docName

    def _checkDetails(self, typ, entry=None, schema=None,
                      index=None, prop=None):

        if(typ not in [Index, Schema, Property, Entry]):
            raise TypeError("Type must be one of these values:" +
                            str([Index, Schema, Property, Entry]))

        if (not isinstance(entry, str) and not isinstance(entry, unicode) and entry is not None) and \
                (not isinstance(schema, str) and not isinstance(schema, unicode) and schema is not None) and\
                (not isinstance(index, str) and not isinstance(index, index) and index is not None) and \
                (not isinstance(prop, str) and not isinstance(prop, unicode) and prop is not None):
            raise TypeError("Arguments are of invalid Type.")

        if typ is Index:
            if index is None:
                raise InvalidDetailsException("Must provide Index for Index")
        if typ is Schema:
            if index is None or schema is None:
                raise InvalidDetailsException(
                    "Must provide Index,Schema for Schema")
        elif typ is Property:
            if index is None or schema is None or prop is None:
                raise InvalidDetailsException(
                    "Must provide Index,Schema,Property for Property")
        elif typ is Entry:
            if index is None or schema is None or entry is None:
                raise InvalidDetailsException(
                    "Must provide Index,Schema,Entry for Entry")

        return

    def getDocument(self, typ, entry=None, schema=None, index=None, prop=None):

        documentPath, docName = self._getDocPath(
            typ, entry, schema, index, prop)

        self._checkExistence(documentPath, docName, typ, True)

        with DataManipulator(typ, documentPath, 'read') as doc:
            data = doc.readData()

        return data

    def createDocument(self, document, entry=None,
                       schema=None, index=None, prop=None):

        typ = type(document)

        documentPath, docName = self._getDocPath(
            typ, entry, schema, index, prop)

        self._checkExistence(documentPath, docName, typ, False)

        if typ is Schema:

            self.editDocument(
                data=document.getSchemaName(),
                typ=Index,
                op=c.ADD,
                index=index)

        elif typ is Entry:

            self._editProperties(
                document.getFieldValueDict(),
                entry,
                schema,
                index,
                document.getEntryName())
            self._addEntryToSchema(
                document.getFieldValueDict(), entry, schema, index)

        with DataManipulator(typ, documentPath, 'write') as doc:
            doc.createData(document)

    '''Method to add Fields and Entries in Schema Mapping File'''

    def _addEntryToSchema(self, fieldValueDict, entry, schema, index):

        fieldTypeDict = dict()

        for field in fieldValueDict.keys():
            if(type(fieldValueDict[field]) not in c.PERMISSIBLETYPES):
                raise Exception(
                    "Type: " +
                    type(
                        fieldValueDict[field]) +
                    " not permitted. Please use one of " +
                    c.PERMISSIBLETYPES)
            else:
                fieldTypeDict[field] = type(fieldValueDict[field])

        self.editDocument(
            data=[
                entry,
                fieldTypeDict],
            typ=Schema,
            op=c.ADD,
            entry=None,
            schema=schema,
            index=index,
            prop=None)

    '''Methods Relating to Editing Documents'''

    def editDocument(self, data, typ, op, entry=None,
                     schema=None, index=None, prop=None):

        if op.upper() not in c.OPERATIONS:
            raise Exception("Invalid Operation Specified")

        documentPath, docName = self._getDocPath(
            typ, entry, schema, index, prop)

        self._checkExistence(documentPath, docName, typ, True)

        if typ is Entry:
            if op.upper() == c.ADD:
                self._editEntryMeta(data, entry, schema, index)

        with DataManipulator(typ, documentPath, 'write') as doc:
            if(op.upper() == c.ADD):
                doc.addData(data)
            elif(op.upper() == c.DELETE):
                doc.deleteData(data)

    def _editEntryMeta(self, fieldValueDict, entry, schema, index):
        try:
            self._delEntryFromProperties(fieldValueDict, entry, schema, index)
        except ValueError:
            pass
        except ExistenceError:
            pass

        self._editProperties(fieldValueDict, entry, schema, index, entry)

        self._addEntryToSchema(fieldValueDict, entry, schema, index)

    '''Method to Add Document to respective Properties/Indices'''

    def _editProperties(self, fieldValueDict, entry, schema, index, entryName):

        for field in fieldValueDict.keys():
            propertyPath, _propName = self._getDocPath(
                typ=Property, entry=entry, schema=schema, index=index, prop=field)
            value = fieldValueDict[field]

            if(isinstance(value, str)):
                for splitValue in value.split(' '):
                    entryProperty = Property(
                        PropertyName=field, EntryDict={
                            splitValue: [entryName]})
                    self._genProperty(
                        propertyPath, entryProperty, entry, schema, index, field)
            else:
                entryProperty = Property(
                    PropertyName=field, EntryDict={
                        value: [entryName]})
                self._genProperty(
                    propertyPath,
                    entryProperty,
                    entry,
                    schema,
                    index,
                    field)

    def _genProperty(self, propertyPath, entryProperty,
                     entry, schema, index, field):

        if (self._checkExistence(propertyPath)):
            self.createDocument(document=entryProperty, entry=entry,
                                schema=schema, index=index, prop=field)
        else:
            self.editDocument(data=entryProperty.getEntryDict(), typ=Property, op=c.ADD,
                              entry=entry, schema=schema, index=index, prop=field)

    '''Methods relating to deleting Document or Data from Documents'''

    def deleteDocument(self, typ, entry, schema=None, index=None, prop=None):

        self._validateInputBeforeDelete(typ, entry, schema, index, prop)

        documentPath, docName = self._getDocPath(
            typ, entry, schema, index, prop)

        self._checkExistence(documentPath, docName, typ, True)

        if typ is Index:
            path = os.path.dirname(str(documentPath))
            shutil.rmtree(path)
        elif typ is Schema:
            path = os.path.dirname(str(documentPath))

            self.editDocument(data=schema, typ=Index, op=c.DELETE, index=index)

            shutil.rmtree(path)

        elif typ is Property:

            propObj = self.getDocument(
                typ=typ,
                entry=entry,
                schema=schema,
                index=index,
                prop=prop)

            entryDict = propObj.getEntryDict()

            for value in entryDict.keys():
                for entry in entryDict[value]:
                    self._delPropertyFromEntry(prop, entry, schema, index)

            self._delPropertyFromSchema(prop, schema, index)

            os.remove(documentPath)

        elif typ is Entry:
            doc = self.getDocument(
                typ=typ,
                entry=entry,
                schema=schema,
                index=index,
                prop=prop)

            self._delEntryFromProperties(
                doc.getFieldValueDict(), entry, schema, index)

            self._delEntryFromSchema(entry, schema, index)

            os.remove(documentPath)

    def _validateInputBeforeDelete(
            self, typ, entry, schema=None, index=None, prop=None):
        if(typ is Index):
            if entry is not None or schema is not None or prop is not None:
                raise InvalidDetailsException(
                    "Provide only Type,Index Name to delete Index")
        elif(typ is Schema):
            if entry is not None or prop is not None:
                raise InvalidDetailsException(
                    "Provide only Type,Index Name,Schema Name to delete Schema")
        elif typ is Entry:
            if prop is not None:
                raise InvalidDetailsException(
                    "Do not provide Property for deleting Entry")
        elif typ is Property:
            if entry is not None:
                raise InvalidDetailsException(
                    "Do not provide Entry for deleting Property")

    def _delEntryFromProperties(self, fieldValueDict, entry, schema, index):
        for field in fieldValueDict.keys():
            self.editDocument(
                entry,
                Property,
                c.DELETE,
                entry=None,
                schema=schema,
                index=index,
                prop=field)

    def _delEntryFromSchema(self, entry, schema, index):
        self.editDocument({c.ENTRY: [entry]},
                          Schema,
                          c.DELETE,
                          entry=None,
                          schema=schema,
                          index=index,
                          prop=None)

    def _delPropertyFromEntry(self, field, entry, schema, index):
        self.editDocument(
            field,
            Entry,
            c.DELETE,
            entry=entry,
            schema=schema,
            index=index,
            prop=None)

    def _delPropertyFromSchema(self, field, schema, index):
        self.editDocument({c.FIELD: [field]},
                          Schema,
                          c.DELETE,
                          entry=None,
                          schema=schema,
                          index=index,
                          prop=None)
