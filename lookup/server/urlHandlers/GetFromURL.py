'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''

import json

import tornado

from engine import Constants as c
from engine.ResultGenerator import ResultGenerator
from ..ServerLogger import ServerLogger


class GetFromURL(tornado.web.RequestHandler):
    '''
    This class fetches the data requested like index,schema,entry,query from the url and responds with the result
    '''
    def initialize(self):
        self.logger = ServerLogger().getLogger()
        
    def get(self, index=None, schema=None, entry=None, query=None):

        query = dict()

        resultGenerator = ResultGenerator()

        query[c.OPERATION] = c.GET

        if index:
            query[c.INDEX] = index
        if schema:
            query[c.SCHEMA] = schema
        if entry:
            query[c.ENTRY] = entry
        
        self.logger.debug("Internal Query Generated"+str(query))
        
        try:
            result = str(resultGenerator.processQuery(json.dumps(query)))
            
            self.logger.info("Result fetched:" + result)
            
            self.write(result)
        except Exception as e:
            self.logger.error('Error', exc_info=True)
            
            self.write("Error: " + str(e))
