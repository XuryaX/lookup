'''
Created on Apr 29, 2016

@author: Shauryadeep Chaudhuri
'''

import errno
import os

import constants as c
from dataModels import Property, Schema, Entry, Index


class DataManipulator(object):
    '''
    classdocs
    '''

    def __init__(self, typ, docPath, mode):
        '''
        Constructor
        '''

        if(typ not in [Entry, Index, Schema, Property]):
            raise Exception("Invalid Type: +" + str(typ))

        self.docPath = docPath
        self.mode = mode
        self.docType = typ

    def __enter__(self):
        if(self.mode == "read"):

            self.dataFile = open(self.docPath, 'r+')

        if(self.mode == "write"):
            if not (os.path.exists(self.docPath)):
                if not (os.path.exists(os.path.dirname(self.docPath))):
                    try:
                        os.makedirs(os.path.dirname(self.docPath))
                    except OSError as e:
                        if e.errno == errno.EEXIST:
                            pass
                        else:
                            raise
            self.dataFile = open(self.docPath, 'a+')
        return self

    def readData(self):
        x = self.dataFile.read()
        return self.docType(jsonrep=x)

    def createData(self, docObject):

        if(self.docType is Index):

            if not isinstance(docObject, Index):
                raise TypeError("Document Object is not of Index Type")

        elif(self.docType is Schema):

            if not isinstance(docObject, Schema):
                raise TypeError("Document Object is not of Schema Type")

        elif(self.docType is Property):

            if not isinstance(docObject, Property):
                raise TypeError("Document Object is not of Property Type")

        elif (self.docType is Entry):
            if not isinstance(docObject, Entry):
                raise TypeError("Document Object is not of Entry Type")

        self.dataFile.write(docObject.getJson())

    def deleteData(self, deleteData):

        try:
            if(self.docType is Index):
                document = self.readData()

                if(isinstance(deleteData, list)):
                    document.delSchemaList(deleteData)
                else:
                    document.delSchema(deleteData)

            elif(self.docType is Schema):
                document = self.readData()

                if(c.ENTRY in deleteData.keys()):
                    document.delEntries(deleteData[c.ENTRY])
                if(c.FIELD in deleteData.keys()):
                    document.delFields(deleteData[c.FIELD])

            elif(self.docType is Property):
                document = self.readData()

                document.delEntry(deleteData)

            elif(self.docType is Entry):
                document = self.readData()

                if isinstance(deleteData, list):
                    document.delFields(deleteData)
                else:
                    document.delField(deleteData)

        except:
            raise

        self.dataFile.truncate(0)
        self.dataFile.write(document.getJson())

    def addData(self, addData):

        try:
            if(self.docType is Index):
                document = self.readData()

                if(isinstance(addData, str)):
                    document.addSchema(addData)
                else:
                    document.addSchemaList(addData)

            elif(self.docType is Schema):
                document = self.readData()

                if(isinstance(addData, list)):
                    if(len(addData) == 2):
                        document.addEntry(addData[0])
                        document.addField(addData[1])
                    else:
                        raise "List Not in Format"
                else:
                    document.addField(addData)

            elif(self.docType is Property):

                document = self.readData()

                document.addEntryDict(addData)

            elif(self.docType is Entry):
                document = self.readData()

                document.updateField(addData)

        except:
            raise

        self.dataFile.truncate(0)
        self.dataFile.write(document.getJson())

    def __exit__(self, *args):
        self.dataFile.close()
