'''
Created on May 16, 2016

@author: Shauryadeep Chaudhuri
'''

from ConfigReader import ConfigReader


import os
from .. import Constants as c


class ServerConfig(object):
    '''
    This class contains the configuration of the server
    '''

    def __init__(self, configPath):

        self.config = ConfigReader(configPath)

        self.warehousePath = self.config.getWarehousePath()
        self.portNo = self.config.getPortNo()
        
        self.logDir = self.config.getLogDir()

        self.urlHandlers = c.URLHANDLERS

    def getLogDirectory(self):
        if not os.path.exists(self.logDir):
            os.makedirs(self.logDir)
        return self.logDir
    
    def getPortNo(self):
        return self.portNo

    def getWarehousePath(self):
        return self.warehousePath

    def getURLHandlers(self):
        return self.urlHandlers
