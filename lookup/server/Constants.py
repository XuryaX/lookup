'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''
from server.urlHandlers.GetFromURL import GetFromURL
from server.urlHandlers.GetQueryFromURL import GetQueryFromURL
from server.urlHandlers.LookupDetails import LookupDetails
from server.urlHandlers.RequestHandler import RequestHandler


HANDLEREQUEST = (r"/", RequestHandler)
ABOUT = (r"/about", LookupDetails)
ABOUT2 = (r"/about/", LookupDetails)


GETINDEX = (r"/([A-Za-z0-9]*)", GetFromURL)
GETSCHEMA = (r"/([A-Za-z0-9]*)/([A-Za-z0-9]*)", GetFromURL)
GETENTRY = (r"/([A-Za-z0-9]*)/([A-Za-z0-9]*)/([A-Za-z0-9]*)", GetFromURL)
GETQUERY = (r"/([A-Za-z0-9]*)/([A-Za-z0-9]*)/query=(.*)", GetQueryFromURL)


URLHANDLERS = [
    HANDLEREQUEST,
    ABOUT,
    ABOUT2,
    GETINDEX,
    GETSCHEMA,
    GETENTRY,
    GETQUERY]
