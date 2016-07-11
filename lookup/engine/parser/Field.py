'''
Created on May 13, 2016

@author: Shauryadeep Chaudhuri
'''


class Field(object):
    '''
    classdocs
    '''

    def __init__(self, field, value, comparator):
        self.setField(field)
        self.setValue(value)
        self.setComparator(comparator)

    def getField(self):
        return self._field

    def setField(self, field):
        self._field = field

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def getComparator(self):
        return self._comparator

    def setComparator(self, comparator):
        if comparator not in ('==', '!=', '<', '>', '<=',
                              '>=', 'has', 'in', 'hasnot', 'notin'):
            raise Exception('Invalid Comparator')
        self._comparator = comparator

    def negate(self):
        if self._comparator == '==':
            self.setComparator('!=')
        elif self._comparator == '!=':
            self.setComparator('==')
        elif self._comparator == '<':
            self.setComparator('>=')
        elif self._comparator == '<=':
            self.setComparator('>')
        elif self._comparator == '>':
            self.setComparator('<=')
        elif self._comparator == '>=':
            self.setComparator('<')
        elif self._comparator == 'hasnot':
            self.setComparator('has')
        elif self._comparator == 'has':
            self.setComparator('hasnot')
        elif self._comparator == 'in':
            self.setComparator('notin')
        elif self._comparator == 'notin':
            self.setComparator('in')

    def __str__(self):
        return self.getField() + self.getComparator() + self.getValue()

    def __repr__(self):
        return self.__str__()
