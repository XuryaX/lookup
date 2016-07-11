'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''
import json

import tornado

from engine import Constants as c
from engine.ResultGenerator import ResultGenerator

from ..ServerLogger import ServerLogger


class RequestHandler(tornado.web.RequestHandler):
    '''
    This class handles the 4 requests GET,POST,PUT,DELETRE
    '''

    def initialize(self):
        tornado.web.RequestHandler.initialize(self)
        self.resultGenerator = ResultGenerator()
        
        self.logger = ServerLogger().getLogger()

    def post(self):
        try:
            self.logger.info("Request Query: "+self.request.body)
            
            query = json.loads(self.request.body)
            query[c.OPERATION] = c.UPDATE
            
            self.logger.debug("Query Sent: "+str(query))
            
            result = str(self.resultGenerator.processQuery(json.dumps(query)))
            
            self.logger.info("Result Fetched: "+result)
            
            self.write(result)
        except Exception as e:
            self.logger.error('Error ', exc_info=True)
            
            self.write("Error: " + str(e))

    def get(self):
        try:
            self.logger.info("Request Query: "+self.request.body)
            
            query = json.loads(self.request.body)
            query[c.OPERATION] = c.GET
            
            self.logger.debug("Query Sent: "+str(query))
            
            result = str(self.resultGenerator.processQuery(json.dumps(query)))
            
            self.logger.info("Result Fetched: "+result)
            
            self.write(result)
        except Exception as e:
            self.logger.error('Error', exc_info=True)
            
            self.write("Error: " + str(e))

    def put(self):
        try:
            self.logger.info("Request Query: "+self.request.body)
            
            query = json.loads(self.request.body)
            query[c.OPERATION] = c.ADD
            
            self.logger.debug("Query Sent: "+str(query))
            
            result = str(self.resultGenerator.processQuery(json.dumps(query)))
            
            self.logger.info("Result Fetched: "+result)
            
            self.write(result)
        except Exception as e:
            self.logger.error('Error', exc_info=True)
            
            self.write("Error: " + str(e))

    def delete(self):
        try:
            self.logger.info("Request Query: "+self.request.body)
            
            query = json.loads(self.request.body)
            query[c.OPERATION] = c.DELETE
            
            self.logger.debug("Query Sent: "+str(query))
            
            result = str(self.resultGenerator.processQuery(json.dumps(query)))
            
            self.logger.info("Result Fetched: "+result)
            
            self.write(result)
        except Exception as e:
            self.logger.error('Error', exc_info=True)
            
            self.write("Error: " + str(e))
