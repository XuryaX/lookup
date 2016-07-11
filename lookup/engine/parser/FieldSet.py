"""
Created on May 12, 2016

@author: Shauryadeep Chaudhuri
"""
from Field import Field


class FieldSet(object):
    _retriever = None

    def __init__(self, field, retriever):
        self.fields = [field]
        if not self._retriever:
            self._retriever = retriever

    def retrieveElements(self):
        if not hasattr(self, 'elementSet'):
            self.elementSet = set()
            entryList = self._retriever.SearchEntryInProperty(
                self.fields[0].getValue(),
                self.fields[0].getComparator(),
                self.fields[0].getField())
            self.elementSet.update(set(entryList))

    def union(self, otherSet):
        if not hasattr(self, 'elementSet'):
            self.retrieveElements()
        self.elementSet.update(otherSet.getSet())
        self.fields.extend(otherSet.getFields())

    def intersection(self, otherSet):
        if not hasattr(self, 'elementSet'):
            self.retrieveElements()
        self.elementSet.intersection_update(otherSet.getSet())
        self.fields.extend(otherSet.getFields())

    def getSet(self):
        if not hasattr(self, 'elementSet'):
            self.retrieveElements()
        return self.elementSet

    def getFields(self):
        return self.fields
