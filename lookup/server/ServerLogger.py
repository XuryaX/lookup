'''
Created on 18-May-2016

@author: Shauryadeep Chaudhuri
'''

from meta import Singleton
import logging
import time


class ServerLogger(object):
    '''
    This class will log the requests and responses by the server.
    '''

    __metaclass__ = Singleton
    def __init__(self):
        self.logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(self.logFormatter)
        
        self.logger.addHandler(consoleHandler)
    
    def setLevel(self,level):
        self.logger.setLevel(level)
    
    def getLogger(self):
        return self.logger
    
    def addHandler(self,handler):
        handler.setFormatter(self.logFormatter)
        self.logger.addHandler(handler)
        
    def addFileHandler(self,logDir):
        fileName = "log_"+time.strftime("%H_%d_%m_%y")+".log"
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logDir, fileName),mode="a+")
        fileHandler.setFormatter(self.logFormatter)
        self.logger.addHandler(fileHandler)
        
    