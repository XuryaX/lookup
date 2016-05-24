'''
Created on May 16, 2016

@author: Shauryadeep Chaudhuri
'''


class ExistenceException(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''

        super(ExistenceException, self).__init__(message)
