'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''

from Server import Server
from dataStore.Warehouse import Warehouse
from server.config.ServerConfig import ServerConfig
from server.ServerLogger import ServerLogger

class Launcher(object):
    '''
    This class sets up and configures the Server and starts it.
    '''

    def __init__(self, configPath):
        serverConfig = ServerConfig(configPath)

        self.warehouse = Warehouse(serverConfig.getWarehousePath())

        logMngr = ServerLogger()
        logMngr.addFileHandler(serverConfig.getLogDirectory())

        self.server = Server(int(serverConfig.getPortNo()),
                             serverConfig.getURLHandlers())
        

        

    def startServer(self):
        self.server.startServer()

    def stopServer(self):
        self.server.stopServer()
