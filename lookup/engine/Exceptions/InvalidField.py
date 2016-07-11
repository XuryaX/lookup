'''
Created on May 16, 2016

@author: Shauryadeep Chaudhuri
'''


class InvalidField(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''

        super(InvalidField, self).__init__(message)
