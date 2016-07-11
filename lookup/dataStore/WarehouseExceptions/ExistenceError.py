'''
Created on May 3, 2016

@author: Shauryadeep Chaudhuri
'''


class ExistenceError(Exception):
    '''
    This error occurs if a Document Exists when its not required to(Like when adding document with same name)
    and Not Existing when its Required to.(When Deleting a document.)
    '''

    def __init__(self, docPath, docName, docType, req):
        '''
        Constructor
        '''
        self.docName = docName
        self.docType = docType

        if(req):
            message = "Document does not exist at path " + str(docPath)
        else:
            message = "Document already exists at path " + str(docPath)

        super(ExistenceError, self).__init__(message)
