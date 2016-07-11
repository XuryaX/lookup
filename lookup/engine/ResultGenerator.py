'''
Created on 16-May-2016

@author: Shauryadeep Chaudhuri
'''
from dataStore.Warehouse import Warehouse
from dataStore.WarehouseExceptions import ExistenceError
from engine.Exceptions import InvalidField, MissingField, InvalidOperation
from engine.Exceptions.ExistenceException import ExistenceException
from engine.QueryProcessor import QueryProcessor
from engine.Result import Result


class ResultGenerator(object):

    def __init__(self):

        self.processor = QueryProcessor()

    def processQuery(self, query):
        result = Result()

        try:
            message, documents = self.processor(query)
            if documents:
                result.setDocuments(documents)
            result.setMessage(message)
        except ExistenceException as e:
            result.setError(str(e))
        except InvalidField as e:
            result.setError(str(e))
        except InvalidOperation as e:
            result.setError(str(e))
        except MissingField as e:
            result.setError(str(e))

        return result