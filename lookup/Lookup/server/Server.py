'''
Created on Apr 28, 2016

@author: Shauryadeep Chaudhuri
'''

import tornado.ioloop
import tornado.web
from server.ServerLogger import ServerLogger


class Server(object):
    '''
    This is the main server configuration
    '''

    def __init__(self, portno, urlMapping):

        self.logger = ServerLogger().getLogger()
        
        self.portno = portno
        self.urlMapping = urlMapping
        self.app = tornado.web.Application(self.urlMapping)

    def startServer(self):
        
        self.logger.debug("Server Started")
        
        self.app.listen(self._portno)
        tornado.ioloop.IOLoop.instance().start()

    def stopServer(self):
        self.logger.debug("Server Stopped")
        
        tornado.ioloop.IOLoop.instance().stop()

    @property
    def portno(self):
        return self._portno

    @portno.setter
    def portno(self, portno):
        self.logger.debug("Port No Set as "+str(portno))
        
        if (not portno) or (not isinstance(portno, int)):
            raise Exception("Port Number not valid")

        if(hasattr(self, "_portno")):
            raise Exception("Port Number once set cannot be changed")

        self._portno = portno

    @property
    def urlMapping(self):
        return self._urlMapping

    @urlMapping.setter
    def urlMapping(self, urls):

        if (not urls) or (not isinstance(urls, list)):
            raise Exception("Url Mapping is not valid")

        if(hasattr(self, "_urlMapping")):
            raise Exception("URL Mapping once set cannot be changed")

        self._urlMapping = urls

