'''
Created on May 16, 2016

@author: Shauryadeep Chaudhuri
'''


class MissingField(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''

        super(MissingField, self).__init__(message)
