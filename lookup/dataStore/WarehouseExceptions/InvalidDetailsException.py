'''
Created on May 23, 2016

@author: Shauryadeep Chaudhuri
'''


class InvalidDetailsException(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''

        super(InvalidDetailsException, self).__init__(message)
