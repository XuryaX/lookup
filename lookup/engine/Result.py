'''
Created on May 5, 2016

@author: Shauryadeep Chaudhuri
'''


class Result(object):
    '''
    Result whose dictionary would be converted to JSON and returned to the user
    '''

    def calculateHits(self):
        if isinstance(self.documents, list):
            self.hits = len(self.documents)
        else:
            self.hits = 1

    def setDocuments(self, documents):
        self.documents = documents
        self.calculateHits()

    def setMessage(self, msg):
        self.message = msg

    def setError(self, err):
        self.Error = err

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
