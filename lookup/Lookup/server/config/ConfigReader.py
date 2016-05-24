'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''

import ConfigParser


class ConfigReader(object):
    '''
    classdocs
    '''

    def __init__(self, configPath):
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)

    def getPortNo(self):
        return self.config.get("CONFIG", "PORTNO")

    def getWarehousePath(self):
        return self.config.get("CONFIG", "WAREHOUSEPATH")
    
    def getLogDir(self):
        return self.config.get("CONFIG", "LOGDIR")
