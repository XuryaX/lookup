'''
Created on May 16, 2016

@author: Shauryadeep Chaudhuri
'''


class InvalidOperation(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''

        super(InvalidOperation, self).__init__(message)
